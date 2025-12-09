"""Flight Search Module - Handles Amadeus API flight search operations."""

import logging
from datetime import datetime, timedelta
import requests

logger = logging.getLogger(__name__)


class FlightSearch:
    """Handles flight search operations using the Amadeus API."""
    
    def __init__(self, original_location_code, bearer_token):
        """Initialize flight search with origin location and authentication token.
        
        Args:
            original_location_code: IATA code for the origin airport
            bearer_token: Amadeus API bearer token for authentication
        """
        self.bearer_token = bearer_token
        self.base_url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
        self.origin_location_code = original_location_code
        self.headers = {
            "Authorization": f"Bearer {self.bearer_token}"
        }
        
    def find_cheapest_flight(self, destination_code, date, currency="USD", adults=1):
        """Find the cheapest flight for a specific date.
        
        Args:
            destination_code: IATA code for destination airport
            date: Departure date in YYYY-MM-DD format
            currency: Currency code (default: USD)
            adults: Number of adult passengers (default: 1)
            
        Returns:
            float: Minimum flight price, or None if no flights found
        """
        params = {
            "originLocationCode": self.origin_location_code,
            "destinationLocationCode": destination_code,
            "departureDate": date,
            "currencyCode": currency,
            "adults": str(adults),
            "max": 250  # Get more results for better price comparison
        }
        
        try:
            response = requests.get(
                url=self.base_url,
                headers=self.headers,
                params=params,
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json().get("data", [])
            
            if not data:
                logger.warning(f"No flights found for {destination_code} on {date}")
                return None
            
            prices = [float(flight["price"]["total"]) for flight in data]
            min_price = min(prices)
            logger.debug(f"Found {len(prices)} flights, cheapest: ${min_price}")
            return min_price
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            return None
        except (KeyError, ValueError, TypeError) as e:
            logger.error(f"Error parsing flight data: {e}")
            return None
    
    def find_cheapest_flight_in_range(self, destination_code, start_date, end_date, currency="USD"):
        """Find the cheapest flight within a date range by sampling dates.
        
        Instead of checking every single day (180 API calls), this method samples
        key dates throughout the range for efficiency.
        
        Args:
            destination_code: IATA code for destination airport
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            currency: Currency code (default: USD)
            
        Returns:
            tuple: (min_price, best_date) or (None, None) if no flights found
        """
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        total_days = (end - start).days
        
        # Sample strategy: check every 7 days to reduce API calls
        # For 180 days, this means ~26 API calls instead of 180
        sample_interval = 7
        
        min_price = None
        best_date = None
        
        logger.info(f"Sampling dates every {sample_interval} days in range {start_date} to {end_date}")
        
        for day_offset in range(0, total_days, sample_interval):
            check_date = start + timedelta(days=day_offset)
            date_str = check_date.strftime("%Y-%m-%d")
            
            price = self.find_cheapest_flight(destination_code, date_str, currency)
            
            if price is not None:
                if min_price is None or price < min_price:
                    min_price = price
                    best_date = date_str
        
        return min_price, best_date
