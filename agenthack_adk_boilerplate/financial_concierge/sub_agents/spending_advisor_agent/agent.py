# financial_concierge/sub_agents/spending_advisor_agent/agent.py
from google.adk.agents import Agent

from financial_concierge.bank_api_client import (
    fetch_user_profile,
    fetch_transaction_history,
    fetch_account_details
)
from . import prompt
from config import DEFAULT_LLM_MODEL as MODEL

spending_advisor_agent = Agent(
    model=MODEL,
    name="spending_advisor_agent",
    instruction=prompt.SPENDING_ADVISOR_PROMPT,
    output_key="spending_advisor_output",
    #TODO Define the tools for the Spending Advisor Agent.
    #     This agent analyzes spending patterns and provides advice.
    #     1. Import the necessary functions from `financial_concierge.bank_api_client`:
    #        - `fetch_user_profile`
    #        - `fetch_transaction_history`
    #        - `fetch_account_details`
    #     2. Create a list containing these imported functions.
    #     Refer to the ADK documentation for how to add tools to an agent.
    #====Start your code here====
    tools=[], # Replace this with the actual list of tools
    #====End your code here====
)
