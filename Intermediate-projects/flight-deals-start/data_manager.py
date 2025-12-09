"""Data Manager Module - Handles Google Sheets operations via Sheety API."""

import os
import logging
from dotenv import load_dotenv
import requests

load_dotenv()
logger = logging.getLogger(__name__)


class DataManager:
    """Manages data operations with Google Sheets through Sheety API."""
    
    def __init__(self):
        """Initialize DataManager with Sheety API credentials."""
        self.sheety_endpoint = "https://api.sheety.co/69f7db387d564a87133246560a716a23/flightDeals/prices"
        self.sheety_auth = os.environ.get("SHEET_AUTH")
        
        if not self.sheety_auth:
            raise ValueError("SHEET_AUTH environment variable not set")
        
        self.sheety_headers = {
            "Authorization": f"Basic {self.sheety_auth}"
        }
    
    def update_data(self, field, value, row):
        """Update a specific field in a row.
        
        Args:
            field: Field name in camelCase (e.g., 'iataCode')
            value: New value for the field
            row: Row ID to update
            
        Returns:
            dict: JSON response from API or None on failure
        """
        url = f"{self.sheety_endpoint}/{row}"
        params = {
            "price": {
                field: value
            }
        }
        
        try:
            response = requests.put(
                url=url,
                json=params,
                headers=self.sheety_headers,
                timeout=10
            )
            response.raise_for_status()
            logger.info(f"Updated row {row}: {field}={value}")
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to update row {row}: {e}")
            return None
    
    def get_info(self):
        """Retrieve all destination data from Google Sheet.
        
        Returns:
            dict: JSON response containing prices data
            
        Raises:
            requests.exceptions.RequestException: If API request fails
        """
        try:
            response = requests.get(
                url=self.sheety_endpoint,
                headers=self.sheety_headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch sheet data: {e}")
            raise
    
    def populate_airport_code(self, cities_and_code):
        """Update IATA codes for multiple cities in the sheet.
        
        Args:
            cities_and_code: Dictionary mapping city names to IATA codes
        """
        if not cities_and_code:
            logger.info("No airport codes to populate")
            return
        
        try:
            data = self.get_info()["prices"]
            
            # Create a lookup dictionary for faster access
            city_to_row = {row["city"]: row["id"] for row in data}
            
            # Update each city's IATA code
            for city, iata_code in cities_and_code.items():
                if city in city_to_row:
                    row_id = city_to_row[city]
                    self.update_data(field="iataCode", value=iata_code, row=row_id)
                else:
                    logger.warning(f"City '{city}' not found in sheet")
                    
        except Exception as e:
            logger.error(f"Error populating airport codes: {e}")
            raise


