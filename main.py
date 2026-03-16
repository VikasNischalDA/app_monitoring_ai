import os
from dotenv import load_dotenv

from app.orchestrator import Orchestrator
from app.agents.log_fetch_agent import LogFetchAgent
from app.agents.rule_agent import RuleAgent
from app.agents.llm_agent import LLMAgent
from app.agents.meta_agent import MetaAgent
from app.agents.business_agent import BusinessAgent
from app.agents.email_agent import EmailAgent

load_dotenv()

log_agent = LogFetchAgent(
    app_id=os.getenv("APP_INSIGHTS_APP_ID"),
    api_key=os.getenv("APP_INSIGHTS_API_KEY")
)

rule_agent = RuleAgent()
llm_agent = LLMAgent()
meta_agent = MetaAgent()
business_agent = BusinessAgent()
email_agent = EmailAgent()

orchestrator = Orchestrator(
    log_agent,
    rule_agent,
    llm_agent,
    meta_agent,
    business_agent,
    email_agent
)

orchestrator.run()