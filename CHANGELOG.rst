=========
Changelog
=========


v1.2.0 - 31/10/2026
===================

* Add support for Django 5.2, 6.0 and 6.1, and Python 3.10 to 3.14.
* Drop support for Django older than 5.2 and Python older than 3.10.
* Fix change messages showing as raw JSON (a regression in 1.1.0).
* Fix the translations, which never loaded: no release shipped the
  compiled catalogs.
* Fix the spelling of "Adição" in the Brazilian Portuguese translation.
* Show each log entry on a read-only page, without Save buttons.
* Fetch each entry's user with the list on Django 6.1, which stopped
  joining it on its own and ran one query per row.
* Fix links in a project with more than one admin site, which could lead
  to another site than the one in use.
* Fix links to objects whose text primary key contains a sequence the
  admin escapes, such as "_26".
* Fix the staff user filter for custom user models whose primary key is
  not named ``id``.
* Remove the ``get_actions()`` override that Django 6.1 deprecates.
* Package with ``pyproject.toml``, test on GitHub Actions, and publish to
  PyPI through trusted publishing.


v1.1.0 - 25/05/2021
===================

* Add tests/support for Django 3.2, 3.1.
* Add tests/support for Python 3.9.
* Drop support for Python 2.7, 3.4.
* Drop support for Django 1.x, 2.0, 2.1.


v1.0.6 - 23/04/2020
===================

* Add tests for Python 3.8, Django 3.0.
* Fix including locale files in wheel package.


v1.0.5 - 30/07/2019
===================

* Test on Python 3.7.
* Add tests for Django 2.1.
* Add tests for Django 2.2.
* Remove tests for Django 1.7.
* Fix translations, include locale files in the package.


v1.0.4 - 17/06/2018
===================

* Fix admin links for Django 2.0.


v1.0.3 - 14/12/2017
===================

* Add tests for Django 1.11 and 2.0 compatibility.
* Drop support for Python 3.2, 3.3.
* Make short_descriptions translatable in admin.py.
* Make use of new get_change_message() method on Django >= 1.11.
* Add Russian, Azerbaijani and Portuguese translations.


v1.0.2 - 12/08/2016
===================

* Add tests for Django 1.10 compatibility.


v1.0.1 - 24/07/2016
===================

* Add tests and support for Django 1.9 and Python 3.5.
* Drop support for Python 2.5, 2.6, Django 1.4, 1.5, 1.6.
* Fix AttributeError when content_type is None, issue `#21 <https://github.com/yprez/django-logentry-admin/issues/21>`_.
* Show log entries for users with change_logentry permission, `#25 <https://github.com/yprez/django-logentry-admin/pull/25>`_.
* Test with py.test instead of unittest.


v0.1.5 - 17/02/2015
===================

* Django 1.8 compatibility.


v0.1.4 - 28/09/2014
===================

* Added Django 1.7 compatibility.
* Fixed compatibility issues with Django 1.5, 1.4 and Python 3.2.
* Added tests.


v0.1.3 - 02/06/2014
===================

* Improved display layout.
* Added links to user and object.
* Added "By staff user" filter.
* Don't allow delete action for LogEntry.
* Better performance by prefetching content types.


v0.1.2 - 26/08/2013
===================

* Added an empty model.py file.
* Minor documentation (readme) updates/fixes.


v0.1.1 - 28/12/2011
===================

* Added object links and action description.


v0.1.0 - 26/12/2011
===================

* Initial release.
