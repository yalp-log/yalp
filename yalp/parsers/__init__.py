# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.parsers
============
'''


class BaseParser(object):
    '''
    Base parser.
    '''

    def __init__(self, tags=None, **kwargs):  # pylint: disable=W0613
        self.tags = tags or []

    def parse(self, message):
        '''
        Parse the log message.
        '''
        event = {
            'message': message,
            'tags': self.tags,
        }
        from yalp.outputs import tasks
        tasks.process_output.delay(event)
        return message
