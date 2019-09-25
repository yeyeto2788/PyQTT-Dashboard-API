from pyqtt_application.extensions import celery


@celery.task(bind=True)
def stop_task(self, task_id: str):
    """
    Stop a task by its given id.

    Args:
        self:
        task_id: Id of the task to be stopped.

    """
    celery.control.revoke([task_id], terminate=True)
