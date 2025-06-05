# financial_concierge/bank_api_client.py
import requests
import json
from typing import Optional
from config import API_BASE_URL # Import from root config


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
    try:
        response = requests.get(f"{API_BASE_URL}/users/{account_number}/profile") # Use imported API_BASE_URL
        response.raise_for_status() # Raises an HTTPError for bad responses (4XX or 5XX)
        return {"status": "success", "data": response.json()}
    except requests.exceptions.HTTPError as e:
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
        print(f"API HTTPError fetching user profile for {account_number}: {error_message_for_agent}")
        return {"status": "error", "error_message": f"Failed to fetch user profile. {error_message_for_agent}"}
    except requests.exceptions.RequestException as e:
        print(f"API RequestException fetching user profile for {account_number}: {e}")
        return {"status": "error", "error_message": f"Failed to fetch user profile. API request failed: {e}"}
    except json.JSONDecodeError as e:
        print(f"API JSONDecodeError for user profile {account_number}: {e}")
        return {"status": "error", "error_message": "Failed to fetch user profile. Invalid JSON response from API."}

def fetch_transaction_history(account_number: str, start_date: str, end_date: str) -> dict:
    """
    Retrieves a list of transactions for the specified account_number within a given date range.
    Transactions include details like date, description, amount, currency, and category.

    Args:
        account_number (str): The user's bank account number.
        start_date (str): The start date for the transaction history (YYYY-MM-DD).
        end_date (str): The end date for the transaction history (YYYY-MM-DD).

    Returns:
        dict: A dictionary containing:
              - 'status' (str): "success" or "error".
              - 'data' (list[dict], optional): A list of transaction objects if status is "success".
                Example: [{'transaction_id': 'txn_1', 'date': '2023-01-15', ...}]
              - 'error_message' (str, optional): A description of the error if status is "error".
    """
    params = {"start_date": start_date, "end_date": end_date}
    try:
        response = requests.get(f"{API_BASE_URL}/users/{account_number}/transactions", params=params) # Use imported API_BASE_URL
        response.raise_for_status()
        return {"status": "success", "data": response.json()}
    except requests.exceptions.HTTPError as e:
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
        print(f"API HTTPError fetching transaction history for {account_number}: {error_message_for_agent}")
        return {"status": "error", "error_message": f"Failed to fetch transaction history. {error_message_for_agent}"}
    except requests.exceptions.RequestException as e:
        print(f"API RequestException fetching transaction history for {account_number}: {e}")
        return {"status": "error", "error_message": f"Failed to fetch transaction history. API request failed: {e}"}
    except json.JSONDecodeError as e:
        print(f"API JSONDecodeError for transaction history {account_number}: {e}")
        return {"status": "error", "error_message": "Failed to fetch transaction history. Invalid JSON response from API."}

def fetch_account_details(account_number: str) -> dict:
    """
    Fetches comprehensive details about the user's account associated with the given account_number.
    This includes account type, balance, overdraft limits, and linked products.

    Args:
        account_number (str): The user's bank account number.

    Returns:
        dict: A dictionary containing:
              - 'status' (str): "success" or "error".
              - 'data' (dict, optional): Comprehensive account details if status is "success".
                Example: {'account_number': '123456789', 'current_balance': 5000.00, ...}
              - 'error_message' (str, optional): A description of the error if status is "error".
    """
    try:
        response = requests.get(f"{API_BASE_URL}/users/{account_number}/account_details") # Use imported API_BASE_URL
        response.raise_for_status()
        return {"status": "success", "data": response.json()}
    except requests.exceptions.HTTPError as e:
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
        print(f"API HTTPError fetching account details for {account_number}: {error_message_for_agent}")
        return {"status": "error", "error_message": f"Failed to fetch account details. {error_message_for_agent}"}
    except requests.exceptions.RequestException as e:
        print(f"API RequestException fetching account details for {account_number}: {e}")
        return {"status": "error", "error_message": f"Failed to fetch account details. API request failed: {e}"}
    except json.JSONDecodeError as e:
        print(f"API JSONDecodeError for account details {account_number}: {e}")
        return {"status": "error", "error_message": "Failed to fetch account details. Invalid JSON response from API."}

