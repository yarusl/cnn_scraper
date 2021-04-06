import sys
import settings
import logging

#LOGGING CODE
logger = logging.getLogger(settings.NYTname)
logger.setLevel(logging.DEBUG)

# Create Formatter
formatter = logging.Formatter('%(asctime)s-%(levelname)s-FUNC:%(funcName)s-LINE:%(lineno)d: %(message)s')

if not settings.DEMO:
    # create a file handler and add it to logger
    file_handler = logging.FileHandler(settings.LOG)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

# Stream also in SYS OUTPUT
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

