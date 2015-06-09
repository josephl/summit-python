import ConfigParser
from flask import Flask, jsonify, request
import json
from twilio.rest import TwilioRestClient


app = Flask(__name__)
config = ConfigParser.ConfigParser()
config.read('config.ini')


@app.route('/sms/<recipient>', methods=['POST'])
def sms_send(recipient):
    auth = (
        config.get('Twilio', 'account_sid'),
        config.get('Twilio', 'auth_token'))
    from_number = config.get('Twilio', 'from_number')
    body = request.get_data() or 'OH HI THERE'
    client = TwilioRestClient(*auth)
    message = client.messages.create(to=recipient, from_=from_number,
                                     body=body)
    return jsonify(status=message.status)


if __name__ == '__main__':
    app.run(debug=True)
