# underwriting_agent/sub_agents/application_intake_agent/agent.py
from google.adk.agents import Agent
# Assuming read_file is a system tool provided by ADK, not needing explicit import here for definition.
# If it were a custom tool, it would be imported.

# Import API client functions.
# It will try to use the shared ones from financial_concierge first,
# then fall back to stubs defined in underwriting_agent's own bank_api_client.
from underwriting_agent.bank_api_client import (
    fetch_user_profile,
    fetch_account_details,
    create_loan_application
)
# We also need the read_file tool. ADK's AgentEvaluator should make it available if it's a standard tool.
# If it's a custom tool, it would need to be explicitly passed or registered.
# For now, assuming `read_file` is implicitly available or will be added to a shared toolset.

from . import prompt
from config import DEFAULT_LLM_MODEL as MODEL

application_intake_agent = Agent(
    model=MODEL,
    name="application_intake_agent",
    instruction=prompt.APPLICATION_INTAKE_PROMPT,
    output_key="application_intake_output",
    #TODO Define the tools for the Application Intake Agent.
    #     This agent is responsible for gathering initial application data and user information.
    #     1. Import the necessary functions from `underwriting_agent.bank_api_client`:
    #        - `fetch_user_profile`
    #        - `fetch_account_details`
    #        - `create_loan_application`
    #     2. Consider if the `read_file` tool is needed (e.g., for reading uploaded documents).
    #        If so, include `read_file` directly in the list (it's a system-provided tool).
    #     3. Create a list containing these functions/tools.
    #     Refer to the ADK documentation for how to add tools to an agent.
    #====Start your code here====
    tools=[], # Replace this with the actual list of tools
    #====End your code here====
)
