from enum import Enum
import logging
import colorlog

# set up logging
logger = logging.getLogger(__name__)
# Define log colors
cformat = "%(log_color)s%(levelname)s:  %(message)s"
colors = {
    "DEBUG": "cyan",
    "INFO": "green",
    "WARNING": "yellow",
    "ERROR": "red",
    "CRITICAL": "red,bg_white",
}
# Set up stream handler
stream_handler = logging.StreamHandler()
stream_formatter = colorlog.ColoredFormatter(cformat, log_colors=colors)
stream_handler.setFormatter(stream_formatter)
logger.addHandler(stream_handler)
# Set up file handler
file_handler = logging.FileHandler("Akatosh.log")
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


class EventState(Enum):
    """State of the event."""

    Future = "Future"
    Current = "Current"
    Past = "Past"