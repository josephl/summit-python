class SummitRestException(Exception):

    def __init__(self, status, uri, msg='', code=None, method='GET'):
        self.status = status
        self.uri = uri
        self.msg = msg
        self.code = code
        self.method = method

    def __str__(self):
        return 'HTTP {0} error: {1}'.format(self.status, self.msg)
