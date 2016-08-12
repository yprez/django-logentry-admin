from django.conf import settings


def pytest_configure():
    settings.configure(
        ROOT_URLCONF='tests.urls',
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'test.db',
            },
        },
        INSTALLED_APPS=[
            'django.contrib.sessions',
            'django.contrib.contenttypes',
            'django.contrib.auth',
            'django.contrib.admin',
            'logentry_admin',
        ],
        MIDDLEWARE_CLASSES=[
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
        ],
        TEMPLATES=[{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.contrib.auth.context_processors.auth',
                ],
            },
        }],
    )
