import httpx
import os
import logging

logger = logging.getLogger("uvicorn.error")

# --- DB GATEWAY CONFIGURATION ---
DB_GATE_URL = os.getenv("DB_GATE_URL", "http://db-gate:8001/query")

class ToolExecutionService:
    """
    Relays actions to the specialized Database Gateway.
    This service no longer possesses database credentials.
    """

    async def query_db(self, sql_query: str, user_context: dict) -> str:
        """Relays a SQL query to the DB-Gate for final authorization and execution."""
        payload = {
            "user_id": user_context.get("user_id"),
            "token": user_context.get("token"),
            "role": user_context.get("role"),
            "sql_query": sql_query,
            "correlation_id": user_context.get("correlation_id"),
            "tool_hash": user_context.get("tool_hash")
        }

        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(DB_GATE_URL, json=payload, timeout=10.0)
                if resp.status_code == 403:
                    return f"SECURITY_ERROR: {resp.json().get('detail')}"
                resp.raise_for_status()
                return str(resp.json())
        except Exception as e:
            logger.error(f"DB_GATE_RELAY_FAILURE: {e}")
            return f"Gateway Error: {str(e)}"

# --- TOOL DEFINITIONS (OpenAI Format) ---

AGENT_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "jarl_query_db",
            "description": "Execute a SQL query on the corporate database to retrieve or update information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "sql_query": {"type": "string", "description": "The SQL query to execute (e.g., SELECT * FROM inventory)."}
                },
                "required": ["sql_query"]
            }
        }
    }
]
