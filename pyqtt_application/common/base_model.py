"""
Base model parent class to declarative define all the models
"""

import json

from sqlalchemy.ext.declarative import declarative_base

BASE = declarative_base()


class BaseModel(BASE):
    """
    Extended SQLAlchemy model with common methods for all models
    """

    __abstract__ = True

    def __repr__(self):
        row_dict = {
            col.name: str(getattr(self, col.name)) for col in self.__table__.columns
        }
        return json.dumps(row_dict)
