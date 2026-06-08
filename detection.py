import re
from typing import Optional
from models import SignalContext, SQLSignals

class DetectionService:
    """
    The 'Officer' of the system. 
    Responsible for investigating raw text and generating structured signals.
    """

    def __init__(self) -> None:
        """Initialize detection patterns."""
        all_cmds = [
            "sudo", "rm", "chmod", "cat", "mv", "dd", "wget", "curl",
            "iptables", "ufw", "firewall-cmd", "nft", "systemctl", "reboot"
        ]
        self.short_cmds = [c for c in all_cmds if len(c) <= 3]
        self.long_cmds = [c for c in all_cmds if len(c) > 3]

        self.exact_pattern = re.compile(
            r"\b(?:" + "|".join(all_cmds) + r")\b", 
            re.IGNORECASE
        )
        self.fuzzy_pattern = re.compile(
            "|".join(self.long_cmds),
            re.IGNORECASE
        )

        self.email_pattern = re.compile(
            r"\b\w+@\w+\.\w{2,}\b", 
            re.IGNORECASE
        )

        # Secret Detection (API Keys, Passwords, etc.)
        self.secret_pattern = re.compile(
            r"(?:api[_-]?key|password|secret|token|credential)\s*[:=]\s*[a-zA-Z0-9_-]{16,}",
            re.IGNORECASE
        )

    def _normalize_text(self, text: str) -> str:
        return text.strip().lower()

    def _fuzzy_normalize(self, text: str) -> str:
        return re.sub(r'[^a-zA-Z0-9]', '', text).lower()

    def _check_dangerous_commands(self, text: str) -> tuple[list[str], list[str]]:
        exacts = self.exact_pattern.findall(text)
        compressed = self._fuzzy_normalize(text)
        fuzzies = self.fuzzy_pattern.findall(compressed)
        unique_fuzzies = list(set(fuzzies) - set(exacts))
        return list(set(exacts)), unique_fuzzies

    def _check_pii(self, text: str) -> bool:
        match = self.email_pattern.search(text)
        if match: return True
        return self.secret_pattern.search(text) is not None

    def infer_intent(self, text: str) -> tuple[str, str]:
        """Infers the AI's semantic intent from its reasoning trace."""
        text = text.lower()
        
        # Mappings for intent verbs
        intent_map = {
            "DELETE": ["delete", "remove", "drop", "truncate", "wipe", "clear"],
            "WRITE": ["update", "set", "insert", "change", "modify", "edit"],
            "READ": ["search", "find", "list", "show", "query", "check", "get", "summarize", "read", "reading", "analyze", "review"]
        }
        
        for intent, keywords in intent_map.items():
            for kw in keywords:
                if kw in text:
                    return intent, f"Detected keyword: {kw}"
        
        return "UNKNOWN", "No clear intent keywords found in reasoning."

    def parse_sql(self, sql: str) -> Optional[SQLSignals]:
        """Deconstructs SQL into structural signals for OPA."""
        if not sql: return None
        
        sql_clean = sql.strip().upper()
        verb = sql_clean.split()[0] if sql_clean else None
        
        # Metadata Discovery Detection
        is_metadata = "INFORMATION_SCHEMA" in sql_clean or "PG_CATALOG" in sql_clean
        
        # Extract tables (Simple regex for FROM/JOIN/INTO/UPDATE)
        tables = re.findall(r"(?:FROM|JOIN|INTO|UPDATE)\s+([a-zA-Z0-9_]+)", sql_clean)
        
        # Check for joins
        has_join = "JOIN" in sql_clean
        
        # Check for wildcards
        has_wildcard = "*" in sql_clean
        
        # DDL & Destruction check (Locking down the database configuration)
        destructive_verbs = {
            "DROP", "TRUNCATE", "DELETE", "ALTER", 
            "CREATE", "GRANT", "REVOKE", "REPLACE"
        }
        is_destructive = verb in destructive_verbs
        
        return SQLSignals(
            verb=verb,
            tables=list(set(tables)),
            columns=[], 
            has_join=has_join,
            has_wildcard=has_wildcard,
            is_destructive=is_destructive,
            is_metadata_discovery=is_metadata
        )

    def get_signals(self, text: str, sql_query: str = None) -> SignalContext:
        """Full investigation including fuzzy analysis and structural SQL parsing."""
        normalized = self._normalize_text(text)
        
        found_exacts, found_fuzzies = self._check_dangerous_commands(normalized)
        has_pii = self._check_pii(normalized)
        
        # Structural SQL signals
        sql_signals = self.parse_sql(sql_query) if sql_query else None
        
        # Semantic Intent signals (from the AI reasoning trace)
        intent, logic = self.infer_intent(text)
        
        # Scoring
        score = (len(found_exacts) * 5) + (len(found_fuzzies) * 3) + (5 if has_pii else 0)
        if sql_signals and sql_signals.is_destructive: score += 10

        return SignalContext(
            severity_score=min(score, 10),
            contains_pii=has_pii,
            matches_threat_pattern=found_exacts,
            fuzzy_matches=found_fuzzies,
            is_prompt_injection=False,
            raw_content=text,
            sql=sql_signals,
            intent_verb=intent,
            inferred_intent=logic
        )
