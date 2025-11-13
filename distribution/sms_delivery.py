"""
This module provides functions for sending SMS alerts.
"""

from twilio.rest import Client

def send_sms_alert(phone_number: str, message: str) -> None:
    """
    Sends an SMS alert to the specified phone number.

    Args:
        phone_number: The recipient's phone number.
        message: The message to be sent.

    Raises:
        twilio.base.exceptions.TwilioException: If an error occurs during SMS sending.
    """
