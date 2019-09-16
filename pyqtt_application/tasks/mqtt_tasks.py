from pyqtt_application.extensions import celery
from pyqtt_application.sql_logger import record_messages


@celery.task(bind=True)
def start_recording(self, host, port, topic):
    """

    Args:
        self:
        host:
        port:
        topic:

    Returns:

    """

    record_messages(host=host, port=port, topic=topic)


@celery.task(bind=True)
def stop_recording(task_id: str):
    """

    Args:
        task_id:

    Returns:

    """
    celery.control.revoke(task_id, terminate=True)
