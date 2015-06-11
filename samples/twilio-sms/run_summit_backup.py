"""
This sample application sends an SMS message to a recipient via a POST request.
Similar to Twilio's example, but uses the Summit API as a fallback if the
Twilio request fails.

To test, create a config file with account information in config.ini:
-------------------------------------------------------------------------------
[Twilio]
account_sid: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
auth_token: YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY
from_number: +15555555555

[Summit]
account_sid: AAAAAAAAAAAAAAAAAAAAAAAA
auth_token: BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
from_number: +14145551234
-------------------------------------------------------------------------------

Start the Flask application:
    python run_summit_backup.py

Send a request from the command-line using curl:
    curl -X POST --data "<message>" localhost:5000/sms/<recipient phone #>
"""

import ConfigParser
from flask import Flask, jsonify, request
import json

from summit.rest import SummitRestClient
from twilio import TwilioRestException
from twilio.rest import TwilioRestClient


app = Flask(__name__)
config = ConfigParser.ConfigParser()
config.read('config.ini')

Clients = {
    'Summit': SummitRestClient,
    'Twilio': TwilioRestClient,
}


def get_auth(provider):
    """Get authentication info from config based on provider name"""
    return (config.get(provider, 'account_sid'),
            config.get(provider, 'auth_token'))

def get_client(provider):
    """Get provider's client object"""
    return Clients[provider](*get_auth(provider))


def send_sms_through_provider(provider, to, body):
    """Perform API request through provider to send an SMS message"""
    auth = get_auth(provider)
    from_number = config.get(provider, 'from_number')
    body += '\nSent using {}'.format(provider)
    client = get_client(provider)
    return client.messages.create(to=to, from_=from_number, body=body)


@app.route('/sms/<recipient>', methods=['POST'])
def sms_send(recipient):
    """
    Attempt to send SMS message using Twilio's API.
    If this fails, use the Summit API to send the SMS message.
    """
    try:
        message = send_sms_through_provider('Twilio', recipient, body)
    except TwilioRestException:
        message = send_sms_through_provider('Summit', recipient, body)

    return jsonify(status=message.status)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
