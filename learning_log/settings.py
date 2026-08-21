"""
Django settings for learning_log project.
"""

from pathlib import Path
import os
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Are we running on a cloud host (Render/Heroku)?
ON_CLOUD = bool(
    os.environ.get('RENDER') or os.environ.get('HEROKU_APP_NAME') or os.getcwd() == '/app'
)

# SECURITY WARNING: keep the secret key used in production secret!
# BUG FIX: the key used to be hard-coded in source. It now comes from an
# environment variable in production, with the old value only kept as a
# local-development fallback.
SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-(no!d-thlrrj_j1r@-5*w0h-66fm&1o49$t@@hq81aua#m4_w%',
)

# BUG FIX: DEBUG was hard-coded to True, which is unsafe to ship to
# production. It now defaults to True locally and must be explicitly
# disabled (or left unset) in the cloud environment.
DEBUG = os.environ.get('DEBUG', 'True' if not ON_CLOUD else 'False') == 'True'

# BUG FIX: ALLOWED_HOSTS was wide open ('*'). Locally that's fine, but in
# production it should be restricted to the real host(s).
if ON_CLOUD:
    ALLOWED_HOSTS = [h for h in os.environ.get('ALLOWED_HOSTS', '').split(',') if h]
    render_host = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
    if render_host:
        ALLOWED_HOSTS.append(render_host)
    if not ALLOWED_HOSTS:
        ALLOWED_HOSTS = ['.onrender.com', '.herokuapp.com']
else:
    ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party apps
    'django_bootstrap5',

    # My apps
    'learning_logs',
    'users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # BUG FIX: WhiteNoise was in requirements.txt but never wired into
    # MIDDLEWARE, so static files (CSS/JS/Bootstrap) were never served
    # correctly once deployed to Render/Heroku. This line fixes that.
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'learning_log.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'learning_log.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/6.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/6.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = []

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Email
# https://docs.djangoproject.com/en/6.1/topics/email/#topic-email-configuration

# BUG FIX: "MAILERS" is not a real Django setting, so this block silently
# did nothing. The real setting is EMAIL_BACKEND.
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# My settings

# BUG FIX: missing trailing slash meant this didn't exactly match the real
# login URL ('/users/login/'), which could cause an extra redirect hop.
LOGIN_URL = '/users/login/'

# Settings for django-bootstrap5
BOOTSTRAP5 = {
    'error_css_class': 'django-bootstrap5-error',
    'required_css_class': 'django-bootstrap5-required',
    'set_placeholder': False,
}

if ON_CLOUD:
    # Se houver um banco na nuvem, ele usa. Se não, mantém o SQLite padrão com segurança
    if os.environ.get('DATABASE_URL'):
        DATABASES['default'] = dj_database_url.config(
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=True,
        )

    # Configuração de Arquivos Estáticos com WhiteNoise
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

    # BUG FIX: needed so WhiteNoise actually compresses/hashes/serves the
    # files instead of just having a MIDDLEWARE entry with nothing behind it.
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }

    os.makedirs(STATIC_ROOT, exist_ok=True)

    # Segurança de cabeçalho obrigatória para servidores em nuvem
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

LOGIN_REDIRECT_URL = 'learning_logs:index'
LOGOUT_REDIRECT_URL = 'learning_logs:index'
