import datetime
import uuid

from flask import Response

from pyqtt_application.common.http_responses import HTTPResponse
from pyqtt_application.extensions import db
from pyqtt_application.models.users_models import User


class UserController:
    @staticmethod
    def get_user(public_id):

        return User.query.filter_by(public_id=public_id).first()

    @staticmethod
    def edit_user_password(public_id, password):

        user_object = User.query.filter_by(public_id=public_id).first()
        user_object.password = password
        db.session.add(user_object)
        db.session.commit()

        return user_object

    @staticmethod
    def delete_user(public_id):

        user_obj = User.query.filter_by(public_id=public_id).first()
        db.session.delete(user_obj)
        db.session.commit()

        return user_obj

    @staticmethod
    def add_user(email: str, username: str, password: str) -> Response:

        user_object = User.query.filter_by(email=email).first()

        if not user_object:

            user_object = User(
                public_id=str(uuid.uuid4()),
                email=email,
                username=username,
                password=password,
                registered_on=datetime.datetime.utcnow(),
            )

            db.session.add(user_object)
            db.session.commit()

            return HTTPResponse.http_201_created(str(user_object))

        else:

            return HTTPResponse.http_409_already_exists(item_name=str(user_object))

    @staticmethod
    def get_all_users() -> list:

        return User.query.all()
