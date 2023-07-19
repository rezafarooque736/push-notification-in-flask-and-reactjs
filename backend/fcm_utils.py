from typing import Any
import firebase_admin
from firebase_admin import messaging, credentials


class FcmUtils:
    def __init__(self):
        # Initialize Firebase app
        firebase_cred = credentials.Certificate("./serviceAccountKey.json")
        firebase_admin.initialize_app(firebase_cred)

    # send_to_token
    # Send a message to a specific token
    # registration_token: The token to send the message to
    # data: The data to send to the token, should be dictionary
    # example
    def send_to_token(self, registration_token, title, body, data=None):
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            data=data,
            token=registration_token,
        )
        response = messaging.send(message)
        print(response)
        return response

    # send_to_token_multicast
    # Send a message to a specific tokens
    # registration_tokens: The tokens to send the message to
    # data: The data to send to the tokens, should be dictionary
    def send_to_token_multicast(self, registration_tokens, title, body, data=None):
        # registration_tokens has to be a list
        assert isinstance(registration_tokens, list)

        message = messaging.MulticastMessage(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            data=data,
            tokens=registration_tokens,
        )
        response = messaging.send_multicast(message)
        print(response)
        # See the BatchResponse reference documentation
        # for the contents of response.
        return response
