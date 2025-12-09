"""Notification Manager Module - Handles sending flight deal notifications via Twilio."""

import os
import logging
from dotenv import load_dotenv
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

load_dotenv()
logger = logging.getLogger(__name__)


class NotificationManager:
    """Manages sending notifications for flight deals via WhatsApp/SMS."""
    
    def __init__(self):
        """Initialize NotificationManager with Twilio credentials."""
        self.account_sid = os.environ.get("ACCOUNT_SID")
        self.auth_token = os.environ.get("AUTH_TOKEN")
        self.from_sender = os.environ.get("TWILIO_FROM", 'whatsapp:+14155238886')
        self.to_receiver = os.environ.get("TWILIO_TO")
        
        if not all([self.account_sid, self.auth_token, self.to_receiver]):
            raise ValueError(
                "ACCOUNT_SID, AUTH_TOKEN, and TWILIO_TO environment variables must be set"
            )
        
        try:
            self.client = Client(self.account_sid, self.auth_token)
            logger.info("Twilio client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Twilio client: {e}")
            raise

    def send_message(self, outbound_location, outbound_date, inbound_location, city_name, price):
        """Send a flight deal notification.
        
        Args:
            outbound_location: IATA code of origin airport
            outbound_date: Departure date in YYYY-MM-DD format
            inbound_location: IATA code of destination airport
            city_name: Name of destination city
            price: Flight price
            
        Returns:
            bool: True if message sent successfully, False otherwise
        """
        message_body = (
            f"✈️ Low price alert! ✈️\n\n"
            f"Only ${price:.2f} to fly from {outbound_location} "
            f"to {city_name} ({inbound_location})\n"
            f"Departure: {outbound_date}\n\n"
            f"Book now!"
        )
        
        try:
            message = self.client.messages.create(
                from_=self.from_sender,
                body=message_body,
                to=self.to_receiver
            )
            logger.info(f"Message sent successfully. SID: {message.sid}")
            return True
            
        except TwilioRestException as e:
            logger.error(f"Twilio API error: {e}")
            return False
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            return False
