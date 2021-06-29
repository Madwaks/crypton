"""
Django settings for trade_fox project.

Generated by 'django-admin startproject' using Django 3.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

TEST_API_KEY = os.getenv("TEST_API_KEY")
TEST_SECRET_KEY = os.getenv("TEST_SECRET_KEY")


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "yl@kmjp=qoz98^*-l458f8ukf50395#u(-5t&3)-=0on^l98tq"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["51.68.230.72", "hosoda.tradefox.tech", "tradefox.tech", "127.0.0.1"]

INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"


# Application definition
# TODO: Find a way to uninstall some apps
LOCAL_APPS = [
    "crypto.apps.CryptoConfig",
    "decision_maker.apps.DecisionMakerConfig",
    "welcome_dash.apps.WelcomeDashConfig",
]

INSTALLED_APPS = [
    *LOCAL_APPS,
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_plotly_dash.apps.DjangoPlotlyDashConfig",
    "rest_framework",
    "django_filters",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_plotly_dash.middleware.BaseMiddleware",
    "django_plotly_dash.middleware.ExternalRedirectionMiddleware",
]

ROOT_URLCONF = "crypton.urls"

TRADINGBOARD_TEMPLATES = os.path.join(BASE_DIR, "trading_board/templates")
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATE_DIR, TRADINGBOARD_TEMPLATES],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",)
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [
                (os.getenv("REDIS_HOST", "127.0.0.1"), os.getenv("REDIS_PORT", "6379"))
            ]
        },
    }
}

WSGI_APPLICATION = "crypton.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRESQL_DATABASE", "crypto"),
        "USER": os.environ.get("POSTGRESQL_USERNAME", "postgresql"),
        "PASSWORD": os.environ.get("POSTGRESQL_PASSWORD", "atporder"),
        "HOST": os.environ.get("POSTGRESQL_HOST", "localhost"),
        "PORT": "5432",
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"
STATIC_DIR = os.path.join(BASE_DIR, "static")
MEDIA_ROOT = os.path.join(BASE_DIR, "static", "media")
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# STATIC_ROOT =
STATICFILES_DIRS = [BASE_DIR / "crypton" / "static"]

# DATA PATHS

CRYPTO_FOLDER_PATH: Path = Path("data/")

# DASH SETTINGS
X_FRAME_OPTIONS = "SAMEORIGIN"

PLOTLY_DASH = {
    # Route used for the message pipe websocket connection
    "ws_route": "dpd/ws/channel",
    # Route used for direct http insertion of pipe messages
    "http_route": "dpd/views",
    # Flag controlling existince of http poke endpoint
    "http_poke_enabled": True,
    # Insert data for the demo when migrating
    "insert_demo_migrations": False,
    # Timeout for caching of initial arguments in seconds
    "cache_timeout_initial_arguments": 60,
    # Name of view wrapping function
    "view_decorator": None,
    # Flag to control location of initial argument storage
    "cache_arguments": True,
    # Flag controlling local serving of assets
    "serve_locally": False,
}

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "django_plotly_dash.finders.DashAssetFinder",
    "django_plotly_dash.finders.DashComponentFinder",
    "django_plotly_dash.finders.DashAppDirectoryFinder",
]

PLOTLY_COMPONENTS = [
    # Common components
    "dash_core_components",
    "dash_html_components",
    "dash_renderer",
    # django-plotly-dash components
    "dpd_components",
    # static support if serving local assets
    "dpd_static_support",
    # Other components, as needed
    "dash_bootstrap_components",
]
CRISPY_TEPLATE_PACK = "bootstrap4"
ASGI_APPLICATION = "welcome_dash.routing.application"
