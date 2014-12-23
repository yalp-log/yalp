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
except ImportError:  # pragma: no cover
    pass
from . import BaseOutputer


class Outputer(BaseOutputer):
    '''
    Send output to elasticsearch
    '''
    def __init__(self,
                 uri,
                 index,
                 doc_type,
                 *args,
                 **kwargs):
        super(Outputer, self).__init__(*args, **kwargs)
        self.es = Elasticsearch([uri])  # pylint: disable=C0103
        self.index = index
        self.doc_type = doc_type
        self.es.indices.create(index=self.index, ignore=400)

    def output(self, event):
        self.es.create(index=self.index, doc_type=self.doc_type, body=event)

    def shutdown(self):
        self.es.indices.flush(self.index)
