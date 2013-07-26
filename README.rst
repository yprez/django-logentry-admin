=====================
django-logentry-admin
=====================

Add Django LogEntries the the Django admin site.

Allows to view all log entries in the admin.

Based on: `Django snippet 2484 <http://djangosnippets.org/snippets/2484/>`_


Installation
============

Install by using pip or easy_install::

  pip install logentry_admin ### correction : pip install django-logentry-admin

Or install from source::

    git clone git@github.com:yprez/django-logentry-admin.git
    cd django-logentry-admin
    python setup.py install

To add this application into your project, just add it to your
``INSTALLED_APPS`` setting::

    INSTALLED_APPS = (
        ...
        'logentry_admin',
    )
