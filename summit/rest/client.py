from .resources import Messages


UNSET_TIMEOUT = 0.1
PROD_CBOSS_API = 'https://api.us1.corvisa.io'
CURRENT_VERSION = 'v0.0.1'


class SummitRestClient(object):
    """Summit REST API client"""

    def __init__(self, account=None, token=None, base=PROD_CBOSS_API,
                 version=CURRENT_VERSION, timeout=UNSET_TIMEOUT):
        """
        :param account: Summit API key
        :param token: Summit API key secret
        """
        self.base = base
        self.auth = (account, token)
        self.timeout = timeout
        # Twilio places all resources under an account resource path
        # but we don't, so account_uri is kind of a misnomer here. Oh well.
        self.account_uri = self.base_uri = '{base}/{version}'.format(
            base=base,
            version=version)
        # Initializes resource types
        self.messages = Messages(self.base_uri, self.auth, self.timeout)
