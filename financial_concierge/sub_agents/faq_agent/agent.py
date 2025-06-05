# financial_concierge/sub_agents/faq_agent/agent.py
from google.adk.agents import Agent
# This agent might not need external tools if all knowledge is in the prompt.
# If a search fallback is desired, import: from google.adk.tools import google_search

from . import prompt
from config import DEFAULT_LLM_MODEL as MODEL

faq_agent = Agent(
    model=MODEL,
    name="faq_agent",
    instruction=prompt.FAQ_PROMPT,
    output_key="faq_output",
    #TODO Define the tools for the FAQ Agent.
    #     This agent primarily answers questions based on its prompt.
    #     Consider if it needs any tools:
    #     1. If it should ONLY use its prompt, provide an empty list: `tools=[]`.
    #     2. If it should have a fallback to search for general, non-bank specific questions:
    #        - Import `google_search` from `google.adk.tools`.
    #        - Provide `tools=[google_search]`.
    #        - (The prompt would also need to be updated to instruct the agent when to use search).
    #     For this exercise, decide on one approach and implement it.
    #====Start your code here====
    tools=[], # Replace this with your chosen tools configuration (e.g., [] or [google_search])
    #====End your code here====
)
