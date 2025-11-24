import requests

####################################
# API Configuration
####################################

def call_api(endpoint: str, params: dict = None) -> dict:
    """Helper function to call the Upbit API."""
    base_url = "https://api.upbit.com/v1"
    url = f"{base_url}{endpoint}"
    headers = {"Accept": "application/json"}

    # Upbit API does not require an API key for public data like ticker and candles.
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()
