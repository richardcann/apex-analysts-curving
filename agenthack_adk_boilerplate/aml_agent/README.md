# Moneypenny's Bank - AML (Anti-Money Laundering) Agent

## Overview

The AML Agent is designed to assist Moneypenny's Bank in detecting and assessing potential money laundering activities. It analyzes customer transaction data over a specified period to identify suspicious patterns, geographic risks, and risky entity linkages, ultimately aligning these findings with the bank's internal AML policies to produce a comprehensive risk assessment. The `aml_coordinator_agent` orchestrates this process.

## Core Functionality

The `aml_coordinator_agent` is responsible for:
- Receiving requests for AML reviews, including account number and review period.
- Orchestrating a sequence of specialized sub-agents for detailed analysis.
- Managing the flow of data (primarily transaction lists and analysis summaries) between sub-agents.
- Consolidating the findings from all sub-agents.
- Providing a final AML risk assessment and recommended actions based on the `aml_policy_alignment_agent`'s output.

## Sub-Agents Utilized

The `aml_coordinator_agent` leverages the following sub-agents:

1.  **`transaction_pattern_analysis_agent`**:
    *   Receives a list of transactions for an account.
    *   Uses the `get_account_profile_and_history_summary` tool to understand baseline account behavior.
    *   Analyzes transactions for suspicious patterns such as structuring (smurfing), unusual volumes/frequency, rapid fund movements, activities inconsistent with the customer's profile, and high-value cash transactions.
    *   Outputs a list of flagged patterns and an overall pattern risk score.

2.  **`geographic_risk_assessment_agent`**:
    *   Receives a list of transactions.
    *   Determines the country associated with transactions using `counterparty_country` data or by geocoding `latitude` and `longitude` coordinates via the `direct_google_maps_geocoding_tool`.
    *   Uses the `get_country_risk_rating` tool to assess the AML risk of identified countries.
    *   Flags transactions involving high-risk or sanctioned jurisdictions.
    *   Outputs a list of geographically flagged transactions and an overall geographic risk assessment.

3.  **`entity_linkage_analysis_agent`**:
    *   Receives details of the primary account holder and any counterparties of interest (often those flagged by other agents).
    *   Uses the `check_entity_against_watchlists` tool to screen entities against sanctions and high-risk lists.
    *   For business entities, uses the `get_company_director_information` tool to investigate ownership and control structures.
    *   Can use `fetch_user_profile` for counterparties who are also bank customers.
    *   Identifies and reports risky relationships or networks.

4.  **`aml_policy_alignment_agent`**:
    *   Receives the consolidated findings from all other analysis agents.
    *   Evaluates these findings against a simplified version of Moneypenny's Bank's internal AML policies and risk appetite (embedded in its prompt).
    *   Determines an overall AML risk level (e.g., Low, Medium, High, Critical) for the account's activity.
    *   Recommends appropriate actions (e.g., no action, Enhanced Due Diligence (EDD), consider Suspicious Activity Report (SAR) filing).

## Interaction Flow

1.  An AML review is initiated for a specific account and period, triggering the `aml_coordinator_agent`.
2.  The coordinator first uses its `fetch_transaction_history` tool to retrieve all relevant transactions.
3.  The transaction data is then passed (typically in parallel) to the `transaction_pattern_analysis_agent` and the `geographic_risk_assessment_agent`.
4.  Optionally, based on initial findings, the `entity_linkage_analysis_agent` may be invoked with details of suspicious entities.
5.  The outputs from all these analytical sub-agents are collected by the coordinator and passed to the `aml_policy_alignment_agent`.
6.  The `aml_policy_alignment_agent` produces the final risk assessment and recommendation.
7.  The coordinator presents this consolidated output.
