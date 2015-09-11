Inputers
========

Inputers collect events from input sources. The events are send to the parsers
for proccessing, or if there are no parsers configured, the events are directly
sent to the outputers. All input events are sent as a dictionary with the
fields ``hostname`` and ``message`` which contain the hostname where the
inputer was collected and the raw input from the source. Events can also have
an optional ``type`` field used to filter events. Custom inputers can also add
additional optional fields.

Example input event:

.. code-block:: python

    {
      'hostname': 'localhost',
      'message': '127.0.0.1 - - [13/Mar/2014:13:46:00 -0400] "GET / HTTP/1.1" 200 6301 "-" "Mozilla/5.0 (X11; Linux x86_64; rv:24.0) Gecko/20100101 Firefox/24.0" "6.57"',
      'type': 'nginx',
    }


Full List of Inputers
---------------------

.. currentmodule:: yalp.inputs

.. toctree::

    yalp.inputs.file
    yalp.inputs.log_handler
