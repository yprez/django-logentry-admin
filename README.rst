=====================
django-logentry-admin
=====================

|ci| |pypi-version|

Show all LogEntry objects in the Django admin site.

Originally based on: `Django snippet 2484 <http://djangosnippets.org/snippets/2484/>`_


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

To add this application into your project, just add it to your ``INSTALLED_APPS`` setting:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'logentry_admin',
    )



Development
===========

The project uses `uv <https://docs.astral.sh/uv/>`_. Set up the
environment and run the tests with coverage:

.. code-block:: bash

    uv sync
    uv run coverage run -m pytest
    uv run coverage report

Run them against a particular Python and Django version:

.. code-block:: bash

    uv run --python 3.12 --with "django~=5.2.0" pytest

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


.. |ci| image:: https://github.com/yprez/django-logentry-admin/actions/workflows/ci.yml/badge.svg?branch=master
    :target: https://github.com/yprez/django-logentry-admin/actions/workflows/ci.yml

.. |pypi-version| image:: https://img.shields.io/pypi/v/django-logentry-admin.svg
    :target: https://pypi.org/project/django-logentry-admin/
