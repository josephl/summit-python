import json
import requests

from ...exceptions import SummitRestException


UNSET_TIMEOUT = 0.1


class Resource(object):
    """Base REST resource object"""

    id_key = NotImplemented

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

    def request(self, method, uri, **kwargs):
        """
        :param method: HTTP method type
        :param uri: request uri
        :returns: 2-tuple of (response, instance dict)
        """
        resp = make_request(method, uri, auth=self.auth, **kwargs)
        if method == 'DELETE':
            return resp, {}
        try:
            instance = resp.json()
        except ValueError:
            instance = {}
        return resp, instance


class InstanceResource(Resource):

    name = None

    def __init__(self, parent, sid):
        self.parent = parent
        self.name = sid
        super(InstanceResource, self).__init__(parent.uri, parent.auth,
                                               parent.timeout)

    def load(self, entries):
        self.__dict__.update(entries)


class MultiResource(Resource):
    """Multiple instances of one REST resource type"""

    instance = NotImplemented

    def create_instance(self, body):
        """Create an instance resource with a POST request to the API"""
        resp, inst = self.request('POST', self.uri, params=body)
        if resp.status_code not in (200, 201):
            raise SummitRestException(resp.status_code, self.uri,
                                      "Resource failed to create")
        return resp, inst

    def load_instance(self, data):
        instance = self.instance(self, data[self.instance.id_key])
        instance.load(data)
        return instance


def make_request(method, url, params=None, auth=None):
    """
    :param method: HTTP method
    :param url: URL
    :param params: dict of query parameters
    :param auth: 2-tuple of (user, password)
    :returns: HTTP response
    """
    headers = {'content-type': 'application/json'}
    data = json.dumps(params)
    return requests.request(method, url, data=data, auth=auth,
                            headers=headers)




