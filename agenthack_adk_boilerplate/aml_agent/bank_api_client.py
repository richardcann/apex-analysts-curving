# aml_agent/bank_api_client.py
import requests
import json
from typing import Optional, List, Dict, Any
from config import API_BASE_URL, GOOGLE_MAPS_API_KEY # Import from root config

# Alias for clarity within this client, though it uses the shared base URL
AML_API_BASE_URL = API_BASE_URL

def fetch_transaction_history(account_number: str, start_date: str, end_date: str) -> dict:
    """
    Retrieves a list of transactions for the specified account_number within a given date range.
    For AML analysis, this endpoint is expected to return transactions enriched with details like 
    counterparty_name, counterparty_account_number, counterparty_bank_identifier, counterparty_country, 
    transaction_location_latitude, transaction_location_longitude, and is_cash_transaction.
    """
    params = {"start_date": start_date, "end_date": end_date} # Standard parameters for the existing endpoint
    url = f"{AML_API_BASE_URL}/users/{account_number}/transactions"
    print(f"\n=====API Call:======\n{url} (params: {params})\n=================")
    try:
        response = requests.get(url, params=params)
        print(f"Response: {response.status_code}\n=================")
        response.raise_for_status()
        return {"status": "success", "data": response.json()}
    except requests.exceptions.HTTPError as e:
        # Log status code even for HTTP errors before raising or returning
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.status_code}\n=================")
        # Basic error handling, can be expanded like in financial_concierge
        error_message = f"API Error (HTTP {e.response.status_code}): Failed to fetch transaction history."
        try:
            error_details = e.response.json().get("message", e.response.text)
            error_message += f" Details: {error_details}"
        except json.JSONDecodeError:
            error_message += f" Raw: {e.response.text}"
        print(f"API HTTPError in fetch_transaction_history (AML): {error_message}")
        return {"status": "error", "error_message": error_message}
    except requests.exceptions.RequestException as e:
        print(f"API RequestException in fetch_transaction_history (AML): {e}")
        return {"status": "error", "error_message": f"API request failed for transaction history: {e}"}

def fetch_user_profile(account_number: str) -> dict:
    """
    Fetches basic profile information for the user associated with the given account_number.
    This includes full name, email, phone number, address, date of birth, account type, and account open date.

    Args:
        account_number (str): The unique identifier (e.g., "123456789") for the user's bank account.

    Returns:
        dict: A dictionary containing:
              - 'status' (str): "success" or "error".
              - 'data' (dict, optional): The user's profile information if status is "success".
                Example: {'account_number': '123456789', 'full_name': 'Jane Doe', ...}
              - 'error_message' (str, optional): A description of the error if status is "error".
    """
    url = f"{AML_API_BASE_URL}/users/{account_number}/profile"
    print(f"\n=====API Call:======\n{url}\n=================")
    try:
        response = requests.get(url) 
        print(f"Response: {response.status_code}\n=================")
        response.raise_for_status() 
        return {"status": "success", "data": response.json()}
    except requests.exceptions.HTTPError as e:
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.status_code}\n=================")
        try:
            error_response = e.response.json()
            status_code = error_response.get("statusCode", e.response.status_code)
            error_type = error_response.get("error", "Unknown Error Type")
            raw_message = error_response.get("message", "No specific error message provided by API.")
            if isinstance(raw_message, list):
                detailed_messages = "; ".join(raw_message)
            else:
                detailed_messages = raw_message
            error_message_for_agent = f"API Error (HTTP {status_code} - {error_type}): {detailed_messages}"
        except json.JSONDecodeError:
            error_message_for_agent = f"API Error (HTTP {e.response.status_code}): Failed to decode error response. Raw: {e.response.text}"
        print(f"API HTTPError fetching user profile for {account_number} (AML): {error_message_for_agent}")
        return {"status": "error", "error_message": f"Failed to fetch user profile. {error_message_for_agent}"}
    except requests.exceptions.RequestException as e:
        print(f"API RequestException fetching user profile for {account_number} (AML): {e}")
        return {"status": "error", "error_message": f"Failed to fetch user profile. API request failed: {e}"}
    except json.JSONDecodeError as e:
        print(f"API JSONDecodeError for user profile {account_number} (AML): {e}")
        return {"status": "error", "error_message": "Failed to fetch user profile. Invalid JSON response from API."}

