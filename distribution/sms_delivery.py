"""
This module provides functions for sending SMS alerts.
"""

import os
from twilio.rest import Client
from twilio.base.exceptions import TwilioException

def send_sms_alert(phone_number: str, message: str, twilio_account_sid: str = None, twilio_auth_token: str = None, from_number: str = None) -> dict:
    """
    Sends an SMS alert to the specified phone number.

    Args:
        phone_number: The recipient's phone number (E.164 format, e.g., +1234567890).
        message: The message to be sent.
        twilio_account_sid: Twilio Account SID (optional, uses env var if not provided).
        twilio_auth_token: Twilio Auth Token (optional, uses env var if not provided).
        from_number: Twilio phone number to send from (optional, uses env var if not provided).

    Returns:
        A dictionary containing the message SID and status.

    Raises:
        TwilioException: If an error occurs during SMS sending.
        ValueError: If required credentials are missing.
    """
    # Get credentials from parameters or environment variables
    account_sid = twilio_account_sid or os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = twilio_auth_token or os.getenv('TWILIO_AUTH_TOKEN')
    from_phone = from_number or os.getenv('TWILIO_FROM_NUMBER')
    
    if not all([account_sid, auth_token, from_phone]):
        raise ValueError("Twilio credentials (account_sid, auth_token, from_number) must be provided either as parameters or environment variables")
    
    try:
        client = Client(account_sid, auth_token)
        message_obj = client.messages.create(
            body=message,
            from_=from_phone,
            to=phone_number
        )
        return {
            'sid': message_obj.sid,
            'status': message_obj.status,
            'to': message_obj.to
        }
    except TwilioException as e:
        print(f"Error sending SMS: {e}")
        raise
