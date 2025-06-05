# underwriting_agent/bank_api_client.py
import requests
import json
from typing import Optional, List, Dict, Any
from config import API_BASE_URL # Import from root config

# UW_BASE_URL can be an alias or directly use API_BASE_URL
UW_API_BASE_URL = API_BASE_URL # Using the shared base URL

def _log_api_call(url: str, method: str, params: Optional[Dict] = None, payload: Optional[Dict] = None):
    log_message = f"\n=====API Call:======\n{method} {url}"
    if params:
        log_message += f"\nParams: {params}"
    if payload:
        try:
            log_message += f"\nPayload: {json.dumps(payload, indent=2)}"
        except TypeError:
            log_message += f"\nPayload: {payload}" # Fallback if not JSON serializable
    log_message += "\n================="
    print(log_message)

def _log_api_response(response: requests.Response):
    print(f"Response Status: {response.status_code}\n=================")

def _handle_api_error(e: requests.exceptions.RequestException, func_name: str, context: str = "") -> dict:
    error_message = f"API request failed in {func_name}"
    if context:
        error_message += f" for {context}"
    
    if isinstance(e, requests.exceptions.HTTPError):
        status_code = e.response.status_code
        error_message = f"API Error (HTTP {status_code}) in {func_name}"
        if context:
            error_message += f" for {context}"
        try:
            error_details = e.response.json().get("message", e.response.text)
            error_message += f". Details: {error_details}"
        except json.JSONDecodeError:
            error_message += f". Raw response: {e.response.text}"
    else: # Other RequestException
        error_message += f". Error: {e}"

    print(f"{error_message} (underwriting_agent)")
    return {"status": "error", "error_message": error_message}

def _handle_json_decode_error(e: json.JSONDecodeError, func_name: str, context: str = "") -> dict:
    error_message = f"Invalid JSON response in {func_name}"
    if context:
        error_message += f" for {context}"
    error_message += f". Error: {e}"
    print(f"{error_message} (underwriting_agent)")
    return {"status": "error", "error_message": error_message}

# --- Existing User/Account functions (logging updated) ---
def fetch_user_profile(account_number: str) -> dict:
    """Fetches basic profile information for the user."""
    url = f"{UW_API_BASE_URL}/users/{account_number}/profile"
    _log_api_call(url, "GET")
    try:
        response = requests.get(url)
        _log_api_response(response)
        response.raise_for_status()
        return {"status": "success", "data": response.json()}
    except requests.exceptions.RequestException as e:
        return _handle_api_error(e, "fetch_user_profile", f"account {account_number}")
    except json.JSONDecodeError as e:
        return _handle_json_decode_error(e, "fetch_user_profile", f"account {account_number}")

def fetch_account_details(account_number: str) -> dict:
    """Fetches comprehensive details about the user's account."""
    url = f"{UW_API_BASE_URL}/users/{account_number}/account_details"
    _log_api_call(url, "GET")
    try:
        response = requests.get(url)
        _log_api_response(response)
        response.raise_for_status()
        return {"status": "success", "data": response.json()}
    except requests.exceptions.RequestException as e:
        return _handle_api_error(e, "fetch_account_details", f"account {account_number}")
    except json.JSONDecodeError as e:
        return _handle_json_decode_error(e, "fetch_account_details", f"account {account_number}")

def fetch_transaction_history(account_number: str, start_date: str, end_date: str) -> dict:
    """Retrieves a list of transactions for the specified account."""
    params = {"start_date": start_date, "end_date": end_date}
    url = f"{UW_API_BASE_URL}/users/{account_number}/transactions"
    _log_api_call(url, "GET", params=params)
    try:
        response = requests.get(url, params=params)
        _log_api_response(response)
        response.raise_for_status()
        return {"status": "success", "data": response.json()}
    except requests.exceptions.RequestException as e:
        return _handle_api_error(e, "fetch_transaction_history", f"account {account_number}")
    except json.JSONDecodeError as e:
        return _handle_json_decode_error(e, "fetch_transaction_history", f"account {account_number}")

