YALP
====

Distributed log parsing and collection.

YALP is a log parsing pipeline written in python. It utilized Celery_ for
stable and scalable distributed processing, is easy to configure, and customize
and extend.

Install and Configure
---------------------

Brief install guide:

.. code-block:: bash

    $ sudo apt-get install rabbitmq-server mongodb
    $ virtualenv /srv/yalp_env
    $ source /srv/yalp_env/bin/activate
    (yalp_env) $ pip install yalp

``/srv/yalp.yml``:

.. code-block:: yaml

    # Celery configuration
    broker_url: amqp://guest:guest@localhost:5672//
    inputs:
      - 'file':
          path: '/var/log/syslog'
          type: messages
    parsers:
      - 'passthrough':
          type: messages
    outputs:
      - 'mongo':
          uri: 'mongodb://localhost:27017/yalp'
          database: yalp
          collection: logs

.. code-block:: bash

    (yalp_env) $ yalp-inputs -c /srv/yalp.yml
    (yalp_env) $ yalp-parsers -c /srv/yalp.yml
    (yalp_env) $ yalp-outputs -c /srv/yalp.yml

:doc:`Full Installation Guide </topics/install>`

Reference
---------

:doc:`Full Plugin Reference </ref/index>`


.. toctree::
    :hidden:
    :glob:

    topics/install
    topics/logging
    ref/index
    topics/plugins
    topics/scaling


.. _Celery: http://www.celeryproject.org/
