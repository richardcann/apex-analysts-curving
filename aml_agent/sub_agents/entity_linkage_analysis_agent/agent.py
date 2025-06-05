# aml_agent/sub_agents/entity_linkage_analysis_agent/agent.py
from google.adk.agents import Agent
from aml_agent.bank_api_client import (
    check_entity_against_watchlists,
    get_company_director_information,
    # fetch_user_profile # Assuming this is from aml_agent.bank_api_client if needed, or a shared client
)
# If fetch_user_profile is intended to be from financial_concierge or a truly common place:
# from financial_concierge.bank_api_client import fetch_user_profile as fc_fetch_user_profile
# Or if it's defined within aml_agent.bank_api_client (even if copied):
from aml_agent.bank_api_client import fetch_user_profile


from . import prompt
from config import DEFAULT_LLM_MODEL as MODEL

entity_linkage_analysis_agent = Agent(
    model=MODEL,
    name="entity_linkage_analysis_agent",
    instruction=prompt.ENTITY_LINKAGE_ANALYSIS_PROMPT,
    output_key="entity_linkage_analysis_output",
    #TODO Define the tools for the Entity Linkage Analysis Agent.
    #     This agent needs tools to gather information about entities (individuals and companies).
    #     1. Import the necessary functions from `aml_agent.bank_api_client`:
    #        - `check_entity_against_watchlists`
    #        - `get_company_director_information`
    #        - `fetch_user_profile`
    #     2. Create a list containing these imported functions.
    #     Refer to the ADK documentation for how to add tools to an agent.
    #====Start your code here====
    tools=[], # Replace this with the actual list of tools
    #====End your code here====
)