# --- Loan Application Management ---
def create_loan_application(account_number: str, loan_type: str, amount_requested: float, purpose: str, term_months: int) -> dict:
    """Initiates a new loan application in the system via backend."""
    url = f"{UW_API_BASE_URL}/api/v1/underwriting/loan_applications"
    payload = {
        "account_number": account_number,
        "loan_type": loan_type,
        "amount_requested": amount_requested,
        "purpose": purpose,
        "term_months": term_months
    }
    _log_api_call(url, "POST", payload=payload)
    try:
        response = requests.post(url, json=payload)
        _log_api_response(response)
        response.raise_for_status()
        return {"status": "success", "data": response.json()}
    except requests.exceptions.RequestException as e:
        return _handle_api_error(e, "create_loan_application")
    except json.JSONDecodeError as e:
        return _handle_json_decode_error(e, "create_loan_application")

def get_loan_application_status(application_id: str) -> dict:
    """Retrieves the current status of an existing loan application."""
    url = f"{UW_API_BASE_URL}/api/v1/underwriting/loan_applications/{application_id}/status"
    _log_api_call(url, "GET")
    try:
        response = requests.get(url)
        _log_api_response(response)
        response.raise_for_status()
        return {"status": "success", "data": response.json()}
    except requests.exceptions.RequestException as e:
        return _handle_api_error(e, "get_loan_application_status", f"application {application_id}")
    except json.JSONDecodeError as e:
        return _handle_json_decode_error(e, "get_loan_application_status", f"application {application_id}")

def update_loan_application_documents(application_id: str, documents: List[Dict[str, str]]) -> dict:
    """Associates uploaded document references with a loan application."""
    url = f"{UW_API_BASE_URL}/api/v1/underwriting/loan_applications/{application_id}/documents"
    payload = {"documents": documents}
    _log_api_call(url, "POST", payload=payload)
    try:
        response = requests.post(url, json=payload)
        _log_api_response(response)
        response.raise_for_status()
        return {"status": "success", "data": response.json()}
    except requests.exceptions.RequestException as e:
        return _handle_api_error(e, "update_loan_application_documents", f"application {application_id}")
    except json.JSONDecodeError as e:
        return _handle_json_decode_error(e, "update_loan_application_documents", f"application {application_id}")

# --- External Service Integrations ---
def get_credit_report(applicant_identifier: Dict[str, Any], consent_given: bool) -> dict:
    """Requests a credit report from a credit bureau via backend."""
    url = f"{UW_API_BASE_URL}/api/v1/external_services/credit_report"
    if not consent_given:
        print("Consent not given for credit report. (underwriting_agent)")
        return {"status": "error", "error_message": "Consent not given for credit report."}
    payload = {
        "applicant_identifier": applicant_identifier,
        "consent_given": consent_given
    }
    _log_api_call(url, "POST", payload=payload)
    try:
        response = requests.post(url, json=payload)
        _log_api_response(response)
        response.raise_for_status()
        return {"status": "success", "data": response.json()}
    except requests.exceptions.RequestException as e:
        return _handle_api_error(e, "get_credit_report")
    except json.JSONDecodeError as e:
        return _handle_json_decode_error(e, "get_credit_report")

def perform_fraud_check(applicant_data: Dict[str, Any], transaction_context: Optional[Dict[str, Any]] = None) -> dict:
    """Performs a fraud check using a fraud detection service via backend."""
    url = f"{UW_API_BASE_URL}/api/v1/external_services/fraud_check"
    payload = {"applicant_data": applicant_data}
    if transaction_context:
        payload["transaction_context"] = transaction_context
    _log_api_call(url, "POST", payload=payload)
    try:
        response = requests.post(url, json=payload)
        _log_api_response(response)
        response.raise_for_status()
        return {"status": "success", "data": response.json()}
    except requests.exceptions.RequestException as e:
        return _handle_api_error(e, "perform_fraud_check")
    except json.JSONDecodeError as e:
        return _handle_json_decode_error(e, "perform_fraud_check")

