from distutils.core import setup

setup(
    name='django-logentry-admin',
    author='Yuri Prezument',
    author_email='y@yprez.com',
    version='0.1.1dev',
    packages=['logentry_admin'],
    license='ISC',
    url='http://github.com/yprez/django-logentry-admin',
    description='Add Django LogEntries the the Django admin site',
    long_description=open('README.rst').read(),
    install_requires=[
        'Django >= 1.3',
    ],
)
