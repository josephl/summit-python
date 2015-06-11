from .base import Resource, InstanceResource, MultiResource


class Message(InstanceResource):
    """SMS Resource Object"""

    id_key = 'sms_message_id'

    def load(self, entries):
        sent_info = entries.pop('sent')
        entries['from_'] = sent_info.pop('from')
        entries['body'] = sent_info.pop('message')
        entries.update(sent_info)
        self.__dict__.update(entries)


class Messages(MultiResource):
    name = 'sms'
    instance = Message

    def create(self, from_=None, **kwargs):
        """Create and send a new SMS message
        """
        kwargs['From'] = from_ or kwargs.pop('From')
        kwargs['To'] = kwargs.pop('to', None) or kwargs.pop('To', None)
        kwargs['Message'] = (kwargs.pop('body', None) or
                             kwargs.pop('Message', None))
        return self.create_instance(kwargs)

    def create_instance(self, body):
        """SMS endpoint is sms/send, so we have to override"""
        url = '{}/send'.format(self.uri)
        resp, inst = self.request('POST', url, params=body)
        if resp.status_code not in (200, 201):
            raise SummitRestException(resp.status_code, self.uri,
                                      "Resource failed to create")
        return self.load_instance(inst)


