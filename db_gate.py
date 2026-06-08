from fastapi import FastAPI, HTTPException
import asyncpg
import os
import httpx
import logging
import json
from pydantic import BaseModel
from typing import Dict, Any, List

app = FastAPI(title="Policy-Jarl Database Gateway")
logger = logging.getLogger("uvicorn.error")

# Configuration
DB_URL = os.getenv("DB_URL", "postgresql://jarl_admin:jarl_password@db:5432/company_db")
OFFICER_URL = os.getenv("OFFICER_URL", "http://officer:8000/evaluate")

class DBQueryRequest(BaseModel):
    user_id: str
    token: str | None = None
    role: str | None = None
    sql_query: str
    correlation_id: str | None = None
    tool_hash: str | None = None

def mask_data(data: Any, columns_to_mask: List[str]) -> Any:
    """Redacts sensitive columns from the result set."""
    if not isinstance(data, list) or not columns_to_mask:
        return data
    masked_results = []
    for row in data:
        new_row = dict(row) # Convert Record to dict
        for col in columns_to_mask:
            if col in new_row:
                new_row[col] = "REDACTED"
        masked_results.append(new_row)
    return masked_results

@app.post("/query")
async def handle_db_query(request: DBQueryRequest):
    """
    Credential Sequestration Point.
    Asks the Officer for an intelligent verdict before touching the DB.
    """
    
    # 1. Ask the Officer for Intelligence
    eval_payload = {
        "user_id": request.user_id,
        "prompt": "System validation of incoming SQL query.",
        "action": "execute_tool",
        "tool_name": "jarl_query_db",
        "tool_args": {"sql_query": request.sql_query},
        "correlation_id": request.correlation_id
    }

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(OFFICER_URL, json=eval_payload, timeout=10.0)
            verdict = resp.json()
            
            if verdict.get("decision") not in ["ALLOW", "MASK"]:
                logger.warning(f"ACTION_DENIED: {verdict.get('reason')}")
                raise HTTPException(status_code=403, detail=f"Policy Block: {verdict.get('reason')}")
            
            mask_columns = verdict.get("mask_columns", [])
            sql_patch = verdict.get("sql_patch")

    except Exception as e:
        if isinstance(e, HTTPException): raise e
        logger.error(f"OFFICER_CONNECT_FAILURE: {e}")
        raise HTTPException(status_code=500, detail="Security Governance Unreachable")

    # 2. Execution & Masking
    try:
        final_sql = request.sql_query.strip().rstrip(';')
        if sql_patch:
            logger.info(f"DYNAMIC_PATCHING: Applying '{sql_patch}' to query.")
            # If the patch is a LIMIT, it must go at the absolute end
            if "LIMIT" in sql_patch.upper():
                # Remove existing LIMIT if any (crude but effective for thesis proof)
                import re
                final_sql = re.sub(r"LIMIT\s+\d+", "", final_sql, flags=re.IGNORECASE)
                final_sql = f"{final_sql.strip()} {sql_patch}"
            elif "WHERE" in sql_patch.upper():
                if "WHERE" in final_sql.upper():
                    final_sql = f"{final_sql} AND {sql_patch.replace('WHERE ', '')}"
                else:
                    final_sql = f"{final_sql} {sql_patch}"

        conn = await asyncpg.connect(DB_URL)
        rows = await conn.fetch(final_sql)
        await conn.close()
        
        # Apply dynamic masking if instructed
        result_set = [dict(r) for r in rows]
        if mask_columns:
            logger.info(f"DATA_MASKING: Redacting columns {mask_columns}")
            result_set = mask_data(result_set, mask_columns)
            
        return result_set
    except Exception as e:
        logger.error(f"DATABASE_ERROR: {e}")
        raise HTTPException(status_code=400, detail=str(e))
