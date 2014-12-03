# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.parsers
============
'''


class BaseParser(object):
    '''
    Base parser.
    '''

    def __init__(self, config):
        self.type_ = config.get('type')
        self.tags = config.get('tags', [])
        self.output_config = config.get('outputs', [])

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
        tasks.process_output.delay(self.output_config, event)
        return message
