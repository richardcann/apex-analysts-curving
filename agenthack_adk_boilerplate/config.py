# config.py
# Shared configuration variables for the project.

import os

API_BASE_URL = os.getenv("MONEYPENNY_API_BASE_URL", "https://api.agenthack.uk/api")
DEFAULT_LLM_MODEL = "gemini-2.5-flash-preview-05-20"


#TODO Generate a Google Maps API key from Google Cloud Console and add it here
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "REPLACE THIS WITH A GOOGLE MAPS API KEY")
