class MetaAgent:

    def decide(self, rule_result: str, llm_result: str) -> str:
        if rule_result != "Unknown":
            return rule_result
        return llm_result