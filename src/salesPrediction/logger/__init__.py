# https://www.youtube.com/watch?v=gsa1oFn9n0M
import os
import sys
import logging

logging_str = "[%(asctime)s] %(name)s:%(levelname)s:: %(module)s:%(filename)s:%(funcName)s() => %(message)s"
LOG_DIR = "logs"
LOG_FILE = "running_logs.log"
LOG_FILEPATH = os.path.join(LOG_DIR, LOG_FILE)
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format=logging_str,
    handlers=[  # as we want to print on terminal as well as in file
        logging.FileHandler(LOG_FILEPATH),
        logging.StreamHandler(sys.stdout),
    ],
)

logger = logging.getLogger("salesPrediction")
