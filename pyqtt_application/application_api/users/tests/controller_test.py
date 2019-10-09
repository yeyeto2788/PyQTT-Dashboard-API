import logging
from unittest import TestCase, mock

from pyqtt_application.application_api.users.controller import UserController


class TestUserController(TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Global setUp.
        """

        logging.basicConfig(level=logging.INFO)

    @mock.patch("pyqtt_application.application_api.users.controller.User")
    @mock.patch("pyqtt_application.application_api.users.controller.db")
    def test_get_user(self, db_mock, user_mock):
        session_mock = mock.Mock()
        session_mock.add.return_value = True
        session_mock.commit.return_value = True
        db_mock.session.return_value = session_mock

        expected = "LocoUser"
        user_mock.query.filter_by.return_value.first.return_value = expected

        obtained = UserController.get_user("crazyid")

        self.assertEqual(
            expected,
            obtained,
            msg=f"Expected: {expected}, Obtained: {obtained}",
        )

    @mock.patch("pyqtt_application.application_api.users.controller.User")
    @mock.patch("pyqtt_application.application_api.users.controller.db")
    def test_edit_user_password(self, db_mock, user_mock):
        session_mock = mock.Mock()
        session_mock.add.return_value = True
        session_mock.commit.return_value = True
        db_mock.session.return_value = session_mock

        user_id = "crazyid"
        user_obj_mock = mock.Mock()
        user_obj_mock.password = "oldpassword"
        user_obj_mock.__str__ = user_id
        user_obj_mock.query.filter_by.return_value.first.return_value = (
            "crazyid"
        )
        user_mock.return_value = user_obj_mock

        user = UserController.edit_user_password(
            public_id="crazyid", password="newpassword"
        )

        self.assertEqual(
            "newpassword",
            user.password,
            msg=f"Expected: {'newpassword'}, Obtained: {user.password}",
        )
        db_mock.session.add.assert_called_once()
        db_mock.session.commit.assert_called_once()

    @mock.patch("pyqtt_application.application_api.users.controller.User")
    @mock.patch("pyqtt_application.application_api.users.controller.db")
    def test_delete_user(self, db_mock, user_mock):
        session_mock = mock.Mock()
        session_mock.delete.return_value = True
        session_mock.commit.return_value = True
        db_mock.session.return_value = session_mock

        expected = "LocoUser"
        user_mock.query.filter_by.return_value.first.return_value = expected

        UserController.delete_user("crazyid")

        db_mock.session.delete.assert_called_once()
        db_mock.session.commit.assert_called_once()

    @mock.patch(
        "pyqtt_application.application_api.users.controller.HTTPResponse"
    )
    @mock.patch("pyqtt_application.application_api.users.controller.User")
    @mock.patch("pyqtt_application.application_api.users.controller.db")
    def test_add_user_abnormal(self, db_mock, user_mock, response_mock):
        session_mock = mock.Mock()
        session_mock.add.return_value = True
        session_mock.commit.return_value = True
        db_mock.session.return_value = session_mock

        user_id = "crazyid"
        user_obj_mock = mock.Mock()
        user_obj_mock.password = "oldpassword"
        user_obj_mock.__str__ = mock.Mock()
        user_obj_mock.__str__.return_value = user_id
        user_mock.query.filter_by.return_value.first.return_value = (
            user_obj_mock
        )

        expected = {"NOK": 404}
        response_mock.http_409_already_exists.return_value = expected

        obtained = UserController.add_user(
            email="test@test.com", username="test", password="test"
        )

        response_mock.http_409_already_exists.assert_called_once()

        self.assertEqual(
            expected,
            obtained,
            msg=f"Expected: {expected}, Obtained: {obtained}",
        )

    @mock.patch(
        "pyqtt_application.application_api.users.controller.HTTPResponse"
    )
    @mock.patch("pyqtt_application.application_api.users.controller.User")
    @mock.patch("pyqtt_application.application_api.users.controller.db")
    def test_add_user(self, db_mock, user_mock, response_mock):
        session_mock = mock.Mock()
        session_mock.add.return_value = True
        session_mock.commit.return_value = True
        db_mock.session.return_value = session_mock

        user_mock.query.filter_by.return_value.first.return_value = None

        expected = {"OK": 200}
        response_mock.http_201_created.return_value = expected

        obtained = UserController.add_user(
            email="test@test.com", username="test", password="test"
        )

        response_mock.http_201_created.assert_called_once()

        self.assertEqual(
            expected,
            obtained,
            msg=f"Expected: {expected}, Obtained: {obtained}",
        )

        db_mock.session.add.assert_called_once()
        db_mock.session.commit.assert_called_once()

    @mock.patch("pyqtt_application.application_api.users.controller.User")
    @mock.patch("pyqtt_application.application_api.users.controller.db")
    def test_get_all_users(self, db_mock, user_mock):
        session_mock = mock.Mock()
        session_mock.add.return_value = True
        session_mock.commit.return_value = True
        db_mock.session.return_value = session_mock

        expected = ["User1", "User2"]

        user_mock.query.all.return_value = expected

        obtained = UserController.get_all_users()

        self.assertEqual(
            expected,
            obtained,
            msg=f"Expected: {expected}, Obtained: {obtained}",
        )
