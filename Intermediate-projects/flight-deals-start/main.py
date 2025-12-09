"""Flight Deals Finder - Main Application

This application checks for cheap flights from a home location to destinations
listed in a Google Sheet and sends notifications when deals are found.
"""

import logging
from datetime import datetime, timedelta
from data_manager import DataManager
from flight_data import FlightData
from flight_search import FlightSearch
from notification_manager import NotificationManager

# Configuration
ORIGINAL_LOCATION = "PRG"
DAY_RANGE = 180
CURRENCY = "USD"

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def populate_missing_airport_codes(data_manager, flight_data, destinations):
    """Populate IATA codes for cities that don't have them."""
    logger.info("Checking for missing airport codes...")
    cities_to_update = {}
    
    for destination in destinations:
        if not destination.get("iataCode"):
            city = destination["city"]
            try:
                iata_code = flight_data.get_iataCode(city)
                cities_to_update[city] = iata_code
                logger.info(f"Found IATA code for {city}: {iata_code}")
            except Exception as e:
                logger.error(f"Failed to get IATA code for {city}: {e}")
    
    if cities_to_update:
        try:
            data_manager.populate_airport_code(cities_to_update)
            logger.info(f"Updated {len(cities_to_update)} airport codes")
        except Exception as e:
            logger.error(f"Failed to update airport codes: {e}")
    else:
        logger.info("All cities already have IATA codes")


def search_flights_for_destination(flight_search, destination, start_date, end_date, notification_manager):
    """Search for flights to a single destination and send notifications for deals."""
    city = destination["city"]
    iata_code = destination["iataCode"]
    lowest_price = destination["lowestPrice"]
    
    if not iata_code:
        logger.warning(f"Skipping {city} - no IATA code available")
        return
    
    logger.info(f"Searching flights to {city} ({iata_code})...")
    
    try:
        # Search for the cheapest flight in the date range
        min_price, best_date = flight_search.find_cheapest_flight_in_range(
            destination_code=iata_code,
            start_date=start_date,
            end_date=end_date,
            currency=CURRENCY
        )
        
        if min_price is None:
            logger.warning(f"No flights found for {city}")
            return
        
        logger.info(f"Cheapest flight to {city}: ${min_price} on {best_date}")
        
        # Send notification if price is below threshold
        if min_price < lowest_price:
            logger.info(f"Deal found! Price ${min_price} is below threshold ${lowest_price}")
            notification_manager.send_message(
                outbound_location=ORIGINAL_LOCATION,
                outbound_date=best_date,
                inbound_location=iata_code,
                city_name=city,
                price=min_price
            )
        else:
            logger.info(f"No deal - price ${min_price} is above threshold ${lowest_price}")
            
    except Exception as e:
        logger.error(f"Error searching flights to {city}: {e}")


def main():
    """Main application logic."""
    logger.info("Starting Flight Deals Finder...")
    
    try:
        # Initialize services
        data_manager = DataManager()
        flight_data = FlightData()
        flight_search = FlightSearch(ORIGINAL_LOCATION, flight_data.bearer_token)
        notification_manager = NotificationManager()
        
        # Get destination data from Google Sheet
        logger.info("Fetching destination data...")
        destinations = data_manager.get_info()["prices"]
        logger.info(f"Found {len(destinations)} destinations to check")
        
        # Populate missing airport codes
        populate_missing_airport_codes(data_manager, flight_data, destinations)
        
        # Refresh data after potential updates
        destinations = data_manager.get_info()["prices"]
        
        # Calculate date range
        tomorrow = datetime.now() + timedelta(days=1)
        end_date = tomorrow + timedelta(days=DAY_RANGE)
        start_date_str = tomorrow.strftime("%Y-%m-%d")
        end_date_str = end_date.strftime("%Y-%m-%d")
        
        logger.info(f"Searching for flights from {start_date_str} to {end_date_str}")
        
        # Search flights for each destination
        for destination in destinations:
            search_flights_for_destination(
                flight_search,
                destination,
                start_date_str,
                end_date_str,
                notification_manager
            )
        
        logger.info("Flight search completed successfully!")
        
    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()

