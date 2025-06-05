# aml_agent/sub_agents/transaction_pattern_analysis_agent/agent.py
from google.adk.agents import Agent
from aml_agent.bank_api_client import get_account_profile_and_history_summary
from . import prompt
from config import DEFAULT_LLM_MODEL as MODEL

transaction_pattern_analysis_agent = Agent(
    model=MODEL,
    name="transaction_pattern_analysis_agent",
    instruction=prompt.TRANSACTION_PATTERN_ANALYSIS_PROMPT,
    output_key="transaction_pattern_analysis_output",
    #TODO Define the tools for the Transaction Pattern Analysis Agent.
    #     This agent needs a tool to get a summary of the account's profile and history.
    #     1. Import the `get_account_profile_and_history_summary` function from `aml_agent.bank_api_client`.
    #     2. Create a list containing this imported function.
    #     Refer to the ADK documentation for how to add tools to an agent.
    #====Start your code here====
    tools=[], # Replace this with the actual list of tools
    #====End your code here====
)
