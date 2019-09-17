"""
Flask config file where most of the environment variables are set.
"""
import os

__key = os.urandom(16)  # Change this to a fix string.

__default_db = 'sqlite:///' + os.path.join(os.getcwd(), 'test.db')

SQLALCHEMY_DATABASE_URI = os.getenv("PYQTT_DATABASE_URL", __default_db)
SQLALCHEMY_TRACK_MODIFICATIONS = False
JSON_SORT_KEYS = False
JWT_SECRET_KEY = __key
SECRET_KEY = __key
CELERY_BROKER_URL = os.getenv("CELERY_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_BACKEND_URL", "redis://localhost:6379/0")
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_IMPORTS = ['pyqtt_application.app_tasks.mqtt_tasks']
CELERY_ACCEPT_CONTENT = ['json']
