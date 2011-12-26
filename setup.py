from distutils.core import setup

setup(
    name='django-logentry-admin',
    author='Yuri Prezument',
    author_email='y@yprez.com',
    version='0.0.1dev',
    packages=['logentry_admin'],
    license='LICENSE.txt',
    #url='http://pypi.python.org/pypi/django-logentry-admin/',
    description='Add Django LogEntries the the Django admin site',
    long_description=open('README.rst').read(),
    install_requires=[
        'Django >= 1.1.1',
    ],
)
