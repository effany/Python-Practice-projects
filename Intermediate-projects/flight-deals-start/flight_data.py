"""Flight Data Module - Handles Amadeus API authentication and location lookups."""

import os
import logging
from dotenv import load_dotenv
import requests

load_dotenv()
logger = logging.getLogger(__name__)


class FlightData:
    """Manages Amadeus API authentication and flight data operations."""
    
    def __init__(self):
        """Initialize FlightData with API credentials and obtain access token."""
        self.client_id = os.environ.get("FLIGHT_API_KEY")
        self.client_secret = os.environ.get("FLIGHT_API_SECRET")
        
        if not self.client_id or not self.client_secret:
            raise ValueError("FLIGHT_API_KEY and FLIGHT_API_SECRET environment variables must be set")
        
        self.base_url = "https://test.api.amadeus.com/v1"
        self.bearer_token = self.get_access_token()
        
        if not self.bearer_token:
            raise RuntimeError("Failed to obtain Amadeus API access token")

    def get_access_token(self):
        """Obtain OAuth2 access token from Amadeus API.
        
        Returns:
            str: Bearer token for API authentication, or None on failure
        """
        token_endpoint = f"{self.base_url}/security/oauth2/token"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        
        try:
            response = requests.post(
                url=token_endpoint,
                headers=headers,
                data=data,
                timeout=10
            )
            response.raise_for_status()
            token = response.json()["access_token"]
            logger.info("Successfully obtained Amadeus API access token")
            return token
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get access token: {e}")
            return None
        except KeyError as e:
            logger.error(f"Access token not found in response: {e}")
            return None
    
    def get_iataCode(self, city_name):
        """Get IATA code for a city name.
        
        Args:
            city_name: Name of the city to look up
            
        Returns:
            str: IATA code for the city
            
        Raises:
            ValueError: If no city is found or API request fails
        """
        url = f"{self.base_url}/reference-data/locations/cities"
        headers = {
            "Authorization": f"Bearer {self.bearer_token}"
        }
        params = {
            "keyword": city_name,
            "max": 1
        }
        
        try:
            response = requests.get(
                url=url,
                headers=headers,
                params=params,
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json().get("data", [])
            
            if not data:
                raise ValueError(f"No IATA code found for city: {city_name}")
            
            iata_code = data[0]["iataCode"]
            logger.info(f"Found IATA code for {city_name}: {iata_code}")
            return iata_code
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get IATA code for {city_name}: {e}")
            raise ValueError(f"Could not retrieve IATA code for {city_name}") from e
        except (KeyError, IndexError) as e:
            logger.error(f"Invalid response format when looking up {city_name}: {e}")
            raise ValueError(f"Invalid data received for {city_name}") from e
