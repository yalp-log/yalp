# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.outputs.elasticsearch
==========================

The elasticsearch outputer sends events to an elasticsearch index.

.. warning:: This requires the pyelasticsearch_ pacakge to be installed.

This outputer supports the following configuration items:

**uri**
    The elasticsearch connection uri Formatted as
    ``http[s]://[user:password@]<host>[:port]/[path]``

**index**
    The index name to store the documents.

**doc_type**
    The document name

*type*
    A type filter. Only output events of this type.

Example configuration.

.. code-block:: yaml

    outputs:
      - elasticsearch:
          uri: 'http://localhost:9200/'
          index: yalp
          doc_type: logs

.. _pyelasticsearch: https://pypi.python.org/pypi/pyelasticsearch/
'''
from __future__ import absolute_import

try:
    from elasticsearch import Elasticsearch
    from elasticsearch.exceptions import ElasticsearchException
except ImportError:  # pragma: no cover
    pass
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
            'dynamic_templates': [{
                'message_field': {
                    'match': 'message',
                    'match_mapping_type': 'string',
                    'mapping': {
                        'type': 'string',
                        'index': 'analyzed',
                        'omit_norms': True,
                    },
                },
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
            }],
            'properties': {
                '@version': {
                    'type': 'string',
                    'index': 'not_analyzed',
                },
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
                 uri,
                 index,
                 doc_type,
                 template_settings,
                 *args,
                 **kwargs):
        super(Outputer, self).__init__(*args, **kwargs)
        self.es = Elasticsearch([uri])  # pylint: disable=C0103
        self.index = index
        self.doc_type = doc_type
        self.es.indices.create(index=self.index, ignore=400)
        if template_settings['manage']:
            self.es.indices.put_template(
                template_settings['name'],
                TEMPLATE,
                template_settings['override'],
            )

    def output(self, event):
        try:
            self.es.create(
                index=self.index,
                doc_type=self.doc_type,
                body=event,
            )
        except ElasticsearchException:
            self.logger.error('Error processing output', exc_info=True)

    def shutdown(self):
        self.es.indices.flush(self.index)
