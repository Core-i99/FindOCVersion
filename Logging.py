import logging
import os
import platform
import sys
from logging import handlers

if platform.system() == "Darwin":
    lib_logs = os.path.join(
            os.path.expanduser("~"),
            "Library",
            "Logs"
    )    

elif platform.system() == "Windows":
    appdata_local = os.getenv("LOCALAPPDATA")
    lib_logs = os.path.join(appdata_local, 'FindOCVersion')
    if not os.path.exists(lib_logs):
        try:
            os.mkdir(lib_logs)
        except Exception: 
            print("Failed to create log dir")
            sys.exit()     

else:
    print("This OS is currently not supported")
    sys.exit()

# Basic formats.
logformat = "%(asctime)s - %(levelname)s - %(message)s"
date = "%m/%d/%Y %I:%M:%S %p"

# Adding the base log handlers.
handler = logging.getLogger()
rotating = handlers.RotatingFileHandler(os.path.join(lib_logs, "FindOCVersion.log"), mode="a", maxBytes=2 ** 13)

# Add the RotatingFileHandler to the default logger.
handler.addHandler(rotating)
rotating.setFormatter(
    logging.Formatter(
        logformat, datefmt=date
    )
)

def critical(message):
    handler.setLevel(logging.CRITICAL)
    logging.critical(message)

def error(message):
    handler.setLevel(logging.ERROR)
    logging.error(message)

def info(message):
    handler.setLevel(logging.INFO)
    logging.info(message)

def warning(message):
    handler.setLevel(logging.WARNING)
    logging.warning(message)
