Install Guide
=============

YALP is designed to be installed on multiple servers, with different
components running on separate machines. It can just as easily be installed on
a single machine. This guide will show how to setup all components on a single
host, but will also describe how the components could easily be distributed.


Celery Broker
-------------

Since YALP uses Celery_ for communication between components, a broker must be
installed. For this guide, the default broker rabbitmq_ will be used.

.. sidebar:: Brokers

    For more info on brokers see Celery's `broker docs`_.

To install rabbitmq under Ubuntu.

.. code-block:: bash

    $ sudo apt-get install rabbitmq-server


Installing YALP
---------------

For now the easiest way to YALP is installed in a virtualenv.

.. code-block:: bash

    $ virtualenv /srv/yalp_env
    $ source /srv/yalp_env/bin/activate

Then install via pypi_ using ``pip`` or ``easy_install``.

.. code-block:: bash

    (yalp_env) $ pip install yalp

The three components ``yalp-inputs``, ``yalp-parsers`` and ``yalp-outputs``,
should now be accessible.


Configuration
-------------

YALP uses a single ``YAML`` configuration file for all three components.
Generally the config file should be consistent throughout the infrastructure,
with the exception of the ``yalp-inputs`` configuration, which should be
specific to the host where the input is being collected.

The first section of the config file deals with Celery configuration.

.. code-block:: yaml

    # Celery configuration
    broker_url: amqp://guest:guest@localhost:5672//
    parser_queue: parsers
    output_queue: outputs
    parser_worker_name: parser-workers
    output_worker_name: output-workers

**broker_url**
    This is the connection uri for connecting to the broker.

**parser_queue**
    This is the name of the queue that the Parsers will watch for tasks. This
    can be set to any name so that it is easily identifiable, especially if
    the broker is being used for other services. The default name is
    ``parsers``.

**output_queue**
    This is the name of the queue that the Outputs will watch for tasks. This
    can be set to any name so that it is easily identifiable, especially if
    the broker is being used for other services. The default name is
    ``outputs``.

**parser_worker_name**
    This is the name on the Parser processes so that can easily be identifies
    via tools like ``ps``.

**output_worker_name**
    This is the name on the Output processes so that can easily be identifies
    via tools like ``ps``.


The next section of the config is for plugin configuration.

.. code-block:: yaml

    # Plugin configuration
    input_packages:
      - yalp.inputs
    parser_packages:
      - yalp.parsers
    output_packages:
      - yalp.outputs

Each option contains a list of python packages that contain plugin modules for
the specific component. This allows to specifying custom or third-part plugins.
The defaults are in the example above.


Next is the ``inputs`` section.

.. code-block:: yaml

    # Input configuration
    inputs:
      - 'file':
          path: '/var/log/messages'
          type: messages

This section contains a list of inputs to monitor for events. This example is
set to monitor ``/var/log/messages``. The ``type`` option limits what parsers
and outputers will process this input. Only parsers are outputs that have the
same ``type`` will process the message. The general format is as follows.

.. sidebar:: Options for pluings

    See the :doc:`Full Plugin Reference </ref/index>` for options the the
    plugins.

.. code-block:: yaml

    inputs:
      - '<module>':
          <option>: <value>
          ...
          <option>: <value>
      - '<module>':
          <option>: <value>
          ...
          <option>: <value>


The last two sections are similar to the ``inputs`` section but are for
configuring the ``parsers`` and ``outputs``.

.. code-block:: yaml

    parsers:
      - 'passthrough':
          type: messages

    outputs:
      - 'mongo':
          uri: 'mongodb://localhost:27017/yalp'
          database: yalp
          collection: logs


This configures the parsers to pass the message to the outpers without modifing
it. The message will then to output to mongodb running on the same machine.


.. _pypi: https://pypi.python.org/pypi
.. _Celery: http://www.celeryproject.org/
.. _rabbitmq: http://www.rabbitmq.com/
.. _broker docs: http://celery.readthedocs.org/en/latest/getting-started/brokers/
