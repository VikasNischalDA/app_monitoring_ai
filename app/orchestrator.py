from collections import Counter
import json

class Orchestrator:

    def __init__(self, log_agent, rule_agent, llm_agent, meta_agent, business_agent, email_agent):
        self.log_agent = log_agent
        self.rule_agent = rule_agent
        self.llm_agent = llm_agent
        self.meta_agent = meta_agent
        self.business_agent = business_agent
        self.email_agent = email_agent

    def run(self):
        logs = self.log_agent.fetch_logs()
        log_payload = json.dumps([log.__dict__ for log in logs], indent=2, default=str)
        categories = []

        # for log in logs:
            # rule_result = self.rule_agent.classify(log.message)
        llm_result = self.llm_agent.classify(log_payload)
        #final = self.meta_agent.decide(rule_result, llm_result)
        #categories.append(final)

        summary_count = Counter(categories)

        business_summary = self.business_agent.generate_summary(summary_count)

        self.email_agent.send_email(business_summary)