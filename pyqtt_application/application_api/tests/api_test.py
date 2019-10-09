import os
import logging
import unittest

from pyqtt_application.app import create_app


class TestAppEndPoints(unittest.TestCase):
    """
    Unitary tests for utils.
    """

    @classmethod
    def setUpClass(cls):
        """
        Global setUp.
        """

        logging.basicConfig(level=logging.INFO)
        # Create dummy database
        db_file = open("./pyqtt.db", "w")
        db_file.close()

    def setUp(self):
        """
        Test setUp.
        """
        app = create_app()
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        app.config["DEBUG"] = False
        self.app = app.test_client()

    def test_root(self):
        """
        Check whether the root path is enable.

        """
        response = self.app.get("/", follow_redirects=True)
        self.assertEqual(
            response.status_code,
            404,
            msg="Expected: {}, Obtained: {}".format(404, response.status_code),
        )

    def tearDown(self):
        """
        Test tearDown.
        """

    @classmethod
    def tearDownClass(cls):
        """
        Global tearDown.
        """
        os.remove("./pyqtt.db")
