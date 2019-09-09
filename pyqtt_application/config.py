"""
Flask config file where most of the environment variables are set.
"""
import os

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(r'C:/workspace/mqttpyAdmin/test.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
JSON_SORT_KEYS = False
