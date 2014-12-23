Parsers
=======

Parsers process an input event transforming the raw message into more useful
and organized fields. Therefore the parsed event dictionary may contain any
number of fields. Parsers should preserve the ``hostname`` and optional
``type`` field of an input event.

Example parsed event:

.. code-block:: python

    {
      'hostname': 'localhost',
      'remote_addr': '127.0.0.1',
      'time': '13/Mar/2014:13:46:00',
      'request': '/',
      'status': '200',
      'bytes_send': '6301',
      'user_agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:24.0) Gecko/20100101 Firefox/24.0',
      'type': 'nginx',
    }


Full List of Parsers
--------------------

.. currentmodule:: yalp.parsers

.. toctree::

    yalp.parsers.regex
