"""
Fonctionnalités de log
"""
import logging

logging.basicConfig(filename='std.log', filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)