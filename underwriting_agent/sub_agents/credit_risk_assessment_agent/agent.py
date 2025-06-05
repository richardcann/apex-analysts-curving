# underwriting_agent/sub_agents/credit_risk_assessment_agent/agent.py
from google.adk.agents import Agent

from underwriting_agent.bank_api_client import (
    get_credit_report,
    perform_fraud_check,
    get_property_valuation,
    assess_business_risk,
    fetch_user_profile,      # For additional PII if needed
    fetch_account_details  # For further account standing context
)
from . import prompt
from config import DEFAULT_LLM_MODEL as MODEL

credit_risk_assessment_agent = Agent(
    model=MODEL,
    name="credit_risk_assessment_agent",
    instruction=prompt.CREDIT_RISK_ASSESSMENT_PROMPT,
    output_key="credit_risk_assessment_output",
    #TODO Define the tools for the Credit Risk Assessment Agent.
    #     This agent is responsible for assessing various aspects of credit risk.
    #     1. Import the necessary functions from `underwriting_agent.bank_api_client`:
    #        - `get_credit_report`
    #        - `perform_fraud_check`
    #        - `get_property_valuation`
    #        - `assess_business_risk`
    #        - `fetch_user_profile` (for additional PII if needed)
    #        - `fetch_account_details` (for further account standing context)
    #     2. Create a list containing these imported functions.
    #     Refer to the ADK documentation for how to add tools to an agent.
    #====Start your code here====
    tools=[], # Replace this with the actual list of tools
    #====End your code here====
)
