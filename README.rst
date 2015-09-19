YALP
====

|build-status| |coverage| |deps| |pypi| |docs| |health|

Distributed log parsing and collection.

.. |build-status| image:: http://img.shields.io/travis/yalp-log/yalp/master.svg?style=flat
    :alt: Build Status
    :scale: 100%
    :target: https://travis-ci.org/yalp-log/yalp

.. |coverage| image:: http://img.shields.io/coveralls/yalp-log/yalp.svg?style=flat
    :alt: Coverage Status
    :scale: 100%
    :target: https://coveralls.io/r/yalp-log/yalp?branch=master

.. |deps| image:: http://img.shields.io/gemnasium/yalp-log/yalp.svg?style=flat
    :alt: Dependency Status
    :scale: 100%
    :target: https://gemnasium.com/yalp-log/yalp

.. |pypi| image:: http://img.shields.io/pypi/v/yalp.svg?style=flat
    :alt: PyPi version
    :scale: 100%
    :target: https://pypi.python.org/pypi/yalp

.. |docs| image:: https://readthedocs.org/projects/yalp/badge/
    :alt: Documentation Status
    :scale: 100%
    :target: https://yalp.readthedocs.org

.. |health| image:: https://landscape.io/github/yalp-log/yalp/master/landscape.svg?style=flat
   :alt: Code Health
    :scale: 100%
   :target: https://landscape.io/github/yalp-log/yalp/master


Install and Configure
---------------------

Brief install guide:

.. code-block:: bash

    $ sudo apt-get install rabbitmq-server
    $ virtualenv /srv/yalp_env
    $ source /srv/yalp_env/bin/activate
    (yalp_env) $ pip install yalp

``/srv/yalp.yml``:

.. code-block:: yaml

    # Celery configuration
    broker_url: amqp://guest:guest@localhost:5672//
    inputs:
      - file:
          path: '/var/log/nginx/access.log'
    parsers:
      - grok:
          pattern: '%{COMBINEDAPACHELOG}'
      - timestamp:
          field: timestamp
      - goip:
          field: clientip
          geoip_dat: /usr/share/GeoLiteCity.dat
      - user_agent:
          field: agent
      - url:
          field: request
    outputs:
      - elasticsearch:
          uri: http://localhost:9200

.. code-block:: bash

    (yalp_env) $ yalp-inputs -c /srv/yalp.yml
    (yalp_env) $ yalp-parsers -c /srv/yalp.yml
    (yalp_env) $ yalp-outputs -c /srv/yalp.yml
