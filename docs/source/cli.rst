Command-Line Interface
======================

Usage
-----

This project includes some command-line-interface commands,
to install the required dependencies, install them with pip:

.. code-block:: console

    (.venv) $ pip install sapimclient[cli]

Options:
    - ``--tenant {TENANT}``: **Required**
        Tenant to connect to, for example 'CALD-DEV'.
    - ``--username {USERNAME}``: **Required**
        Username for authentication.
    - ``--password {PASSWORD}``: **Required**
        Password for authentication.
    - ``--no-ssl``: *Optional*
        Disable SSL validation.
    - ``--logfile {PATH}``: *Optional*
        Enable logging to a file.
    - ``-v``: *Optional*
        Verbose logging.
    - ``-debug``: *Optional*
        Enable DEBUG logging.

To list all available options and commands:

.. code-block:: console

    (.venv) $ python -m sapimclient --help

.. code-block:: console

    Usage: python -m sapimclient [OPTIONS] COMMAND [ARGS]...

    Command-line interface for Python SAP Incentive Management.

    You may provide parameters by setting environment variables
    prefixed with 'SAP_' or by passing them as options.
    For example: `export SAP_TENANT=CALD-DEV` is equivalent
    to passing `--tenant CALD-DEV`

    Options:
    -t, --tenant TEXT    Tenant to connect to, for example 'CALD-DEV'.
    -u, --username TEXT  Username for authentication.
    -p, --password TEXT  Password for authentication.
    --no-ssl             Disable SSL validation.
    -l, --logfile FILE   Enable logging to a file.
    -v                   Verbose logging.
    -debug               Enable DEBUG logging.
    --help               Show this message and exit.

    Commands:
    calendars  List all calendars.
    deploy     Deploy rule elements from a directory to the tenant.
    export     Export Resource to a file.
    periods    List all periods for a calendar.

Each command has it's own options, to list all options, append ``--help`` to the command.

Calendars
---------

List all calendars:

.. code-block:: console

    (.venv) $ python -m sapimclient \
        --tenant {TENANT} \
        --username {USERNAME} \
        --password {PASSWORD} \
        calendars

Periods
-------

Options:
    - ``--calendar {CALENDAR}`` **Required**
        The calendar name to list periods for.
    - ``--period {PERIOD}`` *Optional*
        Name of the Period to search. Allows wildcard like ``*2024*``.

List all periods for a calendar:

.. code-block:: console

    (.venv) $ python -m sapimclient \
        --tenant {TENANT} \
        --username {USERNAME} \
        --password {PASSWORD} \
        periods --calendar {CALENDAR}

Deploy
------

Deploy exported Plan Data and Global Values from a
directory to the tenant.

Plan data ``*.xml`` is imported with an import pipeline job.
Global Values ``*.txt`` are imported with their respective :ref:`model:data type`.

To correctly identify the :ref:`model:data type`, files have to follow a specific
naming convention:

    - Event Type.txt
    - Credit Type.txt
    - Earning Group.txt
    - Earning Code.txt
    - Fixed Value Type.txt
    - Reason Code.txt

Additionally you can control the order of processing by prefixing the filenames.
For example:

    - 01 Event Type.txt
    - 02 Credit Type.txt
    - 03 Plan.XML

.. tip::
    Enable logging to catch import errors.
    See ``--logfile log.txt`` in the below example.

Arguments:
    - ``PATH``: **Required**
        The path to the directory to be processed.

.. code-block:: console

    (.venv) $ python -m sapimclient \
        --tenant {TENANT} \
        --username {USERNAME} \
        --password {PASSWORD} \
        --logfile log.txt \
        deploy ./deploy


Export
------

Export Credits, Measurements, Incentives, Commissions, Deposits and Payments to a file
in the same way you would using the respective UI workspaces.

Options:
    - ``--calendar {CALENDAR}`` *Optional*
        Apply :py:class:`Calendar <sapimclient.model.resource.Calendar>` filter on the exported data.
    - ``--period {PERIOD}`` *Optional*
        Apply :py:class:`Period <sapimclient.model.resource.Period>` filter on the exported data.
        Requires ``--calendar`` to be provided.
    - ``--filters {FILTER_TEXT}`` *Optional*
        Apply :py:class:`Period <sapimclient.model.resource.Period>` filter on the exported data.
        Can be applied more then once.

.. tip::

    Refer to the :ref:`API Documentation <index:rest api>` to understand the filter mechanism.

Arguments:
    - ``RESOURCE`` **Required**
        The resource to load into a file.
        One of ``{CREDITS|MEASUREMENTS|INCENTIVES|COMMISSIONS|DEPOSITS|PAYMENTS}``
    - ``PATH`` **Required**
        Path of the file to write to.

.. note::

    Exporting a large number of records will lead to poor performance. It is strngly
    recommended to stay below 100.000 records.

.. tip::
    Enable logging to catch import errors.
    See ``--logfile log.txt`` in the below examples.

Export credits to a file:

.. code-block:: console

    (.venv) $ python -m sapimclient \
        --tenant {TENANT} \
        --username {USERNAME} \
        --password {PASSWORD} \
        --logfile log.txt \
        export CREDITS credits.txt \
        --calendar {CALENDAR} \
        --period {PERIOD}

Export payments above € 100.000,-:

.. code-block:: console

    (.venv) $ python -m sapimclient \
        --tenant {TENANT} \
        --username {USERNAME} \
        --password {PASSWORD} \
        --logfile log.txt \
        export PAYMENTS payments.txt \
        --filter "payment ge '100000 EUR'"
