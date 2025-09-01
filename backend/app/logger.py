import logging

# Custom colored formatter
class ColorFormatter(logging.Formatter):
    COLORS = {
        "WARNING": "\033[93m",  # Yellow
        "INFO": "\033[92m",  # Green
        "DEBUG": "\033[94m",  # Blue
        "CRITICAL": "\033[91m",  # Red
        "ERROR": "\033[91m",  # Red
        "ENDC": "\033[0m",  # Reset
    }

    def format(self, record):
        # keep original levelname to restore it after formatting
        original_levelname = record.levelname
        color = self.COLORS.get(original_levelname, self.COLORS["ENDC"])
        # color only the level name
        record.levelname = f"{color}{original_levelname}{self.COLORS['ENDC']}"
        try:
            return super().format(record)
        finally:
            record.levelname = original_levelname


class Logger:
    def __init__(self, app_name, log_level=logging.INFO, log_file=None):
        """
        Initializes the logger instance.

        Args:
            app_name (str): Name of the application.
            log_level (int, optional): The logging level (default: INFO).
            log_file (str, optional): Path to the log file (default: None).
        """
        self.logger = logging.getLogger(app_name)
        self.logger.setLevel(log_level)
        self.logger.propagate = False

        # Only add handlers if the logger doesn't already have any
        # This prevents duplicate handlers when the module is imported multiple times
        if not self.logger.handlers:
            log_format = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"

            if log_file:
                handler = logging.FileHandler(log_file)
                formatter = logging.Formatter(log_format)
            else:
                handler = logging.StreamHandler()
                formatter = ColorFormatter(log_format)

            handler.setLevel(log_level)
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def debug(self, message):
        """Logs a debug message."""
        self.logger.debug(message)

    def info(self, message):
        """Logs an information message."""
        self.logger.info(message)

    def warning(self, message):
        """Logs a warning message."""
        self.logger.warning(message)

    def error(self, message, exc_info=None):
        """Logs an error message."""
        self.logger.error(message, exc_info=exc_info)

    def critical(self, message):
        """Logs a critical message."""
        self.logger.critical(message)


logger = Logger(app_name="Backend-API")