def get_account_profile_and_history_summary(account_number: str) -> dict:
    """
    Provides a baseline profile of the account for AML analysis.
    """
    url = f"{AML_API_BASE_URL}/users/{account_number}/aml_profile_summary"
    print(f"\n=====API Call:======\n{url}\n=================")
    try:
        response = requests.get(url)
        print(f"Response: {response.status_code}\n=================")
        response.raise_for_status()
        return {"status": "success", "data": response.json()}
    except Exception as e: 
        # Log status code for HTTP errors if possible, though generic Exception might not have it
        if isinstance(e, requests.exceptions.HTTPError) and hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.status_code}\n=================")
        print(f"API Error in get_account_profile_and_history_summary: {e}")
        return {"status": "error", "error_message": str(e), "data": {
            "account_type": "Unknown", "customer_since": "Unknown", "primary_business_activity": "N/A",
            "expected_monthly_turnover": 0, "avg_transaction_size": 0,
            "typical_counterparty_countries": [], "known_alerts_history_count": 0
        }} # Return default structure on error

def get_country_risk_rating(country_code: str) -> dict:
    """
    Returns the bank's AML risk rating for a given country.
    """
    url = f"{AML_API_BASE_URL}/aml_data/country_risk/{country_code}"
    print(f"\n=====API Call:======\n{url}\n=================")
    try:
        response = requests.get(url)
        print(f"Response: {response.status_code}\n=================")
        response.raise_for_status()
        return {"status": "success", "data": response.json()}
    except Exception as e:
        if isinstance(e, requests.exceptions.HTTPError) and hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.status_code}\n=================")
        print(f"API Error in get_country_risk_rating for {country_code}: {e}")
        return {"status": "error", "error_message": str(e), "data": {"country_code": country_code, "aml_risk_rating": "unknown", "reason_for_rating": "Error fetching data."}}

# get_ip_geolocation_details removed as per user feedback (not using IP address for now)

# get_location_details_from_coordinates removed as per user feedback
# (agent will use a direct Google Maps tool, not a backend-wrapped one)

# Placeholder for a direct geocoding tool function that the agent would call.
# In a real ADK setup, this might be a registered tool that calls Google Maps API directly.
def direct_google_maps_geocoding_tool(latitude: float, longitude: float) -> dict:
    """
    Calls the Google Maps Geocoding API to get address details from latitude and longitude.
    The API key is sourced from config.py.
    """
    if not GOOGLE_MAPS_API_KEY or GOOGLE_MAPS_API_KEY == "YOUR_ACTUAL_GOOGLE_MAPS_API_KEY":
        print("Warning: GOOGLE_MAPS_API_KEY is not set or is a placeholder. Geocoding will be skipped.")
        return {"status": "error", "error_message": "Google Maps API key not configured.", "data": {"country_code": "XX"}}

    maps_api_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "latlng": f"{latitude},{longitude}",
        "key": GOOGLE_MAPS_API_KEY
    }
    # Construct the full URL with query parameters for logging, though requests library handles it
    log_url_with_params = f"{maps_api_url}?latlng={latitude},{longitude}&key=..." # Key placeholder for log
    print(f"\n=====API Call:======\n{log_url_with_params}\n=================")
    try:
        response = requests.get(maps_api_url, params=params)
        print(f"Response: {response.status_code}\n=================")
        response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
        data = response.json()

        if data.get("status") == "OK" and data.get("results"):
            # Extract relevant information
            # The first result is usually the most accurate
            result = data["results"][0]
            formatted_address = result.get("formatted_address")
            country_code = "XX"
            country_name = "Unknown"
            city_name = "Unknown"

            for component in result.get("address_components", []):
                if "country" in component.get("types", []):
                    country_code = component.get("short_name")
                    country_name = component.get("long_name")
                if "locality" in component.get("types", []) or "postal_town" in component.get("types", []):
                    city_name = component.get("long_name")
            
            return {
                "status": "success",
                "data": {
                    "formatted_address": formatted_address,
                    "country_code": country_code,
                    "country": country_name,
                    "city": city_name,
                    "raw_google_response": result # Optional: include for debugging or more detailed parsing
                }
            }
        else:
            error_message = data.get("error_message", f"Geocoding failed with status: {data.get('status')}")
            print(f"Google Maps API Error: {error_message}")
            return {"status": "error", "error_message": error_message, "data": {"country_code": "XX"}}
    
    except requests.exceptions.HTTPError as e:
        # This block is specifically for HTTP errors, status code already printed if response exists
        if hasattr(e, 'response') and e.response is not None:
            # Already printed, but good to have consistent error handling structure
            pass 
        else: # If no response object in exception, print a generic error status for logging
            print(f"Response: Error (No response object)\n=================")
        print(f"HTTPError calling Google Maps API: {e}")
        return {"status": "error", "error_message": f"HTTP error calling Google Maps API: {e}", "data": {"country_code": "XX"}}
    except requests.exceptions.RequestException as e:
        print(f"Response: Error (RequestException)\n=================")
        print(f"RequestException calling Google Maps API: {e}")
        return {"status": "error", "error_message": f"Request to Google Maps API failed: {e}", "data": {"country_code": "XX"}}
    except json.JSONDecodeError as e:
        # Status code would have been printed if successful HTTP call but bad JSON
        print(f"JSONDecodeError parsing Google Maps API response: {e}")
        return {"status": "error", "error_message": "Invalid JSON response from Google Maps API.", "data": {"country_code": "XX"}}
    except Exception as e:
        print(f"Unexpected error in direct_google_maps_geocoding_tool: {e}")
        return {"status": "error", "error_message": f"An unexpected error occurred during geocoding: {e}", "data": {"country_code": "XX"}}

