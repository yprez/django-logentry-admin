#!/bin/sh

export PYTHONPATH=".:$PYTHONPATH"
export DJANGO_SETTINGS_MODULE="test_settings"

# django-admin.py syncdb --no-input
django-admin.py migrate
django-admin.py test logentry_admin
