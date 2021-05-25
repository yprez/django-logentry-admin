=====================
django-logentry-admin
=====================

|travis-ci| |coverage| |requires-io| |pypi-version|

Show all LogEntry objects in the Django admin site.

Originally based on: `Django snippet 2484 <http://djangosnippets.org/snippets/2484/>`_


Supported versions
==================

* Django 3.2, 3.1, 2.2
* Python 3.9, 3.8, 3.7, 3.6, 3.5


Installation
============

Install by using pip or easy_install:

.. code-block:: bash

  pip install django-logentry-admin

Or install from source:

.. code-block:: bash

    git clone git@github.com:yprez/django-logentry-admin.git
    cd django-logentry-admin
    python setup.py install

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


.. |travis-ci| image:: http://img.shields.io/travis/yprez/django-logentry-admin/master.svg?style=flat
   :target: http://travis-ci.org/yprez/django-logentry-admin

.. |coverage| image:: https://img.shields.io/coveralls/yprez/django-logentry-admin.svg?branch=master
   :target: https://coveralls.io/r/yprez/django-logentry-admin?branch=coveralls

.. |pypi-version| image:: http://img.shields.io/pypi/v/django-logentry-admin.svg?style=flat
    :target: https://pypi.python.org/pypi/django-logentry-admin

.. |requires-io| image:: https://img.shields.io/requires/github/yprez/django-logentry-admin.svg
    :target: https://requires.io/github/yprez/django-logentry-admin/requirements/?branch=master
