import logging
from pathlib import Path
cleaners = {}

class Logger:
    """This class implements a logger that can be used to log messages to a file.

    Attributes:
        filename (str): The name of the file to log to.
        level (str): The logging level. Valid levels are `DEBUG`, `INFO`, `WARNING`, `ERROR`, and `CRITICAL`.

    Methods:
        info(message): Log a message at the `INFO` level.
        debug(message): Log a message at the `DEBUG` level.
        error(message): Log a message at the `ERROR` level.
        critical(message): Log a message at the `CRITICAL` level.
        warning(message): Log a message at the `WARNING` level.
        close(): Close the log file.
    """

    def __init__(self, filename, level='INFO'):
        """Initialize the logger.

        Args:
            filename (str): The name of the file to log to.
            level (str): The logging level. Valid levels are `DEBUG`, `INFO`, `WARNING`, `ERROR`, and `CRITICAL`.
        """
        log_file_path = Path(filename)
        log_file_path.parent.mkdir(parents=True, exist_ok=True)

        self.logger = logging.getLogger(str(log_file_path))
        self.logger.setLevel(getattr(logging, level))
        self.logger.propagate = False

        if not self.logger.handlers:
            handler = logging.FileHandler(log_file_path, encoding="utf-8")
            formatter = logging.Formatter(
                "%(asctime)s | %(levelname)s | %(message)s"
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

        # Log that the logger has been initialized.
        self.logger.info('Log Initiated')

    def info(self, message):
        """Log a message at the `INFO` level.

        Args:
            message (str): The message to log.
        """
        logging.info(message)

    def debug(self, message):
        """Log a message at the `DEBUG` level.

        Args:
            message (str): The message to log.
        """
        logging.debug(message)

    def error(self, message):
        """Log a message at the `ERROR` level.

        Args:
            message (str): The message to log.
        """
        logging.error(message)

    def critical(self, message):
        """Log a message at the `CRITICAL` level.

        Args:
            message (str): The message to log.
        """
        logging.critical(message)

    def warning(self, message):
        """Log a message at the `WARNING` level.

        Args:
            message (str): The message to log.
        """
        logging.warning(message)

    def close(self):
        """Close the log file.
        """
        logging.shutdown()