def check_entity_against_watchlists(
    entity_name: str,
    entity_type: str, # Must be 'individual' or 'organization'
    country_of_residence_or_incorporation: Optional[str] = None, # ISO 3166-1 alpha-2
    date_of_birth: Optional[str] = None, # YYYY-MM-DD
    aliases: Optional[List[str]] = None,
    address: Optional[Dict[str, Any]] = None, 
    identification_numbers: Optional[List[Dict[str, str]]] = None
) -> dict:
    """
    Checks an entity against internal and external watchlists/sanctions lists.
    Payload conforms to WatchlistCheckRequestDto.
    """
    payload: Dict[str, Any] = {"entity_name": entity_name, "entity_type": entity_type}
    if country_of_residence_or_incorporation:
        payload["country_of_residence_or_incorporation"] = country_of_residence_or_incorporation
    if date_of_birth:
        payload["date_of_birth"] = date_of_birth
    if aliases:
        payload["aliases"] = aliases
    if address:
        payload["address"] = address
    if identification_numbers:
        payload["identification_numbers"] = identification_numbers
        
    url = f"{AML_API_BASE_URL}/external_services/watchlist_check"
    # Log the payload carefully, especially in debug scenarios.
    # For production, consider what level of detail is appropriate to log.
    print(f"\n=====API Call:======\nURL: {url}\nPayload: {json.dumps(payload)}\n=================")
    try:
        response = requests.post(url, json=payload)
        print(f"Response: {response.status_code}\n=================")
        response.raise_for_status()
        return {"status": "success", "data": response.json()}
    except Exception as e:
        if isinstance(e, requests.exceptions.HTTPError) and hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.status_code}\n=================")
        print(f"API Error in check_entity_against_watchlists for {entity_name}: {e}")
        return {"status": "error", "error_message": str(e), "data": {"entity_name": entity_name, "is_on_watchlist": None, "watchlist_details": []}}

def get_company_director_information(company_registration_id: str, country_code: str) -> dict:
    """
    Fetches company director information for business AML checks.
    """
    params = {"country_code": country_code}
    url = f"{AML_API_BASE_URL}/external_services/company_info/{company_registration_id}/directors"
    print(f"\n=====API Call:======\n{url} (params: {params})\n=================")
    try:
        response = requests.get(url, params=params)
        print(f"Response: {response.status_code}\n=================")
        response.raise_for_status()
        return {"status": "success", "data": response.json()}
    except Exception as e:
        if isinstance(e, requests.exceptions.HTTPError) and hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.status_code}\n=================")
        print(f"API Error in get_company_director_information for {company_registration_id}: {e}")
        return {"status": "error", "error_message": str(e), "data": {"company_name": "Unknown", "directors": []}}

# Note: Other functions from the copied financial_concierge/bank_api_client.py 
# like fetch_user_profile, fetch_account_details, fetch_credit_card_products, 
# savings goal functions etc., have been removed as they are not directly relevant
# to this initial AML agent's core tasks. If any become necessary, they can be
# added back or imported from a truly shared common client library.
