class RuleAgent:

    def classify(self, message: str) -> str:
        if "SqlException" in message:
            return "Database"
        if "401" in message or "403" in message:
            return "Authentication"
        if "Timeout" in message:
            return "Infrastructure"
        if "HttpRequestException" in message:
            return "API"
        return "Unknown"