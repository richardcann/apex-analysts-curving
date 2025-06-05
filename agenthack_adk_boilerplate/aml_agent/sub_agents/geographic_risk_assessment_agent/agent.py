# aml_agent/sub_agents/geographic_risk_assessment_agent/agent.py
from google.adk.agents import Agent
from aml_agent.bank_api_client import (
    get_country_risk_rating,
    direct_google_maps_geocoding_tool # Use the direct tool placeholder
    # get_ip_geolocation_details is removed as per user feedback
)
from . import prompt
from config import DEFAULT_LLM_MODEL as MODEL

geographic_risk_assessment_agent = Agent(
    model=MODEL,
    name="geographic_risk_assessment_agent",
    instruction=prompt.GEOGRAPHIC_RISK_ASSESSMENT_PROMPT,
    output_key="geographic_risk_assessment_output",
    #TODO Define the tools for the Geographic Risk Assessment Agent.
    #     This agent needs tools to assess risks associated with geographic locations.
    #     1. Import the necessary functions from `aml_agent.bank_api_client`:
    #        - `get_country_risk_rating`
    #        - `direct_google_maps_geocoding_tool`
    #     2. Create a list containing these imported functions.
    #     Refer to the ADK documentation for how to add tools to an agent.
    #====Start your code here====
    tools=[], # Replace this with the actual list of tools
    #====End your code here====
)
