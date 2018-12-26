import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
    handlers=[logging.StreamHandler()])

def log(msg):
    """Wrapper around the 'info' log level from standard logging library"""
    logging.getLogger().info(msg)
