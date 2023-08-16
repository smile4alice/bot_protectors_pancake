import os
import logging

from colorlog import ColoredFormatter


def _create_logger() -> logging:
    "Executes the configuration and creates an instance of the logger"

    os.makedirs(os.path.join(".logs"), exist_ok=True)
    logs_level = logging.DEBUG
    logs_file_level = logging.DEBUG
    logs_format = "%(levelname)-8s| %(asctime)-9s| %(message)s"
    logs_file_date_format = "%H:%M:%S"
    logs_file_path = os.path.join(".logs", "log_data.log")
    logs_colors = {
        "DEBUG": "blue",
        "INFO": "green",
        "WARNING": "cyan",
        "ERROR": "yellow",
        "CRITICAL": "red",
    }

    logger = logging.getLogger()
    logger.setLevel(logs_level)

    file_handler = logging.FileHandler(logs_file_path, mode="w", encoding="utf-8")
    file_handler.setLevel(logs_file_level)
    file_handler.setFormatter(logging.Formatter(logs_format, logs_file_date_format))

    formatter = ColoredFormatter("%(log_color)s" + logs_format, logs_file_date_format, log_colors=logs_colors)

    console_hanlder = logging.StreamHandler()
    console_hanlder.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_hanlder)
    return logger


logger = _create_logger()  # the singleton instance of logging

if __name__ == "__main__":
    logger.info("test info")
    logger.warning("test warn")
    logger.critical("test critical")