def fetch_credit_card_products() -> dict:
    """
    Retrieves a list of available credit card products offered by Moneypenny's Bank.
    Each product includes details like name, fees, APR, rewards, and eligibility criteria.

    Returns:
        dict: A dictionary containing:
              - 'status' (str): "success" or "error".
              - 'data' (list[dict], optional): A list of credit card product objects if status is "success".
                Example: [{'product_id': 'MP_REWARDS_CLASSIC', 'name': 'Moneypenny Rewards Classic Card', ...}]
              - 'error_message' (str, optional): A description of the error if status is "error".
    """
    try:
        response = requests.get(f"{API_BASE_URL}/products/credit_cards") # Use imported API_BASE_URL
        response.raise_for_status()
        return {"status": "success", "data": response.json()}
    except requests.exceptions.HTTPError as e:
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
        print(f"API HTTPError fetching credit card products: {error_message_for_agent}")
        return {"status": "error", "error_message": f"Failed to fetch credit card products. {error_message_for_agent}"}
    except requests.exceptions.RequestException as e:
        print(f"API RequestException fetching credit card products: {e}")
        return {"status": "error", "error_message": f"Failed to fetch credit card products. API request failed: {e}"}
    except json.JSONDecodeError as e:
        print(f"API JSONDecodeError for credit card products: {e}")
        return {"status": "error", "error_message": "Failed to fetch credit card products. Invalid JSON response from API."}

# Savings Goals Endpoints

def create_savings_goal(account_number: str, goal_name: str, target_amount: float, target_date: Optional[str] = None, initial_contribution: Optional[float] = None) -> dict:
    """
    Creates a new savings goal for the user.

    Args:
        account_number (str): The user's bank account number.
        goal_name (str): Name of the savings goal (e.g., "Holiday Fund").
        target_amount (float): The target amount to save.
        target_date (str, optional): The target date to achieve the goal (YYYY-MM-DD).
        initial_contribution (float, optional): An initial amount to contribute to the goal.

    Returns:
        dict: A dictionary containing status, goal_id (on success), message, and optionally data of the created goal.
    """
    payload = {
        "goal_name": goal_name,
        "target_amount": target_amount,
    }
    if target_date:
        payload["target_date"] = target_date
    if initial_contribution is not None:
        payload["initial_contribution"] = initial_contribution
    
    try:
        response = requests.post(f"{API_BASE_URL}/users/{account_number}/savings_goals", json=payload) # Use imported API_BASE_URL
        response.raise_for_status()
        return response.json() # Assuming API returns a dict like: {"status": "success", "goal_id": "...", ...}
    except requests.exceptions.HTTPError as e:
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
        print(f"API HTTPError creating savings goal for {account_number}: {error_message_for_agent}")
        return {"status": "error", "error_message": f"Failed to create savings goal. {error_message_for_agent}"}
    except requests.exceptions.RequestException as e:
        print(f"API RequestException creating savings goal for {account_number}: {e}")
        return {"status": "error", "error_message": f"Failed to create savings goal. API request failed: {e}"}
    except json.JSONDecodeError as e:
        print(f"API JSONDecodeError creating savings goal for {account_number}: {e}")
        return {"status": "error", "error_message": "Failed to create savings goal. Invalid JSON response from API."}

def get_savings_goals(account_number: str) -> dict:
    """
    Retrieves all active savings goals for a user.

    Args:
        account_number (str): The user's bank account number.

    Returns:
        dict: A dictionary containing status and a list of savings goal objects in 'data' on success.
    """
    try:
        response = requests.get(f"{API_BASE_URL}/users/{account_number}/savings_goals") # Use imported API_BASE_URL
        response.raise_for_status()
        return response.json() # Assuming API returns a dict like: {"status": "success", "data": [...goals...]}
    except requests.exceptions.HTTPError as e:
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
        print(f"API HTTPError fetching savings goals for {account_number}: {error_message_for_agent}")
        return {"status": "error", "error_message": f"Failed to fetch savings goals. {error_message_for_agent}"}
    except requests.exceptions.RequestException as e:
        print(f"API RequestException fetching savings goals for {account_number}: {e}")
        return {"status": "error", "error_message": f"Failed to fetch savings goals. API request failed: {e}"}
    except json.JSONDecodeError as e:
        print(f"API JSONDecodeError fetching savings goals for {account_number}: {e}")
        return {"status": "error", "error_message": "Failed to fetch savings goals. Invalid JSON response from API."}

