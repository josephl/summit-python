"""
Basic demo of summit-python that sends a simple SMS message from the
command-line.
"""

import argparse

from summit.rest import SummitRestClient


def main():
    parser = argparse.ArgumentParser(
        description="Command-line SMS sender using Corvisa's Summit API.")
    parser.add_argument('--key', required=True,
                        help="Your application's API key.")
    parser.add_argument('--secret', required=True,
                        help="Your application's API key secret.")
    parser.add_argument('--from', required=True, help=(
        "Number to send from. Must be an authorized number "
        "for your Summit app."))
    parser.add_argument('--to', required=True, help="Recipient of SMS message.")
    parser.add_argument('--message', required=True,
                        help="Body of the SMS message.")
    args = parser.parse_args()

    client = SummitRestClient(account=args.key, token=args.secret)
    resp, inst = client.messages.create(from_=getattr(args, 'from'),
                                        to=args.to,
                                        body=args.message)
    print 'Responded with code: {}'.format(resp.status_code)
    print inst


if __name__ == '__main__':
    main()
