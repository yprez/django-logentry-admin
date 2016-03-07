from setuptools import setup


with open('README.rst') as f:
    readme = f.read()


with open('CHANGELOG.rst') as f:
    changelog = f.read()


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
    description='Show all LogEntry objects in the Django admin site.',
    long_description=readme + '\n\n' + changelog,
    install_requires=[
        'Django>=1.7',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
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
        'Programming Language :: Python :: 3.5',
        'Framework :: Django',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
    ],
)
