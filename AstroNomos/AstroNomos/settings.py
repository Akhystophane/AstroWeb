import os
from pathlib import Path
import logging
import certifi
import django_on_heroku
import dj_database_url


ON_HEROKU = 'DYNO' in os.environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'skf&5(@%=bi3r#jgeq8r7_x=c_t8%%tz6zxa)whqo-o8sn=t&i' #ouais je sais ca doit pas etre en clair

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = ['hidden-lowlands-42657.herokuapp.com', 'localhost', '127.0.0.1', 'astro-nomos.com']
ALLOWED_HOSTS = ['*']

SESSION_COOKIE_SECURE = False

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'newsletter',
    'astrochart',
    'rest_framework',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # Place as high as possible
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'astrochart.middleware.AllowIframeMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'newsletter.middleware.RedirectToWwwMiddleware',
]

REST_FRAMEWORK = {'DEFAULT_AUTHENTICATION_CLASSES': ('astrochart.authentication.FirebaseAuthentication',),
                  'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.AllowAny'],
                'DEFAULT_THROTTLE_CLASSES': [
                    'rest_framework.throttling.UserRateThrottle',
                    'rest_framework.throttling.AnonRateThrottle',
                ],
                'DEFAULT_THROTTLE_RATES': {
                    'user': '5/hour',  # Limite de 5 requêtes par heure pour les utilisateurs authentifiés
                    'anon': '5/hour',  # Limite de 2 requêtes par heure pour les utilisateurs anonymes
                }

}

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'AstroNomos.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),         # Votre dossier de templates principal
            os.path.join(BASE_DIR, 'static_frontend'),   # Ajoutez ce chemin
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'AstroNomos.wsgi.application'

AUTH_USER_MODEL = 'astrochart.UserProfile'



# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(conn_max_age=600, ssl_require=True)
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static_frontend'),  # Le dossier contenant les fichiers statiques du frontend
]

# Extra places for collectstatic to find static files.
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configure requests to use certifi certificates
os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
os.environ['SSL_CERT_FILE'] = certifi.where()

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.debug("Settings module loaded.")



# import django_on_heroku
# django_on_heroku.settings(locals())