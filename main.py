from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import httpx
import uuid
import os
import jwt
import json
import hashlib
from datetime import datetime, timedelta
import logging
import asyncio
from typing import List, Any, Dict, Optional
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# Import our modular logic
from models import (
    UserRequest, UserContext, RequestContext, OPAInput, OPAVerdict, 
    AgentResponse, EscalationResolution, EscalationResponse, SystemContext
)
from detection import DetectionService
from database import save_audit_log, ContextStore
from tools import ToolExecutionService, AGENT_TOOLS

# Initialize the app and services
app = FastAPI(title="Policy-Jarl Guardrail Service")
detector = DetectionService()
context_store = ContextStore()
tool_service = ToolExecutionService()
logger = logging.getLogger("uvicorn.error")

# Configuration from Environment
OPA_URL = os.getenv("OPA_URL", "http://opa:8181/v1/data/jarl/verdict")
AGENT_URL = os.getenv("AGENT_URL", "http://agent:8900/v1/chat/completions")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
AGENT_MODEL = os.getenv("AGENT_MODEL", "gemini-3.1-flash-lite-preview")
JWT_SECRET = os.getenv("JWT_SECRET", "jarl-default-secret-key")
ROOT_ADMIN_ID = os.getenv("ROOT_ADMIN_ID", "6693628053")
EMERGENCY_SECRET = os.getenv("EMERGENCY_SECRET", "JARL_BREAK_GLASS_2026")

# --- UI CONSTANTS ---
ROLE_EMOJIS = {
    "admin": "👑",
    "hr_analytics": "📋",
    "ops_manager": "⚙️",
    "finance_analyst": "💰",
    "data_clerk": "✍️",
    "guest": "👤",
    "pending": "⏳"
}

ROLE_SHORTHANDS = {
    "hr": "hr_analytics",
    "ops": "ops_manager",
    "fin": "finance_analyst",
    "adm": "admin",
    "gst": "guest",
    "clerk": "data_clerk",
    "data": "data_clerk"
}

def get_role_ui(role: str) -> str:
    """Returns a formatted role string with emoji and capitalized name (underscore to space)."""
    ui_name = role.replace("_", " ").upper()
    return f"{ROLE_EMOJIS.get(role, '👤')} <b>{ui_name}</b>"

def resolve_role(role: str) -> str:
    """Maps shorthands like 'hr' to the full role name."""
    role = role.lower().strip()
    return ROLE_SHORTHANDS.get(role, role)

def resolve_target_id(target: str) -> str | None:
    """Resolves an @username or numeric ID into a clean User ID."""
    if target.isdigit():
        return target
    # Check for username in registry
    resolved = context_store.get_id_by_username(target)
    return resolved

# --- UTILS ---

def log_system_event(user_id: str, action: str, decision: str, reason: str, role: str = None, status: str = None, username: str = None, original_sql: str = None, patched_sql: str = None):
    """Utility to log events with high-fidelity state tracking and null-scrubbing for the Witness (ELK)."""
    # Fetch the LATEST state from Redis to ensure the log is never stale
    profile = context_store.get_user_profile(user_id)
    current_status = status or (profile.get("status") if profile else "UNKNOWN")
    current_role = role or (profile.get("active_role") if profile else "guest")
    current_username = username or (profile.get("username") if profile else "Anon")

    # SCRUBBING: Replace nulls with descriptive context
    raw_entry = {
        "event_id": str(uuid.uuid4()),
        "correlation_id": f"sys_{int(datetime.utcnow().timestamp())}",
        "user_id": user_id,
        "username": current_username,
        "user_role": current_role,
        "action": action,
        "decision": decision,
        "reason": reason,
        "status": current_status,
        "original_sql": original_sql or "N/A",
        "executed_sql": patched_sql or "N/A"
    }
    save_audit_log(raw_entry)

def is_active_admin(user_id: str) -> bool:
    """Strict Verification: Does the user have a valid JWT with the 'admin' role?"""
    profile = context_store.get_user_profile(user_id)
    if not profile or not profile.get("token"):
        return False
    try:
        payload = jwt.decode(profile["token"], JWT_SECRET, algorithms=["HS256"])
        return payload.get("role") == "admin"
    except:
        return False

def check_username_change(user_id: str, incoming_username: str):
    """Detects if a user changed their Telegram handle and logs it for auditing."""
    profile = context_store.get_user_profile(user_id)
    if not profile: return
    
    old_username = profile.get("username")
    if incoming_username and old_username and incoming_username != old_username:
        log_system_event(
            user_id, 
            "username_change", 
            "NOTICE", 
            f"Changed from @{old_username} to @{incoming_username}", 
            profile.get("active_role"),
            profile.get("status"),
            incoming_username
        )
        profile["username"] = incoming_username
        context_store.save_user_profile(user_id, profile)

async def send_agent_request(client, payload, max_retries=3):
    """Sends a request to the agent with exponential backoff for 503 errors."""
    for attempt in range(max_retries):
        try:
            resp = await client.post(AGENT_URL, json=payload, timeout=300.0)
            if resp.status_code == 503:
                wait = (attempt + 1) * 2
                logger.warning(f"Agent API busy (503), retrying in {wait}s...")
                await asyncio.sleep(wait)
                continue
            return resp
        except Exception as e:
            if attempt < max_retries - 1:
                await asyncio.sleep((attempt + 1) * 2)
                continue
            raise e
    return None

