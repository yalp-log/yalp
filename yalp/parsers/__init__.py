# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.parsers
============
'''


class BaseParser(object):
    '''
    Base parser.
    '''

    def __init__(self, config, type=None, tags=None, **kwargs):
        self.config = config
        self.type_ = type
        self.tags = tags or []

    def parse(self, message):
        '''
        Parse the log message.
        '''
        event = {
            'message': message,
            'tags': self.tags,
            'type': self.type_,
        }
        from yalp.outputs import tasks
        tasks.process_output.delay(self.config, event)
        return message
