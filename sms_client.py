from twilio.rest import Client
from config import config

twilio_config = config["twilio"]

def send_message(msg):
    # Your Account Sid and Auth Token from twilio.com/user/account
    client = Client(twilio_config["account_sid"], twilio_config["auth_token"])

    message = client.messages.create(
        twilio_config["to"],
        body=msg,
        from_=twilio_config["from"])
    return message.sid