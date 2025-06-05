# financial_concierge/sub_agents/credit_eligibility_agent/agent.py
from google.adk.agents import Agent

from financial_concierge.bank_api_client import (
    fetch_user_profile,
    fetch_transaction_history,
    fetch_account_details,
    fetch_credit_card_products
)
from . import prompt
from config import DEFAULT_LLM_MODEL as MODEL

credit_eligibility_agent = Agent(
    model=MODEL,
    name="credit_eligibility_agent",
    instruction=prompt.CREDIT_ELIGIBILITY_PROMPT,
    output_key="credit_eligibility_output",
    #TODO Define the tools for the Credit Eligibility Agent.
    #     This agent assesses credit eligibility and provides credit card recommendations.
    #     1. Import the necessary functions from `financial_concierge.bank_api_client`:
    #        - `fetch_user_profile`
    #        - `fetch_transaction_history` (useful for understanding financial behavior)
    #        - `fetch_account_details`
    #        - `fetch_credit_card_products`
    #     2. Create a list containing these imported functions.
    #     Refer to the ADK documentation for how to add tools to an agent.
    #====Start your code here====
    tools=[], # Replace this with the actual list of tools
    #====End your code here====
)
