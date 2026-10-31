=====================
django-logentry-admin
=====================

|pypi-version|

Show all LogEntry objects in the Django admin site.

Originally based on: `Django snippet 2484 <http://djangosnippets.org/snippets/2484/>`_


Supported versions
==================

* Django 3.2, 3.1, 2.2
* Python 3.9, 3.8, 3.7, 3.6, 3.5


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

    $ tox -e py35-django19

Or run on multiple CPUs in parallel with detox to make it faster:

.. code-block:: bash

    $ pip install detox
    $ detox


.. |pypi-version| image:: https://img.shields.io/pypi/v/django-logentry-admin.svg
    :target: https://pypi.org/project/django-logentry-admin/
