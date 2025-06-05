# underwriting_agent/agent.py
from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

from . import prompt
from .sub_agents.application_intake_agent import application_intake_agent
from .sub_agents.financial_analysis_agent import financial_analysis_agent
from .sub_agents.credit_risk_assessment_agent import credit_risk_assessment_agent
from .sub_agents.loan_structuring_agent import loan_structuring_agent
from config import DEFAULT_LLM_MODEL as MODEL

underwriting_coordinator_agent = LlmAgent(
    name="underwriting_coordinator_agent",
    model=MODEL,
    description=(
        "Manages the loan application underwriting process for Moneypenny's Bank. "
        "Orchestrates sub-agents to gather information, analyze financials, assess risk, "
        "and formulate loan recommendations for personal, mortgage, and business loans."
    ),
    instruction=prompt.UNDERWRITING_COORDINATOR_PROMPT,
    output_key="underwriting_coordinator_output",
    #TODO Define the tools for the Underwriting Coordinator Agent.
    #     This coordinator orchestrates various underwriting sub-agents.
    #     1. Import the `AgentTool` class from `google.adk.tools.agent_tool`.
    #     2. For each imported sub-agent below, create an `AgentTool` instance:
    #        - application_intake_agent
    #        - financial_analysis_agent
    #        - credit_risk_assessment_agent
    #        - loan_structuring_agent
    #     3. Assemble these `AgentTool` instances into a list for the `tools` parameter.
    #     Refer to ADK documentation on how to use AgentTool to integrate sub-agents.
    #====Start your code here====
    tools=[], # Replace this with the actual list of AgentTool instances
    #====End your code here====
)

root_agent = underwriting_coordinator_agent
