"""
Simple hello world flow for testing Prefect setup.
"""
from prefect import flow
from prefect.logging import get_run_logger


@flow(name="hello_world", log_prints=True)
def hello():
    """
    Simple hello world flow for testing Prefect setup.
    """
    logger = get_run_logger()
    logger.info("=" * 60)
    logger.info("Hello World Flow")
    logger.info("=" * 60)
    logger.info("Prefect is working correctly!")
    logger.info("=" * 60)
    return "Hello from Prefect!"
