import sys
import logging

#LOGGING CODE
logger = logging.getLogger(conf.MOVIES)
logger.setLevel(logging.DEBUG)
# Create Formatter
formatter = logging.Formatter('%(asctime)s-%(levelname)s-FUNC:%(funcName)s-LINE:%(lineno)d: %(message)s')
# create a file handler and add it to logger
file_handler = logging.FileHandler(conf.LOG)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
# file handler
stdout_log = logging.FileHandler(conf.STDOUT_LOG)
stdout_log.setLevel(logging.INFO)
stdout_log.setFormatter(formatter)
logger.addHandler(stdout_log)
#2 - Stream also in SYS OUTPUT
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

#logger.debug("Start get movie list")
#logger.info(f'f"Retrieved: movie {i + 1} url :  {movie_url}"')
#logger.critical("No movie url was available")
#logger.debug(f"{i + 1} - {name} - {di_text}")
