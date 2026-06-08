"""
Database Service for Policy-Jarl.
Using Redis as the single source of truth for Identity and State.
"""

import json
import os
from datetime import datetime
from typing import List
import redis

# Redis Configuration
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

class ContextStore:
    """
    Stateful memory for Policy-Jarl.
    Stores request metadata, user profiles, and system-wide state.
    """
    def __init__(self) -> None:
        self.r = redis.from_url(REDIS_URL, decode_responses=True)

    # --- System State (Kill Switch) ---

    def set_system_status(self, active: bool):
        """Toggles the global AI Gateway kill-switch."""
        status = "ACTIVE" if active else "LOCKED"
        self.r.set("system:status", status)

    def get_system_status(self) -> str:
        """Checks if the system is globally LOCKED or ACTIVE."""
        return self.r.get("system:status") or "ACTIVE"

    def set_autonomy_mode(self, enabled: bool):
        """Toggles the 'Free Flow' autonomous mode."""
        status = "ENABLED" if enabled else "DISABLED"
        self.r.set("system:autonomy", status)

    def get_autonomy_mode(self) -> str:
        """Checks if the agent has unrestricted autonomy."""
        return self.r.get("system:autonomy") or "DISABLED"

    # --- Request Context & Escalations ---

    def save_context(self, request_id: str, context: dict, ttl: int = 3600) -> None:
        """Saves request context with a 1-hour expiration."""
        self.r.set(f"context:{request_id}", json.dumps(context), ex=ttl)

    def get_context(self, request_id: str) -> dict | None:
        """Retrieves stored context for a request."""
        data = self.r.get(f"context:{request_id}")
        return json.loads(data) if data else None

    def save_pending_escalation(self, request_id: str, testimony: dict) -> None:
        """Stores a request that requires human approval in the HITL queue."""
        self.r.set(f"hitl:{request_id}", json.dumps(testimony), ex=86400) # 24h TTL

    def get_pending_escalation(self, request_id: str) -> dict | None:
        """Retrieves a pending escalation from the HITL queue."""
        data = self.r.get(f"hitl:{request_id}")
        return json.loads(data) if data else None

    def resolve_escalation(self, request_id: str) -> None:
        """Physically removes a pending escalation after it is resolved."""
        self.r.delete(f"hitl:{request_id}")

    # --- Security Counters ---

    def increment_alert_counter(self, user_id: str) -> int:
        """Increments the 'high risk' alert counter for a user."""
        key = f"alerts:{user_id}"
        count = self.r.incr(key)
        if count == 1:
            self.r.expire(key, 3600)
        return count

    def get_alert_count(self, user_id: str) -> int:
        """Retrieves the current number of active alerts for a user."""
        count = self.r.get(f"alerts:{user_id}")
        return int(count) if count else 0

    # --- IdP: User Profile Management ---

    def save_user_profile(self, user_id: str, profile: dict):
        """Saves or updates a user profile and maintains the username mapping."""
        self.r.set(f"profile:{user_id}", json.dumps(profile))
        if profile.get("username"):
            # Maintain a mapping of lowercase username to ID for ergonomic auth
            username = str(profile["username"]).lower().lstrip("@")
            self.r.set(f"username:{username}", user_id)

    def get_user_profile(self, user_id: str) -> dict | None:
        """Retrieves a user profile from Redis."""
        data = self.r.get(f"profile:{user_id}")
        return json.loads(data) if data else None

    def get_id_by_username(self, username: str) -> str | None:
        """Resolves a Telegram handle to a numeric User ID."""
        username = username.lower().lstrip("@")
        return self.r.get(f"username:{username}")

    def get_all_profiles(self) -> List[dict]:
        """Retrieves all user profiles from Redis."""
        keys = self.r.keys("profile:*")
        profiles = []
        for key in keys:
            data = self.r.get(key)
            if data:
                profiles.append(json.loads(data))
        return profiles

def get_user_role(user_id: str) -> str | None:
    """
    Looks up the role for a given user ID.
    Returns None if the user is unknown (Zero Trust).
    """
    store = ContextStore()
    profile = store.get_user_profile(user_id)
    if profile and profile.get("status") == "ACTIVE":
        return profile.get("role")
    return None

def save_audit_log(entry: dict) -> None:
    """Appends a structured JSON log entry to the audit file."""
    if "timestamp" not in entry:
        entry["timestamp"] = datetime.utcnow().isoformat() + "Z"
        
    with open("audit.log", "a") as f:
        f.write(json.dumps(entry) + "\n")
