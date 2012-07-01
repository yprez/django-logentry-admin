from distutils.core import setup

setup(
    name='django-logentry-admin',
    author='Yuri Prezument',
    author_email='y@yprez.com',
    version='0.1.2a1',
    packages=['logentry_admin'],
    license='ISC',
    url='http://github.com/yprez/django-logentry-admin',
    description='Add Django LogEntries the the Django admin site',
    long_description=open('README.rst').read(),
    install_requires=[
        'Django >= 1.3',
    ],
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ),
)
