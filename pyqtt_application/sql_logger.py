"""
Base logger for MQTT messages that it is triggered when a message is
received calling the callback function `on_message` and adding the messages
into the database.
"""
import uuid
from datetime import datetime

import paho.mqtt.client as mqtt
import sqlalchemy

from pyqtt_application.config import SQLALCHEMY_DATABASE_URI


def on_message(client: mqtt.Client, userdata, message):
    """Callback function to be executed when a message is received

    In this case we're adding all data on a table

    Args:
        client: mqtt.Client object.
        userdata: data passed to this callback function.
        message:

    """

    engine = sqlalchemy.create_engine(SQLALCHEMY_DATABASE_URI)
    connection = engine.connect()
    metadata = sqlalchemy.MetaData()
    messaje_table = sqlalchemy.Table('message', metadata, autoload=True, autoload_with=engine)

    topic = str(message.topic),
    message = message.payload.decode('utf-8'),
    user_data = str(userdata),
    client = str(client)
    timestamp = datetime.utcnow()

    try:
        sql_query = sqlalchemy.insert(messaje_table).values(
            topic=topic,
            message=message,
            datetime=timestamp,
            client=client,
            user_data=user_data
        )
        connection.execute(sql_query)

    except Exception as e:
        print(f'An error occurred trying to add a message to db: {e.__str__()}')

    finally:
        connection.close()


def record_messages(host: str = 'test.mosquitto.org', port: str = 1883, topic: str = '/#'):
    """Main function to connect and set a callback function to execute on each message received.

    Start the MQTT client and add the option to call the function `on_message` in order to
    add the message received on the database.

    This client will connect to the `host` and `port` set by argument and listening to a
    given topic on the broker, if this function is called with no parameters then the host
    will be 'test.mosquitto.org' and the default port will be 1883 listening to all topics.

    Args:
        host: IP or domain of the MQTT broker.
        port: MQTT broker port.
        topic: Topic to subscribe to.

    """
    print(f'host: {host}, port: {port}, topic: {topic}')
    client_name = str(uuid.uuid1())

    client = mqtt.Client(client_id=client_name)
    client.on_message = on_message

    try:
        client.connect(host=host, port=port)

    except TimeoutError:
        print(f"An error occurred trying to connect to '{host}' at '{port}'")

    else:
        client.subscribe(topic, 0)

        client.loop_forever()

    finally:
        client.loop_stop()
