from config.env import env

VALKEY_HOST = env("VALKEY_HOST", default="valkey")
VALKEY_PORT = env("VALKEY_PORT", default="6379")
VALKEY_DB = env("VALKEY_DB", default="0")
VALKEY_PASSWORD = env("VALKEY_PASSWORD", default="")

# Azure Redis Cache requires SSL (rediss://) on port 6380
# Local development uses plain redis:// on port 6379
if VALKEY_PASSWORD:
    # Azure Redis with SSL
    CELERY_BROKER_URL = f"rediss://:{VALKEY_PASSWORD}@{VALKEY_HOST}:{VALKEY_PORT}/{VALKEY_DB}?ssl_cert_reqs=required"
else:
    # Local development without SSL
    CELERY_BROKER_URL = f"redis://{VALKEY_HOST}:{VALKEY_PORT}/{VALKEY_DB}"

CELERY_RESULT_BACKEND = "django-db"
CELERY_TASK_TRACK_STARTED = True

CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

CELERY_DEADLOCK_ATTEMPTS = env.int("DJANGO_CELERY_DEADLOCK_ATTEMPTS", default=5)
