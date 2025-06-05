# underwriting_agent/sub_agents/__init__.py
# This file makes sub_agents a Python sub-package.
from .application_intake_agent import application_intake_agent
from .financial_analysis_agent import financial_analysis_agent
from .credit_risk_assessment_agent import credit_risk_assessment_agent
from .loan_structuring_agent import loan_structuring_agent
# etc.

__all__ = [
    "application_intake_agent",
    "financial_analysis_agent",
    "credit_risk_assessment_agent",
    "loan_structuring_agent",
    # etc.
]
