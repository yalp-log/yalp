Logging Configuration
=====================

Logging configuration is done in the same config file as other
:ref:`configuration`.

Simple Config Options
---------------------

By default, YALP will log warnings and errors to the console. The log level and
format can be changed using the following options:

.. sidebar:: Log format

    See Python's `LogRecord attributes`_ for details on log formats.

.. code-block:: yaml

    log_level: 'WARN'
    log_format: '%(name)s: %(levelname)s [%(module)s:%(lineno)s] %(message)s'


Advanced Configuration
----------------------

YALP supports advanced loggging configuration through the ``logging``
configuration option. For example to set YALP to log to `Sentry`_:

.. code-block:: yaml

    logging:
      version: 1
      disable_existing_loggers: false
      handlers:
        sentry:
          level: DEBUG
          class: 'raven.handlers.logging.SentryHandler'
          dsn: 'https://public:secret@example.com/1'
      loggers:
        yalp.inputs:
          handlers:
            - sentry
          level: WARN
          propagate: false
        yalp.parsers
          handlers:
            - sentry
          level: WARN
          propagate: false
        yalp.outputs
          handlers:
            - sentry
          level: WARN
          propagate: false

.. note::
    The loggers ``yalp.inputs``, ``yalp.parsers``, and ``yalp.outputs`` will
    catch all log messages for the corresponding plugins. To capture all of
    YALP's logs, use the ``yalp`` logger.


.. _Sentry: https://getsentry.com/
.. _LogRecord attributes: https://docs.python.org/2/library/logging.html#logrecord-attributes`
