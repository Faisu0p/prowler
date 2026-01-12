# from config.env import env

# VALKEY_HOST = env("VALKEY_HOST", default="valkey")
# VALKEY_PORT = env("VALKEY_PORT", default="6379")
# VALKEY_DB = env("VALKEY_DB", default="0")

# CELERY_BROKER_URL = f"redis://{VALKEY_HOST}:{VALKEY_PORT}/{VALKEY_DB}"
# CELERY_RESULT_BACKEND = "django-db"
# CELERY_TASK_TRACK_STARTED = True

# CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

# CELERY_DEADLOCK_ATTEMPTS = env.int("DJANGO_CELERY_DEADLOCK_ATTEMPTS", default=5)


from config.env import env

VALKEY_HOST = env("VALKEY_HOST")
VALKEY_PORT = env("VALKEY_PORT", default="6380")
VALKEY_DB = env("VALKEY_DB", default="0")
VALKEY_PASSWORD = env("VALKEY_PASSWORD")

CELERY_BROKER_URL = (
    f"rediss://:{VALKEY_PASSWORD}@" f"{VALKEY_HOST}:{VALKEY_PORT}/{VALKEY_DB}"
)

# You are using django-celery-results → this is fine
CELERY_RESULT_BACKEND = "django-db"

CELERY_TASK_TRACK_STARTED = True
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

CELERY_BROKER_USE_SSL = {
    "ssl_cert_reqs": "required",
}

CELERY_REDIS_BACKEND_USE_SSL = {
    "ssl_cert_reqs": "required",
}

CELERY_DEADLOCK_ATTEMPTS = env.int("DJANGO_CELERY_DEADLOCK_ATTEMPTS", default=5)
