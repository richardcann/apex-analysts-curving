# Moneypenny's Bank - Financial Concierge Agent

## Overview

The Financial Concierge Agent is a comprehensive financial assistant designed for Moneypenny's Bank customers. It acts as a primary interface for users seeking assistance with various personal banking and financial management tasks. The `financial_coordinator_agent` orchestrates a suite of specialized sub-agents to deliver these services.

## Core Functionality

The `financial_coordinator_agent` is responsible for:
- Understanding user requests related to personal finance.
- Delegating tasks to appropriate sub-agents.
- Synthesizing information from sub-agents to provide a cohesive response to the user.
- Guiding users through processes such as understanding spending, checking credit card eligibility, managing savings goals, and obtaining general banking information.
- Potentially offering market data analysis and discussing investment strategies (if those sub-agents are fully integrated).

## Sub-Agents Utilized

The `financial_coordinator_agent` leverages the following sub-agents to perform its tasks:

1.  **`account_data_agent`**:
    *   Fetches and presents user account details, balances, and transaction history.
    *   Helps users understand their spending patterns by categorizing transactions.

2.  **`credit_eligibility_agent`**:
    *   Retrieves available credit card products offered by the bank.
    *   Assesses a user's eligibility for these credit cards based on their financial profile (e.g., income, credit history - mocked).
    *   Provides recommendations for suitable credit card products.

3.  **`spending_advisor_agent`**:
    *   Analyzes a user's spending habits based on their transaction history.
    *   Offers personalized advice and tips for better money management and budgeting.

4.  **`savings_goal_advisor_agent`**:
    *   Assists users in creating, viewing, updating, and deleting savings goals.
    *   Provides advice on achieving these savings goals based on their financial situation.

5.  **`faq_agent`**:
    *   Answers frequently asked questions about Moneypenny's Bank's products, services, policies, and general banking topics.

6.  **`data_analyst_agent`** (from original template, may be used for market analysis):
    *   Intended for analyzing market data for specific tickers.

*(Other sub-agents like `trading_analyst_agent`, `risk_analyst_agent`, `execution_analyst_agent` were part of the original financial advisor template and can be integrated for investment-related advice if required.)*

## Interaction Flow

Typically, a user interacts with the `financial_coordinator_agent`. Based on the user's query, the coordinator determines the intent and routes the request to the relevant sub-agent(s). The sub-agents perform their specialized tasks, potentially using tools to call mock bank APIs, and return their findings to the coordinator, which then formulates the final response for the user.
