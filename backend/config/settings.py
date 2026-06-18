"""
Configuración principal del proyecto Django - Sistema de Becas
"""
from pathlib import Path
from decouple import config, Csv

# ─────────────────────────────────────────────
# Rutas base
# ─────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR.parent / 'frontend'

# ─────────────────────────────────────────────
# Seguridad
# ─────────────────────────────────────────────
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost', cast=Csv())

# ─────────────────────────────────────────────
# Aplicaciones
# ─────────────────────────────────────────────
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
]

THIRD_PARTY_APPS = [
    'django_htmx',
]

LOCAL_APPS = [
    'apps.usuarios',
    'apps.convocatorias',
    'apps.postulantes',
    'apps.parametros',
    'apps.evaluaciones',
    'apps.reportes',
    'apps.landing',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# ─────────────────────────────────────────────
# Middleware
# ─────────────────────────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
]

ROOT_URLCONF = 'config.urls'

# ─────────────────────────────────────────────
# Templates (sirve desde la carpeta frontend/)
# ─────────────────────────────────────────────
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [FRONTEND_DIR / 'templates'],
        'APP_DIRS': False,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# ─────────────────────────────────────────────
# Base de datos
# ─────────────────────────────────────────────
import os

if os.environ.get('MYSQLHOST'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ.get('MYSQLDATABASE'),
            'USER': os.environ.get('MYSQLUSER', 'root'),
            'PASSWORD': os.environ.get('MYSQLPASSWORD'),
            'HOST': os.environ.get('MYSQLHOST'),
            'PORT': os.environ.get('MYSQLPORT', '3306'),
            'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            }
        }
    }
else:
    DB_ENGINE = config('DB_ENGINE', default='sqlite')
    DB_HOST = config('DB_HOST', default='')

    if DB_ENGINE == 'mysql':
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': config('DB_NAME', default='ssd'),
                'USER': config('DB_USER', default='root'),
                'PASSWORD': config('DB_PASSWORD', default=''),
                'HOST': DB_HOST or '127.0.0.1',
                'PORT': config('DB_PORT', default='3306'),
                'OPTIONS': {
                    'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
                }
            }
        }
    elif DB_HOST:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': config('DB_NAME', default='postgres'),
                'USER': config('DB_USER', default='postgres'),
                'PASSWORD': config('DB_PASSWORD'),
                'HOST': DB_HOST,
                'PORT': config('DB_PORT', default='5432'),
            }
        }
    else:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }

# ─────────────────────────────────────────────
# Validación de contraseñas
# ─────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ─────────────────────────────────────────────
# Internacionalización - Español
# ─────────────────────────────────────────────
LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_TZ = True

# ─────────────────────────────────────────────
# Archivos estáticos y media
# ─────────────────────────────────────────────
STATIC_URL = '/static/'
STATICFILES_DIRS = [FRONTEND_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ─────────────────────────────────────────────
# Autenticación
# ─────────────────────────────────────────────
LOGIN_URL = '/usuarios/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/usuarios/login/'

# ─────────────────────────────────────────────
# Email
# ─────────────────────────────────────────────
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='admin@uagrm.edu.bo')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ─────────────────────────────────────────────
# Messages framework (para alertas Bootstrap)
# ─────────────────────────────────────────────
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.DEBUG: 'secondary',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}
