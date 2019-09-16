"""
Base logger for MQTT messages that it is triggered when a message is
received calling the callback function `on_message` and adding the messages
into the database.
"""
import uuid

import paho.mqtt.client as mqtt

from pyqtt_application.extensions import db
from pyqtt_application.models.messages_models import Message


def on_message(client: mqtt.Client, userdata, message):
    """Callback function to be executed when a message is received

    In this case we're adding all data on a table

    Args:
        client: mqtt.Client object.
        userdata: data passed to this callback function.
        message:

    """

    try:
        message = Message(
            topic=str(message.topic),
            h_message=message.payload.decode('utf-8'),
            r_message=message.payload,
            user_data=str(userdata),
            client=str(client)
        )
        db.session.add(message)
        db.session.commit()

    except Exception as e:
        print(f'An error occurred trying to add a message to db: {e.__str__()}')


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
