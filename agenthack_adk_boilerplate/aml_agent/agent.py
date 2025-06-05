# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""AML Coordinator: Orchestrates sub-agents for Anti-Money Laundering analysis."""

from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool 

from . import prompt
from .bank_api_client import fetch_transaction_history # Import the tool
# New AML sub-agent imports will be added here later, e.g.:
# from .sub_agents.transaction_retrieval_agent import transaction_retrieval_agent # Not creating a separate agent for this
from .sub_agents.transaction_pattern_analysis_agent import transaction_pattern_analysis_agent
from .sub_agents.geographic_risk_assessment_agent import geographic_risk_assessment_agent
from .sub_agents.entity_linkage_analysis_agent import entity_linkage_analysis_agent
from .sub_agents.aml_policy_alignment_agent import aml_policy_alignment_agent
from config import DEFAULT_LLM_MODEL as MODEL

aml_coordinator_agent = LlmAgent(
    name="aml_coordinator_agent",
    model=MODEL,
    description=(
        "Coordinates Anti-Money Laundering (AML) analysis by orchestrating specialized sub-agents "
        "to retrieve transaction data, analyze patterns, assess geographic risks, "
        "and align findings with bank AML policies."
    ),
    instruction=prompt.AML_COORDINATOR_PROMPT, # Uses the new AML prompt
    output_key="aml_coordinator_output",
    #TODO Define the tools for the AML Coordinator. This should include:
    #     1. A tool to fetch transaction history directly (hint: it's already imported as fetch_transaction_history).
    #     2. AgentTools for each of the imported sub-agents:
    #        - transaction_pattern_analysis_agent
    #        - geographic_risk_assessment_agent
    #        - entity_linkage_analysis_agent
    #        - aml_policy_alignment_agent
    #     Refer to the ADK documentation for how to add tools and AgentTools.
    #====Start your code here====
    tools=[], # Replace this with the actual list of tools
    #====End your code here====
)

root_agent = aml_coordinator_agent
