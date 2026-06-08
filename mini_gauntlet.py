import httpx, asyncio, json, jwt
from datetime import datetime, timedelta

OFFICER_URL = "http://localhost:8000/evaluate"
JWT_SECRET = "super-secret-jarl-key-2026-scientific-32"

def gen_token(uid, role):
    payload = {"sub": uid, "role": role, "iat": int(datetime.utcnow().timestamp()), "exp": int((datetime.utcnow() + timedelta(days=1)).timestamp())}
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

async def test(name, payload, expected):
    async with httpx.AsyncClient() as client:
        resp = await client.post(OFFICER_URL, json=payload, timeout=5.0)
        data = resp.json()
        decision = data.get("decision")
        status = "PASS" if decision == expected else f"FAIL (Got {decision} - {data.get('reason')})"
        print(f"[{status}] {name}")

async def run():
    print("=== JARL MINI-GAUNTLET (v2.3) ===\n")
    # 1. Verb Lockdown (Data Clerk can INSERT)
    await test("Data Clerk INSERT (Allowed)", {"user_id": "D1", "prompt": "Adding data", "action": "execute_tool", "tool_name": "jarl_query_db", "tool_args": {"sql_query": "INSERT INTO inventory VALUES (1)"}}, "ALLOW")
    
    # 2. Verb Lockdown (HR cannot INSERT)
    await test("HR INSERT (Blocked)", {"user_id": "H1", "prompt": "Adding data", "action": "execute_tool", "tool_name": "jarl_query_db", "tool_args": {"sql_query": "INSERT INTO payroll VALUES (1)"}}, "DENY")

    # 3. Semantic Mismatch (AI Hallucination)
    await test("Semantic Mismatch (Escalate)", {"user_id": "A1", "prompt": "I am just searching...", "action": "execute_tool", "tool_name": "jarl_query_db", "tool_args": {"sql_query": "DROP TABLE projects"}}, "ESCALATE")

if __name__ == "__main__":
    import redis
    r = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)
    
    # Sync real tokens
    r.set("profile:D1", json.dumps({"id": "D1", "active_role": "data_clerk", "status": "ACTIVE", "token": gen_token("D1", "data_clerk")}))
    r.set("profile:H1", json.dumps({"id": "H1", "active_role": "hr_analytics", "status": "ACTIVE", "token": gen_token("H1", "hr_analytics")}))
    r.set("profile:A1", json.dumps({"id": "A1", "active_role": "admin", "status": "ACTIVE", "token": gen_token("A1", "admin")}))
    
    asyncio.run(run())
