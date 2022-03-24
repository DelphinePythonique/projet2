"""
Fonctionnalités de log
"""
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('std.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
