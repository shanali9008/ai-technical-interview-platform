import logging

_LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

_logger = logging.getLogger("AI Technical Interview Platform")

# Guard against duplicate handlers if this module gets imported multiple times
# (e.g. by uvicorn's --reload, or multiple modules importing it independently).
if not _logger.handlers:
    _logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(_LOG_FORMAT, datefmt=_DATE_FORMAT))

    _logger.addHandler(console_handler)
    _logger.propagate = False  # don't double-log via the root logger

logger = _logger