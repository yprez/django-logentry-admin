=====================
django-logentry-admin
=====================

|pypi-version|

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



Running tests
=============

Test on all Python / Django versions with tox:

.. code-block:: bash

   $ pip install tox
   $ tox

Or just a specific Django / Python version:

.. code-block:: bash

    $ tox -e py314-django61

Or run the environments in parallel:

.. code-block:: bash

    $ tox run-parallel


.. |pypi-version| image:: https://img.shields.io/pypi/v/django-logentry-admin.svg
    :target: https://pypi.org/project/django-logentry-admin/
