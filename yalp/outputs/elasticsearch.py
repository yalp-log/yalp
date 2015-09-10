# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.outputs.elasticsearch
==========================

The elasticsearch outputer sends events to an elasticsearch index.

.. warning:: This requires the pyelasticsearch_ pacakge to be installed.

This outputer supports the following configuration items:

*uri*
    The elasticsearch connection uri Formatted as
    ``http[s]://[user:password@]<host>[:port]/[path]``. Default to
    ``http://localhost:9200/``.

*index*
    The index name to store the documents. Default to
    ``yalp-%Y-%m-%d``.  The index can contain a `date format`_ string
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

*type*
    A type filter. Only output events of this type.

Example configuration.

.. code-block:: yaml

    outputs:
      - elasticsearch:
          uri: 'http://localhost:9200/'
          index: "yalp-%Y-%m-%d"
          doc_type: logs

.. _pyelasticsearch: https://pypi.python.org/pypi/pyelasticsearch/
.. _date format: https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior
'''
from __future__ import absolute_import
from datetime import datetime

try:
    from elasticsearch import Elasticsearch
    from elasticsearch.exceptions import ElasticsearchException
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


class Outputer(BaseOutputer):
    '''
    Send output to elasticsearch
    '''
    def __init__(self,
                 uri='http://localhost:9200/',
                 index='yalp-%Y-%m-%d',
                 doc_type='logs',
                 manage_template=True,
                 template_name='yalp',
                 template_overwrite=False,
                 time_based=True,
                 time_stamp_fmt='%Y-%m-%dT%H:%M:%S',
                 *args,
                 **kwargs):
        super(Outputer, self).__init__(*args, **kwargs)
        self.es = Elasticsearch([uri])  # pylint: disable=C0103
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

    def output(self, event):
        try:
            self.es.create(
                index=self.get_index(event),
                doc_type=self.doc_type,
                body=event,
            )
        except ElasticsearchException:
            self.logger.error('Error processing output', exc_info=True)
        except OutputException:
            self.logger.error('Output exception', exc_info=True)

    def shutdown(self):
        self.es.indices.flush(
            index='_all',
            ignore_unavailable=True,
        )
