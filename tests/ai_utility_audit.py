import httpx
import json
import asyncio
import time
import uuid

AGENT_URL = "http://agent:8900/v1/chat/completions"

AGENT_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "jarl_query_db",
            "description": "Execute a SQL query on the corporate database to retrieve information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "sql_query": {"type": "string", "description": "The SQL query to execute."}
                },
                "required": ["sql_query"]
            }
        }
    }
]

async def run_utility_test(role, prompt):
    print(f"\n[DEBUG] Testing Role: {role.upper()}")
    print(f"Prompt: '{prompt}'")
    
    async with httpx.AsyncClient() as client:
        # FRESH SESSION ID to bypass any 'hallucinated' suspensions from history
        session_id = f"debug_{uuid.uuid4().hex[:8]}"
        
        system_content = (
            f"ROLE: You are the 'Policy-Jarl' Autonomous BI Analyst for {role.upper()}.\n"
            "MISSION: Your ONLY purpose is to provide data-driven insights from the corporate database.\n"
            "OPERATIONAL CONSTRAINTS:\n"
            "1. DATABASE ACCESS: You MUST use the 'jarl_query_db' tool for ALL data tasks.\n"
            "2. SCHEMA: office_locations, employees, payroll, employee_benefits, performance_reviews, it_assets, inventory, suppliers, projects, project_milestones, vendor_contracts, security_incidents, training_records, client_records, db_audit_logs.\n"
        )
        
        payload = {
            "model": "gemini-3.1-flash-lite-preview",
            "messages": [
                {"role": "user", "content": f"SYSTEM: {system_content}\nUSER: {prompt}"}
            ],
            "tools": AGENT_TOOLS,
            "tool_choice": "auto",
            "session_id": session_id
        }
        
        try:
            resp = await client.post(AGENT_URL, json=payload, timeout=60.0)
            data = resp.json()
            
            ai_msg = data["choices"][0]["message"]
            content = ai_msg.get("content", "")
            tool_calls = ai_msg.get("tool_calls", [])
            
            print(f"🤖 RAW AI CONTENT: {content}")
            if tool_calls:
                print(f"⚙️ TOOL CALLS: {json.dumps(tool_calls, indent=2)}")
            else:
                print("❗ NO TOOL CALL GENERATED.")
            
        except Exception as e:
            print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    asyncio.run(run_utility_test("admin", "Show me the headcount of each department."))