def update_savings_goal(account_number: str, goal_id: str, add_contribution: Optional[float] = None, goal_name: Optional[str] = None, target_amount: Optional[float] = None, target_date: Optional[str] = None, status: Optional[str] = None) -> dict:
    """
    Updates an existing savings goal (e.g., add contribution, change name/target/status).

    Args:
        account_number (str): The user's bank account number.
        goal_id (str): The ID of the savings goal to update.
        add_contribution (float, optional): Amount to add to the current savings.
        goal_name (str, optional): New name for the goal.
        target_amount (float, optional): New target amount.
        target_date (str, optional): New target date (YYYY-MM-DD).
        status (str, optional): New status (e.g., "active", "completed", "cancelled").

    Returns:
        dict: A dictionary containing status, message, and optionally the updated goal data.
    """
    payload = {}
    if add_contribution is not None:
        payload["add_contribution"] = add_contribution
    if goal_name:
        payload["goal_name"] = goal_name
    if target_amount is not None:
        payload["target_amount"] = target_amount
    if target_date:
        payload["target_date"] = target_date
    if status:
        payload["status"] = status

    if not payload:
        return {"status": "error", "error_message": "No update information provided for savings goal."}

    try:
        response = requests.put(f"{API_BASE_URL}/users/{account_number}/savings_goals/{goal_id}", json=payload) # Use imported API_BASE_URL
        response.raise_for_status()
        return response.json() # Assuming API returns a dict like: {"status": "success", "data": {...updated_goal...}}
    except requests.exceptions.HTTPError as e:
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
        print(f"API HTTPError updating savings goal {goal_id} for {account_number}: {error_message_for_agent}")
        return {"status": "error", "error_message": f"Failed to update savings goal. {error_message_for_agent}"}
    except requests.exceptions.RequestException as e:
        print(f"API RequestException updating savings goal {goal_id} for {account_number}: {e}")
        return {"status": "error", "error_message": f"Failed to update savings goal. API request failed: {e}"}
    except json.JSONDecodeError as e:
        print(f"API JSONDecodeError updating savings goal {goal_id} for {account_number}: {e}")
        return {"status": "error", "error_message": "Failed to update savings goal. Invalid JSON response from API."}

def delete_savings_goal(account_number: str, goal_id: str) -> dict:
    """
    Deletes a specific savings goal for a user.

    Args:
        account_number (str): The user's bank account number.
        goal_id (str): The ID of the savings goal to delete.

    Returns:
        dict: A dictionary containing status and message.
    """
    try:
        response = requests.delete(f"{API_BASE_URL}/users/{account_number}/savings_goals/{goal_id}") # Use imported API_BASE_URL
        response.raise_for_status()
        if response.status_code == 204: # Handle 204 No Content specifically
            return {"status": "success", "message": "Savings goal deleted successfully."}
        # For other success codes (like 200 with a body), try to parse JSON
        return response.json()
    except requests.exceptions.HTTPError as e:
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
        print(f"API HTTPError deleting savings goal {goal_id} for {account_number}: {error_message_for_agent}")
        return {"status": "error", "error_message": f"Failed to delete savings goal. {error_message_for_agent}"}
    except requests.exceptions.RequestException as e:
        print(f"API RequestException deleting savings goal {goal_id} for {account_number}: {e}")
        return {"status": "error", "error_message": f"Failed to delete savings goal. API request failed: {e}"}
    except json.JSONDecodeError as e:
        # This handles cases where a 2xx response (other than 204) doesn't have valid JSON
        print(f"API JSONDecodeError on successful delete for goal {goal_id} (account {account_number}): {e}")
        return {"status": "error", "error_message": "Savings goal deletion response was not valid JSON."}
