#!/bin/sh

export PYTHONPATH=".:$PYTHONPATH"
export DJANGO_SETTINGS_MODULE="test_settings"
export DJANGO_ADMIN_CMD=`which django-admin.py`

django-admin.py syncdb --no-input
django-admin.py migrate
coverage run --source=logentry_admin $DJANGO_ADMIN_CMD test logentry_admin
coverage report --show-missing
