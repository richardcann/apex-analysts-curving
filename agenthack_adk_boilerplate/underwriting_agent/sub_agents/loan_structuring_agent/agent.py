# underwriting_agent/sub_agents/loan_structuring_agent/agent.py
from google.adk.agents import Agent

from underwriting_agent.bank_api_client import get_applicable_loan_products_and_rates
from . import prompt
from config import DEFAULT_LLM_MODEL as MODEL

loan_structuring_agent = Agent(
    model=MODEL,
    name="loan_structuring_agent",
    instruction=prompt.LOAN_STRUCTURING_PROMPT,
    output_key="loan_structuring_output",
    #TODO Define the tools for the Loan Structuring Agent.
    #     This agent is responsible for finding applicable loan products and their rates.
    #     1. Import `get_applicable_loan_products_and_rates` from `underwriting_agent.bank_api_client`.
    #     2. Create a list containing this imported function.
    #     Refer to the ADK documentation for how to add tools to an agent.
    #====Start your code here====
    tools=[], # Replace this with the actual list of tools
    #====End your code here====
)
