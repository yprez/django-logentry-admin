# Use setuptools if we can
try:
    from setuptools.core import setup
except ImportError:
    from distutils.core import setup

setup(
    name='django-logentry-admin',
    author='Yuri Prezument',
    author_email='y@yprez.com',
    version='0.1.5',
    packages=['logentry_admin'],
    package_data={
        'logentry_admin': ['templates/admin/admin/logentry/change_form.html']
    },
    license='ISC',
    url='http://github.com/yprez/django-logentry-admin',
    description='Show all LogEntries in the Django admin site.',
    long_description=open('README.rst').read(),
    install_requires=[
        'Django>=1.4',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)
