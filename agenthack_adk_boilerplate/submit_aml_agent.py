import requests
import json
import uuid # For generating unique IDs
import os
import time

# --- Configuration ---
TASKS_API_ENDPOINT = "http://localhost:3001/api/external/tasks?teamName=Algo%20Avengers&password=kR8sL2fP&taskNumber=3" # Replace with your actual tasks API URL
ADK_SERVER_BASE_URL = os.getenv("ADK_SERVER_URL", "http://localhost:8000") # ADK server
APP_NAME = "aml_agent"

# --- Helper Functions ---

def generate_unique_id():
    """Generates a unique ID."""
    return uuid.uuid4().hex

def fetch_tasks_from_api():
    """Fetches tasks from the configured API endpoint."""
    print(f"Fetching tasks from: {TASKS_API_ENDPOINT}")
    try:
        response = requests.get(TASKS_API_ENDPOINT, timeout=10)
        response.raise_for_status()
        data = response.json()
        if "tasks" in data and isinstance(data["tasks"], list):
            valid_tasks = [
                task for task in data["tasks"]
                if isinstance(task, dict) and "task_string" in task and "submission_url" in task
            ]
            if not valid_tasks and data["tasks"]: 
                print("Warning: Some tasks in the response had an invalid structure.")
            if not valid_tasks:
                print("No valid tasks found.")
            return valid_tasks
        else:
            print("Error: 'tasks' field not found or not a list in API response.")
            return []
    except requests.exceptions.Timeout:
        print(f"Error fetching tasks: Timeout connecting to {TASKS_API_ENDPOINT}")
        return []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching tasks: {e}")
        return []
    except ValueError as e: # Includes JSONDecodeError
        print(f"Error decoding JSON from tasks API: {e}")
        return []

def create_adk_session(user_id: str, session_id: str):
    """Creates a new session with the ADK server."""
    url = f"{ADK_SERVER_BASE_URL}/apps/{APP_NAME}/users/{user_id}/sessions/{session_id}"
    headers = {"Content-Type": "application/json"}
    payload = {} 

    print(f"\n===== API Call (Create Session): =====\nURL: {url}\n======================================")
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        print(f"Response Status: {response.status_code}")
        print("======================================")
        response.raise_for_status()
        print(f"Session created successfully: userId={user_id}, sessionId={session_id}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error creating ADK session: {e}")
        if e.response is not None:
            print(f"Error Response Body: {e.response.text}")
        return False

def run_adk_turn(user_id: str, session_id: str, task_query: str):
    """Runs a turn (sends a message) in an existing ADK session."""
    url = f"{ADK_SERVER_BASE_URL}/run"
    headers = {"Content-Type": "application/json"}
    payload = {
        "appName": APP_NAME,
        "userId": user_id,
        "sessionId": session_id,
        "newMessage": {
            "role": "user",
            "parts": [{"text": task_query}]
        },
        "streaming": False
    }
    print(f"\n===== API Call (Processing task) =====")
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=300) # Increased timeout for agent processing
        response.raise_for_status()
        return response.json() 
    except requests.exceptions.Timeout:
        print(f"Error running ADK turn: Timeout after 180s for task '{task_query}'")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error running ADK turn: {e}")
        if e.response is not None:
            print(f"Error Response Body: {e.response.text}")
        return None
    except ValueError as e: 
        print(f"Error decoding JSON from ADK /run response: {e}")
        return None


def submit_results_to_api(task_string: str, submission_url: str, conversation_log: dict):
    """Submits the conversation log to the specified submission URL."""
    
    submission_string = ""
    try:
        submission_string = str( conversation_log)
    except:
        print("Unable to parse conversation ,skipping submission")
        return
    
    payload = {
        "answer_string": submission_string
    }
    headers = {"Content-Type": "application/json"}
    print(f"\n===== API Call (Submit Results): =====\nURL: {submission_url}")
    try:
        response = requests.post(submission_url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        print(f"Results for task '{task_string}' submitted successfully.")
    except requests.exceptions.Timeout:
        print(f"Error submitting results for task '{task_string}': Timeout connecting to {submission_url}")
    except requests.exceptions.RequestException as e:
        print(f"Error submitting results for task '{task_string}': {e}")
        if e.response is not None:
            print(f"Error Response Body: {e.response.text}")

# --- Main Execution Logic ---

def main_interaction_loop():
    tasks = fetch_tasks_from_api()
    if not tasks:
        print("No tasks fetched or an error occurred. Exiting.")
        return

    for i, task_item in enumerate(tasks):
        
        # if( i != 1): continue
        
        task_string = task_item["task_string"]
        submission_url = task_item["submission_url"]

        print(f"\n+++++++++++++++++++++++++++ Processing Task {i+1}/{len(tasks)} +++++++++++++++++++++++++++")

        user_id = f"aml_user_{generate_unique_id()[:8]}"
        session_id = f"aml_session_{generate_unique_id()[:12]}"

        if not create_adk_session(user_id, session_id):
            print(f"Failed to create session for task: {task_string}. Skipping.")
            continue
 
        time.sleep(1) 

        conversation_log_from_run = run_adk_turn(user_id, session_id, task_string)

        if conversation_log_from_run:
            submit_results_to_api(task_string, submission_url, conversation_log_from_run)
        else:
            print(f"No conversation log obtained from /run for task: {task_string}. Cannot submit results.")
        
        print("--- Task Complete ---")
        time.sleep(1) # Small delay between tasks

    print("\nAll tasks processed.")

if __name__ == "__main__":
    if TASKS_API_ENDPOINT == "YOUR_TASKS_API_ENDPOINT_HERE":
        print("ERROR: Please configure the TASKS_API_ENDPOINT in the script.")
    else:
        main_interaction_loop()
