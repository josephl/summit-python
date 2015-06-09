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
    return (config.get(provider, 'account_sid'),
            config.get(provider, 'auth_token'))

def get_client(provider):
    return Clients[provider](*get_auth(provider))


def send_sms_through_provider(provider, to, body):
    auth = get_auth(provider)
    from_number = config.get(provider, 'from_number')
    body += '\nSent using {}'.format(provider)
    client = get_client(provider)
    return client.messages.create(to=to, from_=from_number, body=body)


@app.route('/sms/<recipient>', methods=['POST'])
def sms_send(recipient):
    try:
        message = send_sms_through_provider('Twilio', recipient, body)
    except TwilioRestException:
        message = send_sms_through_provider('Summit', recipient, body)

    return jsonify(status=message.status)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
