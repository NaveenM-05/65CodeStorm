import logging
import os

# Define the log file path relative to this file
LOG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "service_request.log")

# Create a logger with a specified name
logger = logging.getLogger("service_request")
logger.setLevel(logging.INFO)

# To avoid adding duplicate handlers if this module is imported multiple times,
# check if there are already any handlers attached.
if not logger.handlers:
    # Create a file handler that logs messages to the log file
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setLevel(logging.INFO)
    
    # Define a formatter that includes timestamp, log level, and message
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    
    # Add the file handler to the logger
    logger.addHandler(file_handler)

def log_service_request(message: str):
    """
    Logs a message at INFO level to the service_request.log file.
    """
    logger.info(message)
