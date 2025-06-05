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

"""Financial coordinator: provide reasonable investment strategies"""

from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

from . import prompt
from .sub_agents.data_analyst import data_analyst_agent
from .sub_agents.account_data_agent import account_data_agent
from .sub_agents.credit_eligibility_agent import credit_eligibility_agent
from .sub_agents.spending_advisor_agent import spending_advisor_agent
from .sub_agents.savings_goal_advisor_agent import savings_goal_advisor_agent
from .sub_agents.faq_agent import faq_agent
from config import DEFAULT_LLM_MODEL as MODEL


financial_coordinator = LlmAgent(
    name="financial_coordinator",
    model=MODEL,
    description=(
        "guide users through a structured process to receive financial "
        "advice by orchestrating a series of expert subagents. help them "
        "analyze a market ticker, develop trading strategies, define "
        "execution plans, and evaluate the overall risk."
    ),
    instruction=prompt.FINANCIAL_COORDINATOR_PROMPT,
    output_key="financial_coordinator_output",
    #TODO Define the tools for the Financial Coordinator.
    #     This coordinator orchestrates various financial sub-agents.
    #     1. Import the `AgentTool` class from `google.adk.tools.agent_tool`.
    #     2. For each imported sub-agent below, create an `AgentTool` instance:
    #        - data_analyst_agent
    #        - account_data_agent
    #        - credit_eligibility_agent
    #        - spending_advisor_agent
    #        - savings_goal_advisor_agent
    #        - faq_agent
    #     3. Assemble these `AgentTool` instances into a list for the `tools` parameter.
    #     Refer to ADK documentation on how to use AgentTool to integrate sub-agents.
    #====Start your code here====
    tools=[], # Replace this with the actual list of AgentTool instances
    #====End your code here====
)

root_agent = financial_coordinator
