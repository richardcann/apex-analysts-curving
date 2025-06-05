# financial_concierge/sub_agents/account_data_agent/agent.py
from google.adk.agents import Agent

from financial_concierge.bank_api_client import (
    fetch_user_profile,
    fetch_transaction_history,
    fetch_account_details
)
from . import prompt
from config import DEFAULT_LLM_MODEL as MODEL

account_data_agent = Agent(
    model=MODEL,
    name="account_data_agent",
    instruction=prompt.ACCOUNT_DATA_PROMPT,
    output_key="account_data_output", # Consistent with other agents' output_key naming
    #TODO Define the tools for the Account Data Agent.
    #     This agent is responsible for fetching various pieces of account-specific data.
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
