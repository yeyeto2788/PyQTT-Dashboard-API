"""
Flask server run
"""
import os
import pprint
import threading
from pathlib import Path
from random import randrange

from flask_script import Manager, prompt_bool
from waitress import serve

from pyqtt_application.app import create_app, db
from pyqtt_application.models.messages_models import Message
from pyqtt_application.sql_logger import record_messages

app = create_app()
# app.app_context().push()
manager = Manager(
    app,
    with_default_commands=False
)
db_manager = Manager(usage="Database operations (create, drop, recreate)")
dev_manager = Manager(usage="Development operations.")


@db_manager.command
def create():
    """
    Create database.
    """
    db.create_all()


@db_manager.command
def drop():
    """
    Delete data on database.
    """
    if prompt_bool("Are you sure you want to lose all your data?"):
        db.drop_all()


@db_manager.command
def recreate():
    """
    Delete data and create database.
    """
    drop()
    create()


@db_manager.command
def populate():
    for _ in range(100):
        message = Message(topic='/test/temp', message=str(randrange(20, 42)), client='',
                          user_data='')
        db.session.add(message)

    db.session.commit()


@manager.command
def runserver(host, port, topic):
    """
    Start recording messages from the MQTT broker and the server at the same time.
    """

    record_options = dict(
        host=host,
        port=port if port else 1883,
        topic=topic if topic else 'test.mosquitto.org'
    )

    record_thread = threading.Thread(target=record_messages, kwargs=record_options, daemon=True)

    record_thread.start()
    serve(app, port=8080)


@dev_manager.command
def show():
    """
    Show all available endpoints of the application.

    """
    routes = list(app.url_map.iter_rules())

    found_routes = dict()
    pretty_printer = pprint.PrettyPrinter(indent=4)

    for index, route in enumerate(routes):
        found_routes[index + 1] = dict(
            name=route.endpoint,
            route=str(route),
            methods=[method for method in route.methods],
        )

    pretty_printer.pprint(found_routes)


@dev_manager.command
def run():
    """
    Start the server on development mode.
    """

    db_path = Path(Path.cwd() / 'dev_test.db').absolute()
    db_existence = "exists" if db_path.exists() else "doesn't exists"
    msg = f"The database '{db_path}' \n{db_existence}, want to recreate it?"

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + str(db_path)
    app.config['ENV'] = 'development'
    app.config['DEBUG'] = True

    if prompt_bool(msg):

        if not os.path.exists(db_path):
            create()
            populate()

        else:
            drop()
            create()
            populate()

    record_options = dict(
        host='iot.eclipse.org',
    )
    record_thread = threading.Thread(target=record_messages, kwargs=record_options, daemon=True)
    record_thread.start()

    app.run(host='127.0.0.1', port=8080, debug=True, use_reloader=False)


if __name__ == "__main__":
    manager.add_command('db', db_manager)
    manager.add_command('dev', dev_manager)
    manager.run()
