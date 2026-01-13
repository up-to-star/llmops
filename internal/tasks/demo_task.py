from config.config import celery_app
from celery import shared_task
from config.logger import get_logger
from uuid import UUID
import time

logger = get_logger(__name__)


@shared_task
def demo_task(id: UUID):
    logger.info("sleep 5s")
    time.sleep(5)
    logger.info(f"demo task {id} done")
    logger.info("sleep 5s done")

    return "demo task done"
