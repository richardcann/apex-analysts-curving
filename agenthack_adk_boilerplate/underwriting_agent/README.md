# Moneypenny's Bank - Loan Underwriting Agent

## Overview

The Loan Underwriting Agent automates and manages the loan application underwriting process for Moneypenny's Bank customers. It handles applications for personal home loans, mortgages, and business loans. The `underwriting_coordinator_agent` orchestrates a series of specialized sub-agents to gather information, perform financial and risk analyses, and formulate a loan recommendation.

## Core Functionality

The `underwriting_coordinator_agent` is responsible for:
- Guiding users through the loan application process.
- Collecting initial application details (loan type, amount, purpose, term) and the user's account number.
- Orchestrating sub-agents for identity verification, financial analysis, credit risk assessment, and loan structuring.
- Managing the flow of information between the user and the sub-agents, ensuring critical data such as Personally Identifiable Information (PII), `application_id`, `account_number`, and `loan_type` are passed correctly at each stage.
- Requesting necessary documentation from the user at appropriate stages.
- Providing a final, comprehensive, and descriptive summary of the underwriting decision or recommendation to the user. This summary is based on the detailed message crafted by the `loan_structuring_agent`, which includes positive and negative factors, and a clear decision.

## Sub-Agents Utilized

The `underwriting_coordinator_agent` leverages the following sub-agents:

1.  **`application_intake_agent`**:
    *   Gathers initial loan application details from the customer.
    *   Verifies customer identity using bank records by calling the `fetch_user_profile` and `fetch_account_details` tools (which use existing bank APIs).
    *   Crucially, it extracts all relevant PII from the user's profile and includes this, along with the processed `account_number` and `loan_type`, in its output for use by subsequent agents.
    *   Initiates the loan application in the system by calling the `/api/v1/underwriting/loan_applications` backend API endpoint (via the `create_loan_application` tool in `bank_api_client.py`).
    *   Informs the user about the types of documents they will need to prepare.

2.  **`financial_analysis_agent`**:
    *   Analyzes the applicant's financial health. It receives PII and application details from the coordinator.
    *   Uses the `fetch_transaction_history` tool (which calls an existing bank API) to review the applicant's Moneypenny's Bank transaction history.
    *   Processes user-provided documents (e.g., bank statements from other institutions, payslips, business financial statements) whose text content is passed to it by the coordinator.
    *   Calculates key financial metrics like income, expenses, disposable income, and Debt-to-Income (DTI) ratio.

3.  **`credit_risk_assessment_agent`**:
    *   Assesses the applicant's creditworthiness and associated risks. It receives PII, application details, and financial analysis from the coordinator, prioritizing the use of provided PII.
    *   Uses tools in `bank_api_client.py` to call the following backend API endpoints:
        *   `POST /api/v1/external_services/credit_report` (to fetch external credit reports).
        *   `POST /api/v1/external_services/fraud_check` (to perform fraud checks).
        *   `POST /api/v1/external_services/property_valuation` (for mortgage/secured loans, to evaluate property risk).
        *   `POST /api/v1/external_services/business_risk` (for business loans, to assess business-specific risks).
    *   It is structured to work with real data from these endpoints, though the backend may currently provide mock responses for these.

4.  **`loan_structuring_agent`**:
    *   Based on all preceding analyses (including PII, financial summary, and credit risk assessment received from the coordinator), determines approvable loan amounts.
    *   Uses the `get_applicable_loan_products_and_rates` tool, which calls the `/api/v1/underwriting/applicable_loan_products` backend API endpoint.
    *   Suggests appropriate loan terms and indicative interest rates.
    *   Formulates a final underwriting recommendation (e.g., Approve, Approve with Conditions, Reject), aiming for a definitive outcome rather than defaulting to referral. It can handle scenarios like sub-minimum loan requests for strong applicants by suggesting alternatives or conditional approvals.
    *   Crafts a detailed `message_to_user` that includes a summary of positive factors, areas of consideration (negative factors) as bullet points, the decision, and any terms or conditions.
    *   Can trigger loan offer document generation via the `generate_loan_offer_document` tool, which calls the `/api/v1/underwriting/document_generation/loan_offer` backend API endpoint.

## Bank API Client (`underwriting_agent/bank_api_client.py`)

This module is responsible for all HTTP communications with the backend APIs.
- It contains functions that map to specific backend endpoints for creating applications, fetching statuses, updating documents, retrieving credit reports, performing fraud checks, property valuations, business risk assessments, fetching applicable loan products, and generating loan offer documents.
- Each API-calling function implements standardized logging (for request and response status) and robust error handling.
- The client uses `config.API_BASE_URL` to construct full endpoint URLs.

## Interaction Flow

1.  The user initiates a loan application query with the `underwriting_coordinator_agent`.
2.  The coordinator gathers initial details (`account_number`, loan type, amount, etc.) and delegates to the `application_intake_agent`.
3.  The `application_intake_agent` calls `fetch_user_profile` to get PII, `fetch_account_details`, and then calls the `create_loan_application` API. It returns the `application_id`, PII, and other details to the coordinator.
4.  The coordinator prompts the user to attach necessary documents.
5.  Once documents are provided (as text content), the coordinator passes this data, along with `application_id`, PII, and other relevant details, to the `financial_analysis_agent`.
6.  The financial analysis results, along with `application_id`, `account_number`, `loan_type`, and PII, are passed by the coordinator to the `credit_risk_assessment_agent`. This agent calls various external service APIs (credit report, fraud, etc.).
7.  Finally, all findings (PII, financial summary, credit risk assessment, application details) are passed by the coordinator to the `loan_structuring_agent`. This agent calls the applicable loan products API, formulates a recommendation, and crafts a detailed `message_to_user`.
8.  The `underwriting_coordinator_agent` presents the detailed `message_to_user` (from the `loan_structuring_agent`) and any other key decision details to the user.

## Current Status of Backend Endpoints

As of the latest updates to this agent system, the `underwriting_agent/bank_api_client.py` has been configured to call newly defined backend API endpoints for many of its core operations (loan creation, credit checks, fraud checks, etc.). While the agent code is prepared for these integrations, the backend API endpoints themselves are currently providing **mock responses**. Full end-to-end functionality with real data and services is dependent on the complete implementation of these backend services by the backend development team.
