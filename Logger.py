import logging
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
        self.filename = filename
        self.level = level

        # Set the logging level.
        if level == 'DEBUG':
            level = logging.DEBUG
        elif level == 'INFO':
            level = logging.INFO
        elif level == 'WARNING':
            level = logging.WARNING
        elif level == 'ERROR':
            level = logging.ERROR
        elif level == 'CRITICAL':
            level = logging.CRITICAL
        else:
            raise ValueError('Invalid logging level: {}'.format(level))

        # Configure the logging format.
        logging.basicConfig(level=level,
                             format='%(asctime)s %(levelname)s %(message)s',
                             filename=filename,
                             filemode='w')

        # Log that the logger has been initialized.
        self.info('Log Initiated')

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