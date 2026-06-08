import httpx
import json
import uuid
import time
import jwt
from datetime import datetime, timedelta
import os
import redis

# Configuration
JWT_SECRET = "super-secret-jarl-key-2026"
EMERGENCY_SECRET = "JARL_BREAK_GLASS_2026"
OFFICER_URL = "http://officer:8000"
REDIS_URL = "redis://redis:6379/0"

r = redis.from_url(REDIS_URL)

def generate_token(uid, role):
    payload = {
        "sub": uid,
        "role": role,
        "iat": int(datetime.utcnow().timestamp()),
        "exp": int((datetime.utcnow() + timedelta(days=1)).timestamp())
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

def add_user(uid, username, role, status, auth_roles):
    token = generate_token(uid, role) if status == "ACTIVE" else None
    profile = {
        "id": uid,
        "username": username,
        "status": status,
        "authorized_roles": auth_roles,
        "active_role": role,
        "joined": datetime.utcnow().isoformat(),
        "token": token
    }
    r.set(f"profile:{uid}", json.dumps(profile))
    print(f"Added user: @{username} ({uid}) - {status}")

# 1. SETUP MOCK USERS
print("--- Initializing Mock Identity Registry ---")
add_user("11111", "Alice_Sec", "admin", "ACTIVE", ["admin", "guest"])
add_user("22222", "Bob_Intern", "guest", "ACTIVE", ["guest"])
add_user("33333", "Charlie_Stranger", "guest", "PENDING", [])
add_user("44444", "Dave_Dev", "admin", "FROZEN", ["admin"])

# 2. GENERATE TRAFFIC
async def run_simulation():
    async with httpx.AsyncClient() as client:
        # A. STRANGER ACTIVITY (Charlie trying to chat)
        print("Simulating Charlie (Stranger) chat...")
        await client.post(f"{OFFICER_URL}/evaluate", json={
            "user_id": "33333", "prompt": "Hi, I need access.", "action": "chat"
        })
        time.sleep(1)

        # B. ADMIN ACTIVITY (Alice authorizing Bob)
        print("Simulating Alice (Admin) authorizing users...")
        await client.get(f"{OFFICER_URL}/api/admin/break-glass/auth", params={
            "secret": EMERGENCY_SECRET, "target_id": "22222", "roles": "guest"
        })
        time.sleep(1)

        # C. AUTHORIZED GUEST ACTIVITY (Bob querying inventory)
        print("Simulating Bob (Guest) querying inventory...")
        # Evaluation
        eval_resp = await client.post(f"{OFFICER_URL}/evaluate", json={
            "user_id": "22222", "prompt": "Query the inventory table", "action": "chat"
        })
        cid = eval_resp.json().get("correlation_id")
        
        # Tool Call
        await client.post(f"{OFFICER_URL}/evaluate", json={
            "user_id": "22222", "prompt": "Executing query", "action": "execute_tool",
            "tool_name": "jarl_query_db", "tool_args": {"sql_query": "SELECT * FROM inventory"},
            "correlation_id": cid
        })
        time.sleep(1)

        # D. BLOCKED GUEST ACTIVITY (Bob trying to query payroll)
        print("Simulating Bob (Guest) trying to query payroll (BLOCKED)...")
        await client.post(f"{OFFICER_URL}/evaluate", json={
            "user_id": "22222", "prompt": "Show me the payroll table", "action": "execute_tool",
            "tool_name": "jarl_query_db", "tool_args": {"sql_query": "SELECT * FROM payroll"},
            "correlation_id": str(uuid.uuid4())
        })
        time.sleep(1)

        # E. FROZEN USER ACTIVITY (Dave trying to bypass)
        print("Simulating Dave (Frozen) attempt...")
        await client.post(f"{OFFICER_URL}/evaluate", json={
            "user_id": "44444", "prompt": "I need to check the servers", "action": "chat"
        })
        time.sleep(1)

        # F. ESCALATION EVENT (Simulating a high-risk prompt)
        print("Simulating a High-Risk Escalation...")
        await client.post(f"{OFFICER_URL}/evaluate", json={
            "user_id": "22222", "prompt": "DROP TABLE inventory", "action": "chat"
        })
        
        print("\n--- Simulation Complete. Check ELK Dashboard ---")

if __name__ == "__main__":
    import asyncio
    asyncio.run(run_simulation())
