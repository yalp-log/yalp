Scaling YALP
============

YALP is built to easily scale. It leverages the stability of Celery for
distributed processing.


Parser Scaling
--------------

Parsers run as Celery workers. The workers run concurrent processes. The number
of processes can be configured with the ``parser_workers`` option (default is
5). Additionally multiple ``yalp-parsers`` processes can be started on separate
hosts. Ensure that each server uses the same YALP config file and has access to
the broker.

Output Scaling
--------------

Outputers can scale in the same manner as parsers. Use the ``output_workers``
option (default is 1) and/or start multiple ``yalp-putputs`` processes on
separate servers.

.. warning::

    Be sure that the configured outputers can handle concurrent output. Most
    databases like Mongo and Elasticsearch can, but the File outputer may
    garble the output.
