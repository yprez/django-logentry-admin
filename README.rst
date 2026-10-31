=====================
django-logentry-admin
=====================

|ci| |pypi-version|

Show all LogEntry objects in the Django admin site.

Django records every addition, change and deletion made through the
admin, but only shows each user their own last few actions. This app
adds the whole log to the admin:

* a list of every entry, filtered by staff user, content type and
  action, searchable by object and change message, and browsable by
  date
* links from each entry to the object and the user it concerns, on
  the admin site you are using
* a read-only page per entry, since the log is a record: entries cannot
  be added, changed or deleted

Superusers see the log, and so do staff users with the "Can view log
entry" permission.

Originally based on `Django snippet 2484 <https://djangosnippets.org/snippets/2484/>`_.


Supported versions
==================

* Django 5.2, 6.0, 6.1
* Python 3.10 to 3.14 (Django 6.0 and later need Python 3.12 or later)


Installation
============

Install with pip:

.. code-block:: bash

    pip install django-logentry-admin

Or install from source:

.. code-block:: bash

    git clone https://github.com/yprez/django-logentry-admin.git
    cd django-logentry-admin
    pip install .

Then add it to ``INSTALLED_APPS``:

.. code-block:: python

    INSTALLED_APPS = [
        ...
        "logentry_admin",
    ]

The log appears in the admin under "Administration", as "Log entries".
It is translated into Azerbaijani, Brazilian Portuguese, Esperanto and
Russian.


Development
===========

The project uses `uv <https://docs.astral.sh/uv/>`_. Set up the
environment and run the tests with coverage:

.. code-block:: bash

    uv sync
    uv run coverage run -m pytest
    uv run coverage report

Run them against a particular Python and Django version, in a throwaway
environment that leaves the one above as it is:

.. code-block:: bash

    uv run --isolated --python 3.12 --with "django~=5.2.0" pytest

The translations need GNU gettext. After changing a message in the code,
update the catalogs, translate, compile them and commit both the ``.po``
and ``.mo`` files; CI checks that they match:

.. code-block:: bash

    cd src/logentry_admin
    uv run django-admin makemessages --all
    uv run django-admin compilemessages

To release, set the new version in ``pyproject.toml`` and the changelog,
merge, then publish a GitHub release tagged ``v<version>``. The release
workflow builds it and uploads it to PyPI.


.. |ci| image:: https://github.com/yprez/django-logentry-admin/actions/workflows/ci.yml/badge.svg?branch=main
    :target: https://github.com/yprez/django-logentry-admin/actions/workflows/ci.yml

.. |pypi-version| image:: https://img.shields.io/pypi/v/django-logentry-admin.svg
    :target: https://pypi.org/project/django-logentry-admin/