def get_property_valuation(property_address: Dict[str, str], property_type: str, estimated_value_applicant: Optional[float] = None, purchase_price: Optional[float] = None) -> dict:
    """Obtains a valuation for a property via backend."""
    url = f"{UW_API_BASE_URL}/api/v1/external_services/property_valuation"
    payload = {
        "property_address": property_address,
        "property_type": property_type,
    }
    if estimated_value_applicant is not None:
        payload["estimated_value_applicant"] = estimated_value_applicant
    if purchase_price is not None:
        payload["purchase_price"] = purchase_price
        
    _log_api_call(url, "POST", payload=payload)
    try:
        response = requests.post(url, json=payload)
        _log_api_response(response)
        response.raise_for_status()
        return {"status": "success", "data": response.json()}
    except requests.exceptions.RequestException as e:
        return _handle_api_error(e, "get_property_valuation")
    except json.JSONDecodeError as e:
        return _handle_json_decode_error(e, "get_property_valuation")

def assess_business_risk(business_registration_id: str, country_code: str, financial_summary: Optional[Dict[str, Any]] = None) -> dict:
    """Assesses the risk profile of a business via backend."""
    url = f"{UW_API_BASE_URL}/api/v1/external_services/business_risk"
    payload = {
        "business_registration_id": business_registration_id,
        "country_code": country_code
    }
    if financial_summary:
        payload["financial_summary"] = financial_summary
    _log_api_call(url, "POST", payload=payload)
    try:
        response = requests.post(url, json=payload)
        _log_api_response(response)
        response.raise_for_status()
        return {"status": "success", "data": response.json()}
    except requests.exceptions.RequestException as e:
        return _handle_api_error(e, "assess_business_risk", f"business ID {business_registration_id}")
    except json.JSONDecodeError as e:
        return _handle_json_decode_error(e, "assess_business_risk", f"business ID {business_registration_id}")

# --- Internal Bank Systems (Products, Rates) ---
def get_applicable_loan_products_and_rates(loan_type: str, risk_score: int, dti_ratio: float, loan_amount_requested: float, term_months_requested: int, customer_segment: Optional[str] = None, collateral_type: Optional[str] = None) -> dict:
    """Fetches suitable internal loan products and indicative rates via backend."""
    url = f"{UW_API_BASE_URL}/api/v1/underwriting/applicable_loan_products"
    payload = {
        "loan_type": loan_type,
        "risk_score": risk_score,
        "dti_ratio": dti_ratio,
        "loan_amount_requested": loan_amount_requested,
        "term_months_requested": term_months_requested,
    }
    if customer_segment:
        payload["customer_segment"] = customer_segment
    if collateral_type:
        payload["collateral_type"] = collateral_type
        
    _log_api_call(url, "POST", payload=payload)
    try:
        response = requests.post(url, json=payload)
        _log_api_response(response)
        response.raise_for_status()
        return {"status": "success", "data": response.json()}
    except requests.exceptions.RequestException as e:
        return _handle_api_error(e, "get_applicable_loan_products_and_rates")
    except json.JSONDecodeError as e:
        return _handle_json_decode_error(e, "get_applicable_loan_products_and_rates")

# --- Document Generation Service ---
def generate_loan_offer_document(application_id: str, applicant_details: Dict[str, Any], loan_terms: Dict[str, Any], conditions: List[str], offer_expiry_date: str) -> dict:
    """Generates a loan offer document via backend."""
    url = f"{UW_API_BASE_URL}/api/v1/underwriting/document_generation/loan_offer"
    payload = {
        "application_id": application_id,
        "applicant_details": applicant_details,
        "loan_terms": loan_terms,
        "conditions": conditions,
        "offer_expiry_date": offer_expiry_date
    }
    _log_api_call(url, "POST", payload=payload)
    try:
        response = requests.post(url, json=payload)
        _log_api_response(response)
        response.raise_for_status()
        return {"status": "success", "data": response.json()}
    except requests.exceptions.RequestException as e:
        return _handle_api_error(e, "generate_loan_offer_document", f"application {application_id}")
    except json.JSONDecodeError as e:
        return _handle_json_decode_error(e, "generate_loan_offer_document", f"application {application_id}")
