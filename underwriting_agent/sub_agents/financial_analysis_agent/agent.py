# underwriting_agent/sub_agents/financial_analysis_agent/agent.py
from google.adk.agents import Agent
# from google.adk.tools import ReadFileTool

from underwriting_agent.bank_api_client import fetch_transaction_history
from . import prompt
from config import DEFAULT_LLM_MODEL as MODEL

# Explicitly define ReadFileTool if it needs to be in the tools list.
# ADK might make some system tools available without listing.
# If 'read_file' can be called by the LLM without being in this list, this instance isn't strictly needed.
# However, including it makes its availability explicit.
# read_file_tool = ReadFileTool()

financial_analysis_agent = Agent(
    model=MODEL,
    name="financial_analysis_agent",
    instruction=prompt.FINANCIAL_ANALYSIS_PROMPT,
    output_key="financial_analysis_output",
    #TODO Define the tools for the Financial Analysis Agent.
    #     This agent is responsible for analyzing financial data, including transaction history and potentially documents.
    #     1. Import `fetch_transaction_history` from `underwriting_agent.bank_api_client`.
    #     2. Consider if the `read_file` tool is needed for analyzing financial statements or other documents.
    #        If so, include `read_file` directly in the list (it's a system-provided tool).
    #     3. Create a list containing these functions/tools.
    #     Refer to the ADK documentation for how to add tools to an agent.
    #====Start your code here====
    tools=[], # Replace this with the actual list of tools
    #====End your code here====
)
