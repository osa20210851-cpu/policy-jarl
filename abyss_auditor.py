import httpx
import json
import asyncio
import time
import jwt
import redis
from datetime import datetime, timedelta

# --- CONFIGURATION ---
JWT_SECRET = "super-secret-jarl-key-2026-scientific-32"
OFFICER_URL = "http://localhost:8000"
REDIS_URL = "redis://redis:6379/0"

r = redis.from_url(REDIS_URL, decode_responses=True)

def generate_token(uid, role):
    payload = {"sub": uid, "role": role, "iat": int(datetime.utcnow().timestamp()), "exp": int((datetime.utcnow() + timedelta(days=1)).timestamp())}
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

def sync_user(uid, username, role, status, auth_roles):
    token = generate_token(uid, role)
    profile = {"id": uid, "username": username, "status": status, "authorized_roles": auth_roles, "active_role": role, "joined": datetime.utcnow().isoformat(), "token": token}
    r.set(f"profile:{uid}", json.dumps(profile))

async def test_case(client, case):
    payload = {
        "user_id": case["uid"],
        "prompt": case["prompt"],
        "action": case["action"],
        "tool_name": case["tool"],
        "tool_args": case["args"],
        "correlation_id": f"abyss_{case['id']}"
    }
    
    try:
        resp = await client.post(f"{OFFICER_URL}/evaluate", json=payload, timeout=5.0)
        data = resp.json()
        decision = data.get("decision")
        passed = (decision == case["expected"])
        return passed
    except Exception:
        return False

async def run_abyss():
    print("=== JARL'S ABYSS 2.1: HIGH-FIDELITY ADVERSARIAL AUDIT ===\n")
    # Note: We don't flushall here to keep the profiles synced by the industrial auditor
    
    with open("abyss_gauntlet.json", "r") as f:
        gauntlet = json.load(f)

    # Sync users specific to Abyss (in case they differ)
    users_to_sync = {}
    for c in gauntlet:
        if c["uid"] not in users_to_sync:
            # We derive role from the UID prefix for Abyss (A=admin, H=hr, etc.)
            role_map = {"99": "admin", "55": "hr_analytics", "44": "ops_manager", "33": "finance_analyst", "11": "guest", "66": "data_clerk"}
            role = role_map.get(c["uid"][:2], "guest")
            users_to_sync[c["uid"]] = (c["username"], role)
            
    for uid, (name, role) in users_to_sync.items():
        sync_user(uid, name, role, "ACTIVE", [role])

    results = []
    start_time = time.time()
    
    async with httpx.AsyncClient() as client:
        batch_size = 50
        for i in range(0, len(gauntlet), batch_size):
            batch = gauntlet[i:i+batch_size]
            tasks = [test_case(client, case) for case in batch]
            batch_results = await asyncio.gather(*tasks)
            results.extend(batch_results)
            print(f"Progress: {len(results)}/1000 | Adversarial Resistance: {int(results.count(True)/len(results)*100)}%", end='\r')

    end_time = time.time()
    print("\n\n" + "="*80)
    passed = results.count(True)
    total = len(gauntlet)
    print(f"FINAL ABYSS RESISTANCE SCORE: {passed}/{total} ({int(passed/total*100)}%)")
    print(f"Execution Time: {end_time - start_time:.2f}s")
    print("="*80)

if __name__ == "__main__":
    asyncio.run(run_abyss())

