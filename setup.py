from setuptools import setup

with open('README.rst') as f:
    readme = f.read()


with open('CHANGELOG.rst') as f:
    changelog = f.read()


setup(
    name='django-logentry-admin',
    author='Yuri Prezument',
    author_email='y@yprez.com',
    version='1.1.0',
    packages=['logentry_admin'],
    package_data={
        'logentry_admin': [
            'templates/admin/admin/logentry/change_form.html',
            '*.po',
        ],
    },
    include_package_data=True,
    license='ISC',
    url='https://github.com/yprez/django-logentry-admin',
    description='Show all LogEntry objects in the Django admin site.',
    long_description='\n\n'.join([readme, changelog]),
    install_requires=[
        'Django>=2.2',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.1',
        'Framework :: Django :: 3.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
