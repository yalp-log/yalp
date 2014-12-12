Install Guide
=============

It is recommended that YALP is installed in a virtualenv.

.. code-block:: bash

    $ mkdir /srv/yalp/
    $ virtualenv /srv/yalp/env
    $ source /srv/yalp/env/bin/activate

Then install via pypi_ using ``pip`` or ``easy_install``.

.. code-block:: bash

    (env) $ pip install yalp

The three scripts ``yalp-inputs``, ``yalp-parsers`` and ``yalp-outputs``,
should now be accessible.

Configuration
-------------

YALP uses a single ``YAML`` configuration file for all three components.
Generally the config file should be consistent throughout the infrastructure,
with the exception of the ``yalp-inputs`` configuration, which should be
specific to the host where the input is being collected.

Celery
++++++

YALP uses Celery_ for distributed processing of events. Celery needs to be
configured. First set the broker connection url.


.. code-block:: yaml

    broker_url: amqp://quest:quest@localhost:5672//


.. note:: Brokers

    For more info on brokers see Celery's `broker docs
    <http://celery.readthedocs.org/en/latest/getting-started/brokers/>`_.


The ``yalp-inputs``
script collects events from input sources and enqueues them into Celery. The
``yalp-parsers`` script starts Celery workers that process these events and
enqueue the processed event back into Celery. Then ``yalp-outputs`` starts
Celery workers that take the processes events and output them to output
sources.

It is (hopefully) obvious that ``yalp-inputs`` can run on multiple hosts. This
allows for collecting input events from various sources, such as syslogs from
all hosts. The ``yalp-parsers`` can also run on many hosts, although generally
the number of celery worker processes should be increased before resorting to
installing workers on multiple hosts.


.. _pypi: https://pypi.python.org/pypi
.. _Celery: http://www.celeryproject.org/
