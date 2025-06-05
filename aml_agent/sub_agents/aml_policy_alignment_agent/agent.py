# aml_agent/sub_agents/aml_policy_alignment_agent/agent.py
from google.adk.agents import Agent
from . import prompt
from config import DEFAULT_LLM_MODEL as MODEL

#TODO Define the AML Policy Alignment Agent.
#     This agent is responsible for aligning the findings of other AML sub-agents
#     with the bank's internal AML policies and regulatory requirements.
#     1. Import the `Agent` class from `google.adk.agents`.
#     2. Import the `MODEL` from `config` (already done).
#     3. Import the specific prompt for this agent from `. import prompt` (e.g., `prompt.AML_POLICY_ALIGNMENT_PROMPT`).
#     4. Instantiate the `Agent` with the following parameters:
#        - model: Use the imported `MODEL`.
#        - name: "aml_policy_alignment_agent"
#        - instruction: Use the imported `AML_POLICY_ALIGNMENT_PROMPT`.
#        - output_key: "aml_policy_alignment_output"
#        - tools: This agent does not require any external tools, so pass an empty list `[]`.
#     Assign the instantiated agent to a variable named `aml_policy_alignment_agent`.
#====Start your code here====
# aml_policy_alignment_agent = ... # Your agent definition here
#====End your code here====
