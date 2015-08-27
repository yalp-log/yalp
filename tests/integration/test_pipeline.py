# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
tests.integration.test_pipeline
===============================
'''
import unittest

import yaml
import subprocess
import time
import pickle
from datetime import datetime

from amqp.exceptions import ChannelError

from yalp.config import settings


class TestSerialization(unittest.TestCase):
    '''
    Test that serialization via celery does not break
    '''
    def setUp(self):
        settings.parsers = [{
            'passthrough': {}
        }]
        try:
            import socket
            import amqp
            self.connection = amqp.Connection()
            self.channel = self.connection.channel()
        except socket.error:
            from nose.plugins.skip import SkipTest
            raise SkipTest('Unable to connect to rabbitmq')
        self.now = datetime.now()
        self.event = {
            'host': 'test_host',
            'message': 'test message',
            'date_time': self.now,
        }
        with open('/tmp/test_serial.yml', 'w') as config_file:
            config = {
                'parsers': [{
                    'passthrough': {}
                }],
                'parser_workers': 1
            }
            yaml.dump(config, config_file)

        self.parser_process = subprocess.Popen(
            'scripts/yalp-parsers -c /tmp/test_serial.yml',
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def tearDown(self):
        self.channel.queue_delete(queue=settings.parser_queue)
        self.channel.queue_delete(queue='outputs')
        self.channel.close()
        self.connection.close()
        self.parser_process.kill()

    def test_default_serializer(self):
        from yalp.pipeline import tasks
        tasks.process_message.apply_async(
            args=[self.event],
            queue=settings.parser_queue,
            serializer=settings.celery_serializer,
        )
        while True:
            try:
                message = self.channel.basic_get(queue='outputs')
                break
            except ChannelError:
                time.sleep(0.1)
        self.assertIsNotNone(message)
        event = pickle.loads(message.body)['message']
        self.assertEqual('test message', event['message'])
        self.assertEqual(self.now, event['date_time'])

