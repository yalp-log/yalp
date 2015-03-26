Custom Plugins
==============

YALP allows for building custom plugins. This allows YALP to be extended to
support new input sources, output types, or custom parsing. Plugins are written
in python and involve inheriting from a base class.


Custom Inputers
---------------

Inputers must inherit from ``BaseInputer`` and must implement the ``run``
function. The class name must be ``Inputer`` for YALP's plguin import system to
discover the inputer. The module name will be used to configure the inputer.
The ``BaseInputer`` provides a property ``stopped`` that should be used by
``run`` to stop collecting events and trigger a cleanup of resources. It also
provides the function ``enqueue_event(event)`` that takes an event dictionary,
adds the ``hostname`` and ``type`` fields and sends the event to the next
phase.

Example Inputer ``custominputer.py``:

.. code-block:: python

    from yalp.inputs import BaseInputer


    class Inputer(BaseInputer):

        def __init__(self, custom_option, *args, **kwargs):
            super(Inputer, self).__init__(*args, **kwargs)
            self.custom_option = custom_option

        def _collect_event(self):
            # Custom event collection code. Returns a dictionary with key
            # `message` with value of raw input string.

        def run(self):
            # ... setup
            while not self.stopped:
                event = self._collect_event()
                self.enqueue_event(event)
            # ... cleanup

This inputer can then be configured ``yalp.yml``:

.. code-block:: yaml

    input_packages:
      - yalp.inputs
      - package.with_custominputer_module

    inputs:
      - custominputer:
          custom_option: 'option'
          type: 'custom'


Custom Parsers
--------------

Parsers must inherit from ``BaseParser`` and must implement the ``parse``
function. The class name must be ``Parser`` for YALP's plugin import system to
discover the parser. The module name will be used to configure the parser. The
``BaseParser`` is written so that the ``parse`` function will only be called if
the event passes the ``type`` filter, thus ``parse`` can assume it is ment to
parse the event. The ``parse`` function must return the parsed event.


Example Parser ``customparser.py``:

.. code-block:: python

    from yalp.parsers import BaseParser


    class Parser(BaseParser):
        def __init__(self, custom_option, *args, **kwargs):
            super(Parser, self).__init__(*args, **kwargs)
            self.custom_option = custom_option

        def parse(self, event):
            message = event.pop('message')
            # ... parse message and set new fields into event
            return event

This parser can then be configured ``yalp.yml``:

.. code-block:: yaml

    parser_packages:
      - yalp.parsers
      - package.with_customparser_module

    parsers:
      - customparser:
          custom_option: 'option'
          type: 'custom'


Custom Outputers
----------------

Outputers must inherit from ``BaseOutputer`` and must implement the ``output``
and ``shutdown`` functions. The class name must be ``Outputer`` for YALP's
plugin import system to discover the outputer. The module name will be used to
configure the outputer. The ``BaseOutpuer`` is written so that the ``output``
function is only called if the event passes teh ``type`` filter, thus
``output`` can assume the event should be output. The ``shutdown`` function is
called when the service is stopped. It should preform and cleanup, cleanly
releasing any resources.


Example outputer ``customoutputer.py``:

.. code-block:: python

    from yalp.outputs import BaseOutputer


    class Outputer(BaseOutputer):
        def __init__(self, custom_option, *args, **kwargs):
            super(Outputer, self)__init__(*args, **kwargs)
            self.resource = connect(custom_option)  # connecting to custom output service/database/source

        def output(self, event):
            self.resource.insert(event)  # send event to service/database/source

        def shutdown(self):
            self.resource.flush()  # ensure data is written
            self.resource.close()  # cleanup connection.

This outputer can then be configured ``yalp.yml``:

.. code-block:: yaml

    output_packages:
      - yalp.outputs
      - package.with_customoutputer_module

    outputs:
      - customoutputer:
          custom_option: 'option'
          type: 'custom'


Logging in Custom PLugins
-------------------------

All ``Base*`` plugin classes have logging already setup.This ensures that log
messages are correctly routed based on the components. Log messages by using:

.. code-block:: python

    self.logger.warning('Warning message')
