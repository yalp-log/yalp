# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.outputs.elasticsearch
==========================

The elasticsearch outputer sends events to an elasticsearch index.

.. warning:: This requires the pyelasticsearch_ pacakge to be installed.

This outputer supports the following configuration items:

*uri*
    The elasticsearch connection uri Formatted as
    ``http[s]://[user:password@]<host>[:port]/[path]``. Can also be a
    list of connection uris. Defaults to ``http://localhost:9200/``.

*index*
    The index name to store the documents. Default to
    ``yalp-%Y.%m.%d``.  The index can contain a `date format`_ string
    for a dynamic index.

*doc_type*
    The document name. Default to ``logs``.

*time_based*
    If the index is time based. This requires that the index name
    contains a date format string and that the event contains a valid
    time stamp. Default to ``True``.

*time_stamp_fmt*
    The date format of the time stamp in the event. Not used if the
    ``time_stamp`` field is a datetime. Default to ``%Y-%m-%dT%H:%M:%S``.

*manage_template*
    Allow yalp to manage the elasticsearch index template. Default to
    ``True``.

*template_name*
    The name of the index template to create. Default to ``yalp``.

*template_overwrite*
    Allow yalp to write over any existing template. Default to
    ``False``.

*buffer_size*
    The outputer will buffer this many events before sending them all to
    elasticsearch via a bulk insert. Default is ``500``.

*type*
    A type filter. Only output events of this type.

Example configuration.

.. code-block:: yaml

    outputs:
      - elasticsearch:
          uri: 'http://localhost:9200/'
          index: "yalp-%Y.%m.%d"
          doc_type: logs

.. _pyelasticsearch: https://pypi.python.org/pypi/pyelasticsearch/
.. _date format: https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior
'''
from __future__ import absolute_import
from datetime import datetime

try:
    from elasticsearch import Elasticsearch
    from elasticsearch.exceptions import TransportError
    from elasticsearch.helpers import bulk, BulkIndexError
except ImportError:  # pragma: no cover
    pass
from ..exceptions import OutputException
from . import BaseOutputer


TEMPLATE = {
    'template': 'yalp-*',
    'settings': {
        'index.refresh_interval': '5s',
    },
    'mappings': {
        '_default_': {
            '_all': {
                'enabled': True,
                'omit_norms': True,
            },
            'dynamic_templates': [
                {
                    'message_field': {
                        'match': 'message',
                        'match_mapping_type': 'string',
                        'mapping': {
                            'type': 'string',
                            'index': 'analyzed',
                            'omit_norms': True,
                        },
                    },
                },
                {
                    'string_fields': {
                        'match': '*',
                        'match_mapping_type': 'string',
                        'mapping': {
                            'type': 'string',
                            'index': 'analyzed',
                            'omit_norms': True,
                            'fields': {
                                'raw': {
                                    'type': 'string',
                                    'index':
                                    'not_analyzed',
                                    'ignore_above': 256,
                                    'doc_values': True,
                                },
                            },
                        },
                    },
                }
            ],
            'properties': {
                'geoip': {
                    'type': 'object',
                    'dynamic': True,
                    'properties': {
                        'location': {'type': 'geo_point'},
                    },
                }
            },
        },
    },
}


class ElasticSearchOutputer(BaseOutputer):
    '''
    Send output to elasticsearch
    '''
    def __init__(self,
                 uri='http://localhost:9200/',
                 index='yalp-%Y.%m.%d',
                 doc_type='logs',
                 manage_template=True,
                 template_name='yalp',
                 template_overwrite=False,
                 time_based=True,
                 time_stamp_fmt='%Y-%m-%dT%H:%M:%S',
                 buffer_size=500,
                 *args,
                 **kwargs):
        super(ElasticSearchOutputer, self).__init__(*args, **kwargs)
        sniff_settings = True
        if not isinstance(uri, list):
            sniff_settings = False
            uri = [uri]
        self.es = Elasticsearch(
            uri,
            sniff_on_start=sniff_settings,
            sniff_on_connection_fail=sniff_settings,
        )
        self.index = index
        self.doc_type = doc_type
        self.time_based = time_based
        self.time_stamp_fmt = time_stamp_fmt
        if manage_template:
            self.es.indices.put_template(
                name=template_name,
                body=TEMPLATE,
                create=not template_overwrite,
                ignore=400,
            )
        if not self.time_based:
            self.es.indices.create(index=self.index, ignore=400)
        self.buffer_size = buffer_size
        self.buffer = []

    def get_index(self, event):
        '''
        Get the correct index name for the event.
        '''
        if self.time_based:
            try:
                time_stamp = event['time_stamp']
                if isinstance(time_stamp, str):
                    time_stamp = datetime.strptime(
                        time_stamp,
                        self.time_stamp_fmt,
                    )
                return time_stamp.strftime(self.index)
            except KeyError:
                self.logger.error('Time based event without time stamp')
                raise OutputException
            except ValueError:
                self.logger.error('Time stamp invalid datetime format')
                raise OutputException
            except AttributeError:
                self.logger.error('Time stamp not datetime or str')
                raise OutputException
        else:
            return self.index

    def _flush_buffer(self):
        ''' Write out events to elasticsearch '''
        try:
            try:
                bulk(self.es, self.buffer)
            except BulkIndexError as exc:
                self.logger.error(
                    'Failed to insert some events: %s',
                    exc.errors)
            self.buffer = []
        except TransportError:
            self.logger.warn('Error connection to elasticsearch. Will retry.')

    def output(self, event):
        try:
            self.buffer.append({
                '_type': self.doc_type,
                '_index': self.get_index(event),
                '_source': event
            })
        except OutputException:
            self.logger.error('Output exception', exc_info=True)
        if len(self.buffer) >= self.buffer_size:
            self._flush_buffer()

    def shutdown(self):
        self._flush_buffer()
        self.es.indices.flush(
            index='_all',
            ignore_unavailable=True,
        )


Outputer = ElasticSearchOutputer
