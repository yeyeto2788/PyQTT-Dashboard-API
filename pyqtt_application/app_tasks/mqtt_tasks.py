from pyqtt_application.extensions import celery
from pyqtt_application.sql_logger import record_messages


@celery.task(bind=True)
def start_recording(self):
    """
    First version to check whether this is launched on celery.
    """
    print('Start recording')
    record_messages()


@celery.task(bind=True)
def stop_task(task_id: str):
    """
    Stop a task by its given id.

    Args:
        task_id: Id of the task to be stopped.

    """
    celery.control.revoke(task_id, terminate=True)
