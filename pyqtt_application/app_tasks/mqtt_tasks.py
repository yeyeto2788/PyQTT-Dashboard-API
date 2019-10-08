from pyqtt_application.extensions import celery
from pyqtt_application.sql_logger import record_messages


@celery.task(bind=True)
def start_recording(self, host, port, topic):
    """
    First version to check whether this is launched on celery.
    """
    record_messages(host, port, topic)
