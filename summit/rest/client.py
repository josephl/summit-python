UNSET_TIMEOUT = 0.1
PROD_CBOSS_API = 'https://api.us1.corvisa.io'
CURRENT_VERSION = 'v0.0.1'


class Resource(object):
    """Base REST resource object"""

    def __init__(self, base_uri, auth, timeout=UNSET_TIMEOUT):
        self.base_uri = base_uri
        self.auth = auth
        self.timeout = timeout

    @property
    def uri(self):
        return '{uri}/{name}'.format(uri=self.base_uri, name=self.name)

    @property
    def name(self):
        return self.__class__.__name__.lower()

    def create_instance(self, body):
        """Create an instance resource with a POST request to the API"""
        resp, inst = self.request('POST', self.uri, data=body)

    def request(self, method, uri, **kwargs):
        resp = make_request(method, uri, auth=self.auth, **kwargs)
        if method == 'DELETE':
            return resp, {}
        return resp, json.loads(resp.content)


class MultiResource(Resource):
    """Multiple instances of one REST resource type"""
    pass


class Messages(MultiResource):
    name = 'sms'

    def create(self, from_=None, **kwargs):
        """Create and send a new SMS message
        """
        kwargs['from'] = from_
        self.create_instance(kwargs)


def make_request(method, url, params=None, auth=None):
    """
    :param method: HTTP method
    :param url: URL
    :param params: dict of query parameters
    :param auth: 2-tuple of (user, password)
    :returns: HTTP response
    """
    resp = requests.request(method, url, params=params, auth=auth)
    return resp



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
