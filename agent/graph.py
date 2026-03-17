from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from langgraph.checkpoint.memory import MemorySaver
import config

from agent.state import AgentState
from agent.tools import query_database

tools = [query_database]


DB_SCHEMA = """
DATABASE SCHEMA

Table: BatchMonitoringAlert
Columns:
- Id (bigint, isNullable: false)
- AlertSource (int, isNullable: false)
- FileName (varchar, isNullable: true)
- Message (varchar, isNullable: true)
- DateCreated (datetime, isNullable: false)

Table: DebtorAuthenticationCode
Columns:
- CodeId (int, isNullable: false)
- CodeName (varchar, isNullable: true)

Table: BankChannel
Columns:
- Id (int, isNullable: false)
- BankCode (varchar, isNullable: true)
- ChannelId (int, isNullable: true)

Table: DataSyncBatchExecutionDetail
Columns:
- Id (int, isNullable: false)
- LastStartDate (datetime2, isNullable: false)
- LastEndDate (datetime2, isNullable: false)

Table: ApplicationCorrelation
Columns:
- Id (bigint, isNullable: false)
- CorrelationDescriptor (nvarchar, isNullable: true)
- CorrelationId (nvarchar, isNullable: true)
- SourceSystemId (int, isNullable: true)

Table: Bank
Columns:
- Id (int, isNullable: false)
- BankName (nvarchar, isNullable: true)
- Code (nvarchar, isNullable: true)

Table: Mandate
Columns:
- Id (bigint, isNullable: false)
- ApplicationCorrelationId (bigint, isNullable: false)
- ContractReferenceNumber (nvarchar, isNullable: true)
- CreditorId (int, isNullable: false)
- DateCreated (datetime2, isNullable: false)
- State (int, isNullable: true)

Table: MandateRequest
Columns:
- Id (int, isNullable: false)
- MandateId (bigint, isNullable: true)
- MandateReference (nvarchar, isNullable: true)
- MandateState (int, isNullable: false)
- MandateType (int, isNullable: false)
- MandateInitiationDate (datetime2, isNullable: false)
- ContractPeriod (int, isNullable: false)
- InitialAmount (decimal, isNullable: false)
- InstallmentAmount (decimal, isNullable: false)
- Frequency (int, isNullable: false)
- CollectionDay (int, isNullable: false)
- DebtorFirstName (nvarchar, isNullable: true)
- DebtorSurname (nvarchar, isNullable: true)
- DebtorEmailAddress (nvarchar, isNullable: true)
- DebtorPhoneNumber (nvarchar, isNullable: true)
- DebtorBankAccountNumber (nvarchar, isNullable: true)
- DebtorBranchCode (nvarchar, isNullable: true)
- DebtorIdNumber (nvarchar, isNullable: true)
- DebtorIdentificationType (int, isNullable: false)
- DebtorAuthenticationCode (int, isNullable: false)
- SourceSystemId (int, isNullable: true)
- ApplicationCorrelationId (bigint, isNullable: true)
- DateCreated (datetime2, isNullable: false)

Table: MandateResponse
Columns:
- Id (bigint, isNullable: false)
- HyphenId (nvarchar, isNullable: true)
- OutputJson (nvarchar, isNullable: true)
- ResponseCode (nvarchar, isNullable: true)
- StatusCode (nvarchar, isNullable: true)
- ResponseReceivedOn (datetime2, isNullable: false)
- Reason (nvarchar, isNullable: true)
- MandateRequestId (int, isNullable: true)
- mandateStatusCode (nvarchar, isNullable: true)
- responseSourceCode (nvarchar, isNullable: true)
- ResponseChannelId (nvarchar, isNullable: true)
- ReceivedFromDataSync (bit, isNullable: false)

Table: MandateResponseError
Columns:
- Id (bigint, isNullable: false)
- Code (nvarchar, isNullable: true)
- Field (nvarchar, isNullable: true)
- MandateResponseId (bigint, isNullable: true)
- Message (nvarchar, isNullable: true)

Table: Creditor
Columns:
- Id (int, isNullable: false)
- AccountNumber (nvarchar, isNullable: true)
- AccountType (nvarchar, isNullable: true)
- CompanyCode (nvarchar, isNullable: true)
- CompanyName (nvarchar, isNullable: true)
- CreditorCode (nvarchar, isNullable: true)
- EmailAddress (nvarchar, isNullable: true)
- CompanyShortName (nvarchar, isNullable: true)
- TelephoneNumber (nvarchar, isNullable: true)
- BankShortName (nvarchar, isNullable: true)
- BankUserCode (nvarchar, isNullable: true)
- MandateKey (nvarchar, isNullable: true)

Table: SourceSystem
Columns:
- Id (int, isNullable: false)
- Code (nvarchar, isNullable: true)
- Description (nvarchar, isNullable: true)

Table: BatchRequest
Columns:
- Id (int, isNullable: false)
- BatchJson (ntext, isNullable: true)
- Status (int, isNullable: true)
- TotalNumber (int, isNullable: true)
- TotalSuccess (int, isNullable: true)
- TotalError (int, isNullable: true)
- DateCreated (datetime2, isNullable: true)
- DateUpdated (datetime2, isNullable: true)
- FileName (nvarchar, isNullable: true)
- SourceSystemId (int, isNullable: true)
- BatchId (nvarchar, isNullable: true)
- BatchType (int, isNullable: true)

Table: BatchRequestDetail
Columns:
- Id (int, isNullable: false)
- BatchRequestId (int, isNullable: true)
- RequestJson (nvarchar, isNullable: true)
- ProcessStatus (int, isNullable: true)
- CRNumber (nvarchar, isNullable: true)
- DateCreated (datetime2, isNullable: true)
- DateUpdated (datetime2, isNullable: true)
- SourceSystemId (int, isNullable: true)
- CorrelationId (varchar, isNullable: true)

RELATIONSHIPS

Mandate.ApplicationCorrelationId → ApplicationCorrelation.Id  
Mandate.CreditorId → Creditor.Id  
MandateResponse.MandateRequestId → MandateRequest.Id  
MandateResponseError.MandateResponseId → MandateResponse.Id  
ApplicationCorrelation.SourceSystemId → SourceSystem.Id  
BatchRequest.SourceSystemId → SourceSystem.Id  
BatchRequestDetail.BatchRequestId → BatchRequest.Id
"""

SYSTEM_PROMPT = SystemMessage(
    content=f"""
You are a SQL Server assistant.

Database schema:
{DB_SCHEMA}

Rules:
1. Generate SQL Server compatible queries.
2. Only use tables and columns from schema.
3. If question requires data, call query_database tool.
4. Never hallucinate tables or columns.
5. Use JOIN based on relationships
6. Use TOP instead of LIMIT
7. Do not generate DELETE / UPDATE / DROP
8. Return only SQL
"""
)


llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    api_key=config.OPENAI_API_KEY
)

llm_with_tools = llm.bind_tools(tools)

def chatbot(state: AgentState):
    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

graph_builder = StateGraph(AgentState)

graph_builder.add_node("chatbot", chatbot)

tool_node = ToolNode(tools)
graph_builder.add_node("tools", tool_node)

graph_builder.set_entry_point("chatbot")

graph_builder.add_conditional_edges(
    "chatbot",
    lambda state: "tools" if state["messages"][-1].tool_calls else END
)

graph_builder.add_edge("tools", "chatbot")

memory = MemorySaver()

graph = graph_builder.compile(checkpointer=memory)