def generate_admin_token(user_id: str, role: str) -> str:
    """Generates a cryptographically signed JWT."""
    payload = {
        "sub": user_id,
        "role": role,
        "iat": int(datetime.utcnow().timestamp()),
        "exp": int((datetime.utcnow() + timedelta(days=1)).timestamp())
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

async def safe_reply(update: Update, text: str, parse_mode="HTML"):
    """Safely sends a message regardless of update type, defaulting to HTML for reliability."""
    try:
        if update.message:
            await update.message.reply_text(text, parse_mode=parse_mode)
        elif update.effective_message:
            await update.effective_message.reply_text(text, parse_mode=parse_mode)
        else:
            await update.effective_chat.send_message(text, parse_mode=parse_mode)
    except Exception as e:
        # FALLBACK: Send as plain text if HTML tags are malformed
        try:
            if update.message:
                await update.message.reply_text(text, parse_mode=None)
            elif update.effective_message:
                await update.effective_message.reply_text(text, parse_mode=None)
            else:
                await update.effective_chat.send_message(text, parse_mode=None)
        except Exception as final_e:
            logger.error(f"FATAL_REPLY_ERROR: {str(final_e)}")

# --- TELEGRAM BOT LOGIC ---

async def handle_auth_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Callback for confirming a user authorization."""
    query = update.callback_query
    await query.answer()
    data = query.data
    if not data.startswith("auth_yes_"): return
    
    auth_id = data.replace("auth_yes_", "")
    pending = context_store.get_context(f"pending_auth:{auth_id}")
    if not pending:
        await query.edit_message_text("❌ <b>Session Expired</b> or already processed.", parse_mode="HTML")
        return

    target_id = pending["target_id"]
    roles = pending["roles"]
    admin_id = pending["admin_id"]

    # --- ADMIN ESCALATION LOGIC ---
    if "admin" in roles:
        all_profiles = context_store.get_all_profiles()
        has_admins = any("admin" in p.get("authorized_roles", []) for p in all_profiles)
        
        if has_admins:
            correlation_id = f"admin_grant_{auth_id}"
            context_store.save_pending_escalation(correlation_id, {
                "user_id": target_id,
                "requested_roles": roles,
                "reason": "HIGH_PRIVILEGE_ESCALATION: Granting Admin role requires dual-authorization.",
                "timestamp": datetime.utcnow().isoformat(),
                "requested_by": admin_id
            })
            log_system_event(target_id, "admin_escalation", "ESCALATE", "Admin grant pending dual-auth", status="PENDING")
            await query.edit_message_text("⚠️ <b>Security Protocol Triggered</b>: Granting the <b>ADMIN</b> role requires dual-authorization. This request has been escalated to the ELK Security Console.", parse_mode="HTML")
            context_store.r.delete(f"pending_auth:{auth_id}")
            return

    # Standard Grant
    target_profile = context_store.get_user_profile(target_id) or {"id": target_id}
    target_profile["status"] = "ACTIVE"
    target_profile["authorized_roles"] = list(set(target_profile.get("authorized_roles", [])).union(set(roles)))
    if target_profile.get("active_role") not in target_profile["authorized_roles"]:
        target_profile["active_role"] = target_profile["authorized_roles"][0]
    
    context_store.save_user_profile(target_id, target_profile)
    context_store.r.delete(f"pending_auth:{auth_id}")
    
    log_system_event(target_id, "auth", "ALLOW", f"Roles set: {', '.join(target_profile['authorized_roles'])}", target_profile.get("active_role"), "ACTIVE", target_profile.get("username"))
    await query.edit_message_text(f"✅ User <code>{target_id}</code> authorized with roles: <b>{', '.join(target_profile['authorized_roles']).upper()}</b>.", parse_mode="HTML")

async def handle_auth_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Callback for cancelling a user authorization."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("❌ <b>Action Cancelled</b>.", parse_mode="HTML")

async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Enrollment: Zero Trust Onboarding Flow with Initial Bootstrap."""
    user_id = str(update.effective_user.id)
    username = update.effective_user.username
    
    # CRITICAL SECURITY: Block Anonymous Users
    if not username:
        await safe_reply(update, "❌ <b>Access Denied</b>: Anonymous users cannot be authenticated. Please set a Telegram Username in your profile settings and try again.")
        return

    # Track username changes
    check_username_change(user_id, username)
    
    profile = context_store.get_user_profile(user_id)
    
    # 0. INITIAL BOOTSTRAP LOGIC
    all_profiles = context_store.get_all_profiles()
    if not profile and not all_profiles and user_id == ROOT_ADMIN_ID:
        profile = {
            "id": user_id, 
            "username": username, 
            "status": "ACTIVE", 
            "authorized_roles": ["admin", "guest"],
            "active_role": "admin",
            "joined": datetime.utcnow().isoformat()
        }
        profile["token"] = generate_admin_token(user_id, "admin")
        context_store.save_user_profile(user_id, profile)
        log_system_event(user_id, "enrollment", "ALLOW", "Initial Bootstrap", "admin", "ACTIVE", username)
        
        msg = (
            f"👑 <b>Welcome Jarl {username}!</b>\n\n"
            "Initial Installation Detected. System has been initialized with your Root Admin identity.\n"
            "Digital Passport (JWT) Issued.\n"
            f"Active Role: {get_role_ui('admin')}\n"
            "System Status: 🟢 <b>ACTIVE</b>"
        )
        await safe_reply(update, msg)
        return

    # 1. Standard PENDING flow for new users
    if not profile:
        profile = {"id": user_id, "username": username, "status": "PENDING", "joined": datetime.utcnow().isoformat()}
        context_store.save_user_profile(user_id, profile)
        log_system_event(user_id, "enrollment", "PENDING", f"User @{username} requested access.", status="PENDING", username=username)
        await safe_reply(update, "🛡️ <b>Identity Unknown.</b> Request for access sent.")
        logger.info(f"PENDING_USER: @{username} ({user_id}) has joined the waiting room.")
        return

    if profile.get("status") == "FROZEN":
        await safe_reply(update, "❄️ <b>Account Frozen.</b> Access suspended by administrator.")
        return

    if profile.get("status") != "ACTIVE":
        await safe_reply(update, "⏳ Your access request is still PENDING.")
        return
    
    # If authorized, ensure they have a passport
    active_role = profile.get('active_role', 'guest')
    role_ui = get_role_ui(active_role)
    if "admin" in profile.get("authorized_roles", []):
        profile["token"] = generate_admin_token(user_id, active_role)
        context_store.save_user_profile(user_id, profile)
    
    msg = f"👑 Welcome {username}!\nDigital Passport (JWT) Issued for {role_ui}.\nSystem Status: 🟢 <b>ACTIVE</b>"
    await safe_reply(update, msg)

async def handle_waiting_room(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lists all users in PENDING status. Admin Only."""
    user_id = str(update.effective_user.id)
    if not is_active_admin(user_id):
        await safe_reply(update, "❌ Unauthorized.")
        return
    
    profiles = context_store.get_all_profiles()
    pending = [p for p in profiles if p.get("status") == "PENDING"]
    
    if not pending:
        await safe_reply(update, "📭 The waiting room is currently empty.")
        return
    
    msg = "🚪 <b>Waiting Room</b>\n\n"
    for p in pending:
        msg += f"👤 @{p.get('username', 'Unknown')}\nID: <code>{p['id']}</code>\nJoined: {p.get('joined', 'N/A')}\n\n"
    
    msg += "Use <code>/auth &lt;id&gt; roles</code> to grant access."
    await safe_reply(update, msg)

async def handle_auth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Initiates user authorization with a confirmation step."""
    user_id = str(update.effective_user.id)
    
    if not is_active_admin(user_id):
        # Special check for bootstrap
        all_profiles = context_store.get_all_profiles()
        if any("admin" in p.get("authorized_roles", []) for p in all_profiles):
            await safe_reply(update, "❌ Unauthorized.")
            return

    if not context.args or len(context.args) < 2:
        await safe_reply(update, "Usage: <code>/auth &lt;id|@username&gt; &lt;role1,role2...&gt;</code>")
        return

    target_input = context.args[0]
    target_id = resolve_target_id(target_input)
    if not target_id:
        await safe_reply(update, f"❌ <b>Identity Unknown</b>: Could not resolve '{target_input}'.")
        return

    requested_roles = [resolve_role(r) for r in context.args[1].lower().split(",")]
    valid_roles = {"admin", "guest", "hr_analytics", "ops_manager", "finance_analyst", "data_clerk"}
    if not all(r in valid_roles for r in requested_roles):
        await safe_reply(update, "❌ Invalid role(s) detected.")
        return

    profile = context_store.get_user_profile(target_id)
    username = profile.get("username", "Unknown") if profile else "New User"
    
    auth_id = str(uuid.uuid4())[:8]
    context_store.save_context(f"pending_auth:{auth_id}", {
        "target_id": target_id,
        "roles": requested_roles,
        "admin_id": user_id
    }, ttl=300)

    msg = f"🛡️ <b>Confirm Authorization</b>\n"
    msg += f"Target: <b>@{username}</b> (<code>{target_id}</code>)\n"
    msg += f"New Roles: {', '.join([get_role_ui(r) for r in requested_roles])}\n\n"
    msg += "Do you want to apply these changes?"

    keyboard = [
        [InlineKeyboardButton("✅ Confirm", callback_data=f"auth_yes_{auth_id}"),
         InlineKeyboardButton("❌ Cancel", callback_data=f"auth_no_{auth_id}")]
    ]
    await update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

async def handle_unauth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Removes a specific role from a user. Requires ADMIN role."""
    user_id = str(update.effective_user.id)
    if not is_active_admin(user_id):
        await safe_reply(update, "❌ Unauthorized.")
        return
    if not context.args or len(context.args) < 2:
        await safe_reply(update, "Usage: <code>/unauth &lt;id|@username&gt; &lt;role&gt;</code>")
        return
    
    target_input, role_to_remove = context.args[0], resolve_role(context.args[1])
    target_id = resolve_target_id(target_input)
    if not target_id:
        await safe_reply(update, "❌ <b>Identity Unknown</b>.")
        return

    profile = context_store.get_user_profile(target_id)
    if not profile:
        await safe_reply(update, "❌ User not found.")
        return
    
    # 🛡️ ADMIN PROTECTION: Prevent removing the last admin
    if role_to_remove == "admin":
        all_profiles = context_store.get_all_profiles()
        admins = [p for p in all_profiles if "admin" in p.get("authorized_roles", [])]
        if len(admins) <= 1 and target_id in [a['id'] for a in admins]:
            await safe_reply(update, "❌ <b>Governance Block</b>: Cannot remove the last remaining Admin. Promote a new Admin first.")
            return

    roles = set(profile.get("authorized_roles", []))
    if role_to_remove in roles:
        roles.remove(role_to_remove)
        profile["authorized_roles"] = list(roles)
        if profile.get("active_role") == role_to_remove:
             profile["active_role"] = profile["authorized_roles"][0] if profile["authorized_roles"] else "guest"
             profile["token"] = None 
        context_store.save_user_profile(target_id, profile)
        log_system_event(target_id, "unauth", "ALLOW", f"Role {role_to_remove} removed", profile.get("active_role"), profile.get("status"), profile.get("username"))
        await safe_reply(update, f"✅ Role <b>{role_to_remove.upper()}</b> removed from user <code>{target_id}</code>.")

    else:
        await safe_reply(update, f"❌ User does not have role <b>{role_to_remove.upper()}</b>.")

async def handle_purge(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Wipes a user's access entirely. Requires ADMIN role."""
    user_id = str(update.effective_user.id)
    if not is_active_admin(user_id):
        await safe_reply(update, "❌ Unauthorized.")
        return
    if not context.args:
        await safe_reply(update, "Usage: <code>/purge &lt;id|@username&gt;</code>")
        return
    
    target_input = context.args[0]
    target_id = resolve_target_id(target_input)
    if not target_id:
        await safe_reply(update, "❌ <b>Identity Unknown</b>.")
        return

    # 🛡️ ADMIN PROTECTION: Prevent purging the last admin
    all_profiles = context_store.get_all_profiles()
    admins = [p for p in all_profiles if "admin" in p.get("authorized_roles", [])]
    if len(admins) <= 1 and target_id in [a['id'] for a in admins]:
        await safe_reply(update, "❌ <b>Governance Block</b>: Cannot purge the last remaining Admin.")
        return

    profile = context_store.get_user_profile(target_id)
    if not profile:
        await safe_reply(update, "❌ User not found.")
        return
    profile["status"] = "PENDING"
    profile["authorized_roles"] = []
    profile["active_role"] = "guest"
    profile["token"] = None
    context_store.save_user_profile(target_id, profile)
    log_system_event(target_id, "purge", "ALLOW", "User purged to PENDING state", status="PENDING", username=profile.get("username"))
    await safe_reply(update, f"🗑️ User <code>{target_id}</code> has been purged and reset to <b>PENDING</b>.")


async def handle_list_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lists all registered users and their status. Requires ADMIN role."""
    user_id = str(update.effective_user.id)
    if not is_active_admin(user_id):
        await safe_reply(update, "❌ Unauthorized.")
        return
    profiles = context_store.get_all_profiles()
    if not profiles:
        await safe_reply(update, "📭 No users in registry.")
        return
    msg = "👥 <b>System User Registry</b>\n\n"
    for p in profiles:
        active_role = p.get('active_role', 'guest')
        authorized = p.get("authorized_roles", [])
        status_emoji = "🟢" if p.get("status") == "ACTIVE" else "❄️" if p.get("status") == "FROZEN" else "⏳"
        
        msg += f"{status_emoji} ID: <code>{p['id']}</code> (@{p.get('username', 'Anon')})\n"
        msg += f"Active: {get_role_ui(active_role)}\n"
        msg += f"Auth: {', '.join([ROLE_EMOJIS.get(r, '👤') for r in authorized])}\n---\n"
    
    await safe_reply(update, msg)

async def handle_freeze(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Toggles the frozen status of a user. Requires ADMIN role."""
    user_id = str(update.effective_user.id)
    if not is_active_admin(user_id):
        await safe_reply(update, "❌ Unauthorized.")
        return
    if not context.args:
        await safe_reply(update, "Usage: <code>/freeze &lt;id|@username&gt;</code>")
        return
    
    target_input = context.args[0]
    target_id = resolve_target_id(target_input)
    if not target_id:
        await safe_reply(update, "❌ <b>Identity Unknown</b>.")
        return

    profile = context_store.get_user_profile(target_id)
    if not profile:
        await safe_reply(update, "❌ User not found.")
        return
    
    current_status = profile.get("status")
    new_status = "FROZEN" if current_status != "FROZEN" else "ACTIVE"
    profile["status"] = new_status
    context_store.save_user_profile(target_id, profile)
    log_system_event(target_id, "freeze", "ALLOW", f"User status set to {new_status}", profile.get("active_role"), new_status, profile.get("username"))
    await safe_reply(update, f"❄️ User <code>{target_id}</code> status set to: <b>{new_status}</b>.")

async def handle_switch_role(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Allows a user to switch between their authorized roles."""
    user_id = str(update.effective_user.id)
    if not context.args:
        await safe_reply(update, "Usage: <code>/switch_role &lt;role|shorthand&gt;</code>")
        return

    # FIX: Join arguments with underscores and normalize to handle 'hr analytics' or 'hr_analytics'
    raw_input = "_".join(context.args).lower()
    requested_role = resolve_role(raw_input)
    
    profile = context_store.get_user_profile(user_id)
    authorized_roles = profile.get("authorized_roles", ["guest"])
    if requested_role not in authorized_roles:
        await safe_reply(update, f"❌ <b>Unauthorized</b>: You are not authorized for the '{requested_role}' role.")
        return

    profile["active_role"] = requested_role
    profile["token"] = generate_admin_token(user_id, requested_role)
    context_store.save_user_profile(user_id, profile)
    
    log_system_event(user_id, "switch_role", "ALLOW", f"Switched to {requested_role}", requested_role, profile.get("status"), profile.get("username"))
    await safe_reply(update, f"✅ Switched to {get_role_ui(requested_role)} role. Identity Vault partitioned.")


async def handle_role_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Callback for role switching buttons."""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    if not data.startswith("switch_"): return
    
    # FIX: Correctly extract role name even if it contains underscores
    requested_role = data.replace("switch_", "")
    user_id = str(update.effective_user.id)
    
    # Trigger the existing switch logic
    # We create a fake context to reuse handle_switch_role or just call logic directly
    profile = context_store.get_user_profile(user_id)
    if requested_role not in profile.get("authorized_roles", []):
        await query.edit_message_text("❌ <b>Unauthorized</b> for that role.", parse_mode="HTML")
        return

    profile["active_role"] = requested_role
    profile["token"] = generate_admin_token(user_id, requested_role)
    context_store.save_user_profile(user_id, profile)
    
    log_system_event(user_id, "switch_role", "ALLOW", f"Switched to {requested_role}", requested_role, profile.get("status"), profile.get("username"))
    await query.edit_message_text(f"✅ Switched to {get_role_ui(requested_role)} role. Identity Vault partitioned.", parse_mode="HTML")

async def handle_my_roles(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lists all roles assigned to the user in an interactive 'Identity Vault' card."""
    user_id = str(update.effective_user.id)
    profile = context_store.get_user_profile(user_id)
    if not profile or profile.get("status") != "ACTIVE":
        await safe_reply(update, "❌ Not authorized.")
        return
        
    authorized = profile.get("authorized_roles", [])
    active = profile.get("active_role", "guest")
    
    msg = "<b>👤 Identity Vault</b>\n"
    msg += "──────────────────\n"
    msg += f"<b>Active Role:</b> {get_role_ui(active)}\n"
    msg += f"<b>Status:</b> 🟢 ACTIVE\n\n"
    msg += "<b>Authorized Access:</b>\n"
    
    keyboard = []
    for r in authorized:
        indicator = " (Active)" if r == active else ""
        button_text = f"{ROLE_EMOJIS.get(r, '👤')} {r.upper()}{indicator}"
        keyboard.append([InlineKeyboardButton(button_text, callback_data=f"switch_{r}")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_text(msg, reply_markup=reply_markup, parse_mode="HTML")
    else:
        await update.effective_chat.send_message(msg, reply_markup=reply_markup, parse_mode="HTML")

async def handle_emergency_stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin Only: Toggles the global Kill-Switch. Verified by JWT Role."""
    user_id = str(update.effective_user.id)
    
    if not is_active_admin(user_id):
        await safe_reply(update, "❌ Unauthorized: Active ADMIN role required.")
        return

    new_active = (context_store.get_system_status() == "LOCKED")
    context_store.set_system_status(new_active)
    status_text = "🟢 <b>ACTIVE</b>" if new_active else "🔴 <b>LOCKED</b>"
    await safe_reply(update, f"📢 <b>System Status</b>: {status_text}")

async def handle_autonomy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin Only: Toggles the 'Free Flow' autonomous mode. Verified by JWT Role."""
    user_id = str(update.effective_user.id)
    
    if not is_active_admin(user_id):
        await safe_reply(update, "❌ Unauthorized: Active ADMIN role required.")
        return

    new_enabled = (context_store.get_autonomy_mode() == "DISABLED")
    context_store.set_autonomy_mode(new_enabled)
    status_text = "🚀 <b>ENABLED</b>" if new_enabled else "🛡️ <b>DISABLED</b>"
    await safe_reply(update, f"📢 <b>Agent Autonomy</b>: {status_text}")

async def handle_unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await safe_reply(update, "❌ Unknown command.")

async def handle_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lists available commands based on the user's current role."""
    user_id = str(update.effective_user.id)
    profile = context_store.get_user_profile(user_id)
    active_role = profile.get("active_role", "guest") if profile else "guest"
    
    help_text = "🤖 <b>Policy-Jarl Help Menu</b>\n"
    help_text += f"Current Identity: {get_role_ui(active_role)}\n\n"
    
    help_text += "<b>General:</b>\n"
    help_text += "- /start: Register or check status.\n"
    help_text += "- /help: This menu.\n"

    if profile and profile.get("status") == "ACTIVE":
        help_text += "- /my_roles: List your assigned roles.\n"
        help_text += "- /switch_role &lt;role&gt;: Change active passport.\n"

    if is_active_admin(user_id):
        help_text += "\n<b>Governance (Admin Only):</b>\n"
        help_text += "- /autonomy: Toggle AI autonomy mode.\n"
        help_text += "- /emergency_stop: Global agent kill-switch.\n"
        help_text += "- /user_help: User &amp; Identity management."

    await safe_reply(update, help_text)

async def handle_user_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Specialized help for User Management. Admin Only."""
    user_id = str(update.effective_user.id)
    if not is_active_admin(user_id):
        await safe_reply(update, "❌ Unauthorized.")
        return

    help_text = (
        "👤 <b>User Management Help</b>\n\n"
        "- /waiting_room: Check pending access.\n"
        "- /auth &lt;id|@user&gt; &lt;roles&gt;: Grant access.\n"
        "- /unauth &lt;id|@user&gt; &lt;role&gt;: Revoke role.\n"
        "- /purge &lt;id|@user&gt;: Wipe all access.\n"
        "- /freeze &lt;id|@user&gt;: Suspend access.\n"
        "- /list_users: Audit registry."
    )
    await safe_reply(update, help_text)

async def handle_telegram_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    # CRITICAL SECURITY: Never let slash commands reach the AI.
    if user_text.startswith("/"):
        await handle_unknown_command(update, context)
        return

    user_id = str(update.effective_user.id)
    username = update.effective_user.username or "Anonymous"
    
    # Track username changes
    check_username_change(user_id, username)
    
    correlation_id = str(uuid.uuid4())
    bg_tasks = BackgroundTasks()
    
    # 1. INBOUND GATE
    request = UserRequest(user_id=user_id, prompt=user_text, action="chat", correlation_id=correlation_id)
    verdict = await evaluate_request(request, bg_tasks)
    if verdict.decision == "DENY":
        await safe_reply(update, f"🛡️ <b>Blocked</b>: {verdict.reason}")
        return

    # 2. AGENT FORWARDING
    await update.message.reply_chat_action("typing")
    
    # Extract identity for the agent's context
    profile = context_store.get_user_profile(user_id)
    user_jwt = profile.get("token", "NO_TOKEN")
    active_role = profile.get("active_role", "guest")
    role_ui = get_role_ui(active_role)

    # Dynamic Mission based on Role
    if active_role == "admin":
        mission = "Your mission is GLOBAL DATABASE MANAGEMENT. You are authorized to ANALYZE, INSERT, UPDATE, and DELETE data as requested by the Jarl."
    else:
        mission = "Your ONLY purpose is to provide data-driven insights. You are strictly restricted to READ-ONLY analysis and cannot perform data manipulation (INSERT, UPDATE, DELETE)."

    system_prompt = (
        f"ROLE: You are the 'Policy-Jarl' Autonomous BI Agent for {role_ui}.\n"
        f"MISSION: {mission}\n"
        "IDENTITY CONTEXT:\n"
        f"- USER_ID: {user_id}\n"
        f"- ACTIVE_ROLE: {active_role}\n"
        f"- JWT: {user_jwt}\n\n"
        "OPERATIONAL CONSTRAINTS:\n"
        "1. STRICT MISSION: Refuse all requests unrelated to database analysis or corporate governance.\n"
        "2. DATABASE ACCESS: You MUST use the 'jarl_query_db.py' relay script for ALL data tasks.\n"
        "3. GOVERNED DISCOVERY: If asked for metadata, use SQL to query information_schema.\n"
        "4. SELF-CORRECTION: If OPA returns a POLICY_ERROR, read the reason and rewrite your query to be compliant.\n"
        "5. TONE: Professional, objective, and compliant with ISO 42001 standards.\n"
        "6. FORMATTING: You MUST use Telegram-compatible HTML tags ONLY:\n"
        "   - Use <b>bold</b> and <i>italic</i>.\n"
        "   - Use <code>inline code</code> and <pre>block code</pre>.\n"
        "   - Lists: Use emoji bullets (• or ‣) or simple dashes (-). NEVER use <ul> or <li> tags.\n"
        "   - DO NOT use Markdown (**bold**). If you use an unsupported tag, the message will fail to send.\n\n"
        "Example: python3 jarl_query_db.py <user_id> <jwt> <role> \"SELECT * FROM inventory LIMIT 5\""
    )
    
    messages = [{"role": "user", "content": f"SYSTEM: {system_prompt}\nUSER: {user_text}"}]
    try:
        async with httpx.AsyncClient() as client:
            # IDENTITY VAULT: Sandbox memory by User + Role
            session_id = f"vault_{user_id}_{active_role}"
            agent_payload = {
                "model": AGENT_MODEL, 
                "messages": messages, 
                "tools": AGENT_TOOLS, 
                "tool_choice": "auto",
                "session_id": session_id
            }
            resp = await send_agent_request(client, agent_payload)
            resp.raise_for_status()
            ai_msg = resp.json()["choices"][0]["message"]

            # Prepend role emoji to all AI responses for context awareness
            if ai_msg.get("content"):
                ai_msg["content"] = f"{ROLE_EMOJIS.get(active_role, '👤')} {ai_msg['content']}"

            # 3. INTERCEPTION LOOP
            while ai_msg.get("tool_calls"):
                sanitized_msg = {"role": "assistant", "tool_calls": ai_msg.get("tool_calls")}
                if ai_msg.get("content"): sanitized_msg["content"] = ai_msg.get("content")
                messages.append(sanitized_msg)
                
                for tool_call in ai_msg["tool_calls"]:
                    func_name = tool_call["function"]["name"]
                    args = json.loads(tool_call["function"]["arguments"])
                    
                    # Capture the AI's reasoning trace (the text before the tool call)
                    # This allows OPA to verify if the 'Thought' matches the 'Action'.
                    reasoning_trace = ai_msg.get("content") or f"Executing {func_name}"
                    
                    tool_request = UserRequest(
                        user_id=user_id, 
                        prompt=reasoning_trace, 
                        action="execute_tool", 
                        tool_name=func_name, 
                        tool_args=args, 
                        correlation_id=correlation_id
                    )
                    tool_verdict = await evaluate_request(tool_request, bg_tasks)

                    if tool_verdict.decision in ["ALLOW", "MASK"]:
                        status_msg = f"⚙️ <b>Executing</b>: {func_name}..."
                        if tool_verdict.decision == "MASK": status_msg += " (🛡️ <b>Policy Applied</b>)"
                        await safe_reply(update, status_msg)
                        
                        # Prepare context for the DB Gateway
                        profile = context_store.get_user_profile(user_id)
                        
                        # Integrity: Calculate the hash of the tool logic being used
                        current_tool_hash = None
                        try:
                            with open("/app/tools.py", "rb") as f:
                                current_tool_hash = hashlib.sha256(f.read()).hexdigest()
                        except: pass

                        user_context = {
                            "user_id": user_id,
                            "token": profile.get("token"),
                            "role": profile.get("active_role"),
                            "correlation_id": correlation_id,
                            "tool_hash": current_tool_hash
                        }
                        
                        if func_name == "jarl_query_db": 
                            # 3. INTERCEPTION: Check for Escalation
                            if tool_verdict.decision == "ESCALATE":
                                # Park the request in Redis for HITL
                                context_store.save_pending_escalation(correlation_id, {
                                    "user_id": user_id,
                                    "sql_query": args.get("sql_query"),
                                    "reason": tool_verdict.reason,
                                    "timestamp": datetime.utcnow().isoformat()
                                })
                                await safe_reply(update, f"⚠️ <b>Escalated</b>: {tool_verdict.reason}\nYour request has been parked for administrative review in the ELK console.")
                                result = f"ERROR: Action paused for Human-In-The-Loop review. Correlation ID: {correlation_id}"
                            
                            else:
                                raw_result = await tool_service.query_db(args.get("sql_query", ""), user_context)
                                
                                # 4. ENFORCEMENT: Apply Data Masking if Judge requested it
                                if tool_verdict.decision == "MASK":
                                    result_data = json.loads(raw_result) if isinstance(raw_result, str) else raw_result
                                    # Redaction is handled in db_gate now
                                    result = json.dumps(raw_result)
                                else:
                                    result = raw_result
                        else: 
                            result = f"Error: Unknown tool {func_name}."
                    else:
                        await safe_reply(update, f"🛡️ <b>Blocked</b>: {tool_verdict.reason}")
                        result = f"ERROR: Denied. {tool_verdict.reason}"
                    messages.append({"role": "tool", "tool_call_id": tool_call["id"], "name": func_name, "content": result})

                agent_payload["messages"] = messages
                agent_payload["session_id"] = f"vault_{user_id}_{active_role}"
                resp = await send_agent_request(client, agent_payload)
                resp.raise_for_status()
                ai_msg = resp.json()["choices"][0]["message"]

            ai_text = ai_msg.get("content", "Action complete.")
            if context_store.get_autonomy_mode() == "ENABLED": ai_text = f"🚀 {ai_text}"
            
            # 6. OUTBOUND GATE
            out_verdict = await inspect_response(AgentResponse(user_id=user_id, response_text=ai_text, original_request_id=correlation_id), bg_tasks)
            if out_verdict.decision == "DENY":
                await safe_reply(update, f"🛡️ <b>Blocked</b> (Outbound): {out_verdict.reason}")
                return
            await safe_reply(update, ai_text)
    except Exception as e:
        logger.error(f"PROXY_ERROR: {repr(e)}")
        await safe_reply(update, f"❌ Error: {type(e).__name__}")

async def start_bot():
    if not TELEGRAM_TOKEN: return
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", handle_start))
    application.add_handler(CommandHandler("help", handle_help))
    application.add_handler(CommandHandler("user_help", handle_user_help))
    application.add_handler(CommandHandler("my_roles", handle_my_roles))
    application.add_handler(CommandHandler("switch_role", handle_switch_role))
    application.add_handler(CommandHandler("auth", handle_auth))
    application.add_handler(CommandHandler("unauth", handle_unauth))
    application.add_handler(CommandHandler("purge", handle_purge))
    application.add_handler(CommandHandler("freeze", handle_freeze))
    application.add_handler(CommandHandler("list_users", handle_list_users))
    application.add_handler(CommandHandler("waiting_room", handle_waiting_room))
    application.add_handler(CommandHandler("emergency_stop", handle_emergency_stop))
    application.add_handler(CommandHandler("autonomy", handle_autonomy))
    
    # Callback Handlers
    application.add_handler(CallbackQueryHandler(handle_role_button, pattern="^switch_"))
    application.add_handler(CallbackQueryHandler(handle_auth_confirm, pattern="^auth_yes_"))
    application.add_handler(CallbackQueryHandler(handle_auth_cancel, pattern="^auth_no_"))

    application.add_handler(MessageHandler(filters.COMMAND, handle_unknown_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_telegram_message))
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    logger.info("Bot polling...")

@app.on_event("startup")
async def on_startup():
    asyncio.create_task(start_bot())

@app.post("/evaluate", response_model=OPAVerdict)
async def evaluate_request(request: UserRequest, background_tasks: BackgroundTasks):
    try:
        profile = context_store.get_user_profile(request.user_id)
        role = profile.get("active_role") if profile and profile.get("status") == "ACTIVE" else None
        token = profile.get("token") if profile else None
        
        # Pull SQL query from tool args if available
        sql_query = request.tool_args.get("sql_query") if request.tool_args else None
        signals = detector.get_signals(request.prompt, sql_query=sql_query)
        correlation_id = request.correlation_id or str(uuid.uuid4())
        system_status = context_store.get_system_status()
        autonomy_mode = context_store.get_autonomy_mode()
        tool_hash = None
        if request.tool_name == "jarl_query_db":
            try:
                with open("/app/tools.py", "rb") as f:
                    tool_hash = hashlib.sha256(f.read()).hexdigest()
            except: pass
        
        testimony = OPAInput(
            user=UserContext(id=request.user_id, role=role, token=token), 
            request=RequestContext(
                id=correlation_id, 
                timestamp=datetime.utcnow().isoformat() + "Z", 
                action=request.action, 
                tool_name=request.tool_name, 
                tool_args=request.tool_args, 
                tool_hash=tool_hash
            ), 
            signals=signals, 
            context=SystemContext(
                alerts_last_hour=context_store.get_alert_count(request.user_id), 
                session_risk="LOW", 
                system_status=system_status, 
                autonomy_mode=autonomy_mode,
                jwt_secret=JWT_SECRET # Pass the secret from .env for policy evaluation
            )
        )
        verdict = await _send_to_opa(testimony)
        logger.info(f"OPA_DEBUG_INPUT: {json.dumps(testimony.dict())}")
        logger.info(f"OPA_DEBUG_VERDICT: {json.dumps(verdict.dict())}")
        verdict.correlation_id = correlation_id
        
        if verdict.risk_level in ["MEDIUM", "HIGH", "CRITICAL"]: 
            context_store.increment_alert_counter(request.user_id)

        # ENHANCED LOGGING: Scrub nulls for high-fidelity ELK forensics
        audit_entry = {
            "event_id": str(uuid.uuid4()), 
            "correlation_id": correlation_id, 
            "user_id": request.user_id, 
            "username": profile.get("username") if profile else "Anon",
            "user_role": role or "unverified", 
            "action": request.action, 
            "tool": request.tool_name or "CHAT_ONLY", 
            "decision": verdict.decision, 
            "reason": verdict.reason,
            "risk_level": verdict.risk_level,
            "prompt": request.prompt,
            "intent_verb": signals.intent_verb or "UNKNOWN",
            "tool_args": json.dumps(request.tool_args) if request.tool_args else "N/A",
            "mask_columns": json.dumps(verdict.mask_columns) if verdict.mask_columns else "NONE_REDACTED",
            "sql_patch": verdict.sql_patch or "NONE_APPLIED",
            "status": profile.get("status") if profile else "NEW_REQUEST"
        }
        save_audit_log(audit_entry)
        return verdict
    except Exception as e:
        logger.error(f"EVAL_FAIL: {e}")
        return OPAVerdict(decision="DENY", reason="FAIL", risk_level="CRITICAL")

@app.post("/inspect", response_model=OPAVerdict)
async def inspect_response(response: AgentResponse, background_tasks: BackgroundTasks):
    try:
        profile = context_store.get_user_profile(response.user_id)
        role = profile.get("active_role") if profile and profile.get("status") == "ACTIVE" else None
        token = profile.get("token") if profile else None
        correlation_id = response.original_request_id or str(uuid.uuid4())
        system_status = context_store.get_system_status()
        autonomy_mode = context_store.get_autonomy_mode()
        testimony = OPAInput(
            user=UserContext(id=response.user_id, role=role, token=token), 
            request=RequestContext(id=correlation_id, timestamp=datetime.utcnow().isoformat() + "Z", action="inspect_response"), 
            signals=detector.get_signals(response.response_text), 
            context=SystemContext(
                alerts_last_hour=0, 
                session_risk="LOW", 
                system_status=system_status, 
                autonomy_mode=autonomy_mode,
                jwt_secret=JWT_SECRET
            )
        )
        verdict = await _send_to_opa(testimony)
        logger.info(f"OPA_DEBUG_INPUT: {json.dumps(testimony.dict())}")
        logger.info(f"OPA_DEBUG_VERDICT: {json.dumps(verdict.dict())}")
        verdict.correlation_id = correlation_id
        # ENHANCED LOGGING: Scrub nulls and include real-time status for ELK forensics
        save_audit_log({
            "event_id": str(uuid.uuid4()), 
            "correlation_id": correlation_id, 
            "user_id": response.user_id, 
            "username": profile.get("username") if profile else "Anon", 
            "user_role": role or "unverified", 
            "action": "inspect_response", 
            "decision": verdict.decision, 
            "reason": verdict.reason,
            "status": profile.get("status") if profile else "ACTIVE"
        })
        return verdict
    except Exception as e:
        return OPAVerdict(decision="DENY", reason="FAIL", risk_level="CRITICAL")

async def _send_to_opa(testimony: OPAInput) -> OPAVerdict:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(OPA_URL, json={"input": testimony.dict()}, timeout=5.0)
            result = response.json().get("result")
            if not result: return OPAVerdict(decision="DENY", reason="FAIL", risk_level="CRITICAL")
            return OPAVerdict(**result)
    except: return OPAVerdict(decision="DENY", reason="FAIL", risk_level="CRITICAL")

# --- BREAK-GLASS API (ELK Console Integration) ---

class BreakGlassRequest(BaseModel):
    secret: str
    target_id: str
    roles: str | None = None

@app.get("/api/admin/break-glass/auth")
@app.post("/api/admin/break-glass/auth")
async def break_glass_auth(
    secret: str | None = None, 
    target_id: str | None = None, 
    roles: str | None = None,
    request: BreakGlassRequest | None = None
):
    """Emergency Authorization. Supports GET (Kibana) and POST (API)."""
    # 1. Parameter Extraction (Handle GET vs POST safely)
    eff_secret = secret or (request.secret if request else None)
    eff_id = target_id or (request.target_id if request else None)
    eff_roles = roles or (request.roles if request else "guest")

    if not eff_secret or not eff_id:
        raise HTTPException(status_code=400, detail="Missing secret or target_id")

    if eff_secret != EMERGENCY_SECRET:
        raise HTTPException(status_code=401, detail="Invalid Emergency Secret")
    
    # STRICT VALIDATION: Check if enrollment exists
    target_profile = context_store.get_user_profile(eff_id)
    if not target_profile:
        # We allow creating a profile if it doesn't exist, but we log it as an 'External Provision'
        target_profile = {"id": eff_id, "username": "External_User", "joined": datetime.utcnow().isoformat()}
    
    target_profile["status"] = "ACTIVE"
    role_list = eff_roles.lower().split(",")
    target_profile["authorized_roles"] = list(set(target_profile.get("authorized_roles", [])).union(set(role_list)))
    
    if "admin" in target_profile["authorized_roles"]:
        target_profile["active_role"] = "admin"
        target_profile["token"] = generate_admin_token(eff_id, "admin")
    else:
        target_profile["active_role"] = target_profile["authorized_roles"][0]

    context_store.save_user_profile(eff_id, target_profile)
    # STATE SYNC LOG: Use target_id so the Registry Transform updates
    log_system_event(eff_id, "break_glass_auth", "ALLOW", f"Emergency Auth: {eff_roles}", status="ACTIVE", username=target_profile.get("username"))
    return {"status": "SUCCESS", "user": target_profile}

@app.get("/api/admin/break-glass/purge")
@app.post("/api/admin/break-glass/purge")
async def break_glass_purge(
    secret: str | None = None, 
    target_id: str | None = None, 
    request: BreakGlassRequest | None = None
):
    """Emergency Purge. Supports GET (Kibana) and POST (API)."""
    eff_secret = secret or (request.secret if request else None)
    eff_id = target_id or (request.target_id if request else None)

    if not eff_secret or not eff_id:
        raise HTTPException(status_code=400, detail="Missing secret or target_id")

    if eff_secret != EMERGENCY_SECRET:
        raise HTTPException(status_code=401, detail="Invalid Emergency Secret")
    
    profile = context_store.get_user_profile(eff_id)
    if not profile:
        raise HTTPException(status_code=404, detail=f"User {eff_id} not found.")
    
    context_store.r.delete(f"profile:{eff_id}")
    log_system_event(eff_id, "break_glass_purge", "ALLOW", "Emergency Purge via ELK", status="PURGED", username=profile.get("username"))
    return {"status": "SUCCESS", "message": f"User {eff_id} physically removed."}

@app.get("/api/admin/break-glass/freeze")
@app.post("/api/admin/break-glass/freeze")
async def break_glass_freeze(
    secret: str | None = None, 
    target_id: str | None = None, 
    request: BreakGlassRequest | None = None
):
    """Emergency Freeze/Unfreeze. Supports GET (Kibana) and POST (API)."""
    eff_secret = secret or (request.secret if request else None)
    eff_id = target_id or (request.target_id if request else None)

    if not eff_secret or not eff_id:
        raise HTTPException(status_code=400, detail="Missing secret or target_id")

    if eff_secret != EMERGENCY_SECRET:
        raise HTTPException(status_code=401, detail="Invalid Emergency Secret")
    
    profile = context_store.get_user_profile(eff_id)
    if not profile:
        raise HTTPException(status_code=404, detail="User not found")
    
    current_status = profile.get("status")
    new_status = "FROZEN" if current_status != "FROZEN" else "ACTIVE"
    profile["status"] = new_status
    context_store.save_user_profile(eff_id, profile)
    log_system_event(eff_id, "break_glass_freeze", "ALLOW", f"User status set to {new_status}", status=new_status, username=profile.get("username"))
    return {"status": "SUCCESS", "new_status": new_status}

@app.get("/api/admin/break-glass/resolve")
@app.post("/api/admin/break-glass/resolve")
async def break_glass_resolve(
    secret: str | None = None, 
    correlation_id: str | None = None, 
    decision: str | None = None, 
    request: EscalationResolution | None = None
):
    """Emergency HITL Resolution. Supports GET (Kibana) and POST (API)."""
    eff_secret = secret or (request.admin_secret if request else None)
    eff_cid = correlation_id or (request.correlation_id if request else None)
    eff_decision = decision or (request.decision if request else None)

    if not eff_secret or not eff_cid or not eff_decision:
        raise HTTPException(status_code=400, detail="Missing secret, correlation_id, or decision")

    if eff_secret != EMERGENCY_SECRET:
        raise HTTPException(status_code=401, detail="Invalid Emergency Secret")
    
    # 1. STRICT VALIDATION: Verify the task exists in the HITL queue
    task = context_store.get_pending_escalation(eff_cid)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task {eff_cid} not found or already resolved.")

    # 2. Resolve in Redis (allows the waiting tool-call to proceed)
    context_store.resolve_escalation(eff_cid)
    context_store.r.set(f"hitl:resolution:{eff_cid}", eff_decision, ex=300)

    # 3. STATE SYNC LOG: Emit a log with the SAME correlation_id to satisfy the Transform pivot
    save_audit_log({
        "event_id": str(uuid.uuid4()),
        "correlation_id": eff_cid,
        "user_id": task.get("user_id", "ADMIN_ACTION"),
        "action": "hitl_resolution",
        "decision": eff_decision,
        "reason": "Administrative override via ELK Witness",
        "status": "RESOLVED",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    })

    return {"status": "SUCCESS", "correlation_id": eff_cid}

@app.post("/resolve", response_model=EscalationResponse)
async def resolve_escalation(resolution: EscalationResolution):
    """Standard HITL Resolution (Telegram/Admin-only)."""
    # 1. Verify Admin Identity
    if not is_active_admin(resolution.user_id):
         return EscalationResponse(status="DENIED", message="Unauthorized: Admin role required.")

    # 2. Process Decision
    context = context_store.get_pending_escalation(resolution.correlation_id)
    if not context:
        return EscalationResponse(status="ERROR", message="Escalation not found or expired.")

    # 3. Finalize
    profile = context_store.get_user_profile(resolution.user_id)
    context_store.resolve_escalation(resolution.correlation_id)
    log_system_event(resolution.user_id, "hitl_resolution", resolution.decision, f"Resolved via Telegram: {resolution.correlation_id}", username=profile.get("username") if profile else None)
    
    return EscalationResponse(
        status="SUCCESS", 
        message=f"Action {resolution.decision} for request {resolution.correlation_id}"
    )
