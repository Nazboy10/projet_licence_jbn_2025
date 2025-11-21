import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# Pou wè erè detaye sou Render
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console'],
#             'level': 'DEBUG',
#         },
#         'django.db.backends': {  # pou wè erè baz done
#             'handlers': ['console'],
#             'level': 'DEBUG',
#             'propagate': False,
#         },
#     },
# }

# ===========================
# SECURITY / DEBUG
# ===========================
SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-s1c^#g2mvb9sk#*7s@0)vr&d_3lt0r3fzxqg)1cq9-v0m@d7ke"
)

DEBUG = os.environ.get("DEBUG", "False") == "True"

ALLOWED_HOSTS = [
    'projet-licence-jbn-2025.onrender.com',
    '.onrender.com',  # tout subdomains Render
    'localhost',
    '127.0.0.1',
]

# ===========================
# APPLICATIONS
# ===========================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework.authtoken',

    'corsheaders',
    'SGCBA',
    'api',
    'app_inscription',
    'app_eleve',
    'app_presence',
    'app_note',
    'app_bulletin',
    'app_parametre',
    'app_classe',
    'app_journal',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ]
}

# ===========================
# MIDDLEWARE
# ===========================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",   # ← obligatwa pou static files sou Render
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

CORS_ALLOWED_ORIGINS += [
    "https://projet-licence-jbn-2025.onrender.com",
]


# ===========================
# TEMPLATE
# ===========================
ROOT_URLCONF = 'PROJET_JBN.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'SGCBA.context_processors.user_photo',
            ],
        },
    },
]

WSGI_APPLICATION = 'PROJET_JBN.wsgi.application'

# ===========================
# DATABASE
# ===========================
# ===========================
# DATABASE
# ===========================
if os.environ.get("DATABASE_URL"):
    # 🟢 MODE PRODUCTION (Render + Supabase)
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get("DATABASE_URL"),
            conn_max_age=600,
            ssl_require=False
        )
    }
else:
    # 🟡 MODE LOCAL (WampServer MySQL)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',   # Nou itilize MySQL
            'NAME': 'db_sgcba',              # Non baz done ou te kreye nan phpMyAdmin
            'USER': 'root',                         # Default user WampServer
            'PASSWORD': '',                         # Pa gen modpas pa default nan Wamp
            'HOST': '127.0.0.1',                    # Ou ka itilize localhost tou
            'PORT': '3306',                         # Pò default pou MySQL
        }
    }

# ===========================
# MEDIA FILES
# ===========================
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ===========================
# STATIC FILES (RENDER)
# ===========================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ===========================
# AUTH PASSWORD VALIDATION
# ===========================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# ===========================
# INTERNATIONALIZATION
# ===========================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ===========================
# DEFAULT PRIMARY KEY
# ===========================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ===========================
# EMAIL (GMAIL)
# ===========================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'collegebellangelot5@gmail.com'
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD', '')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
