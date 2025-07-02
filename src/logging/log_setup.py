import logging

from src.configurations import config


def setup_logging():
    config.log_path.mkdir(exist_ok=True)
    logging.basicConfig(
        level=config.log_level,
        format=config.log_format,
        handlers=[
            logging.FileHandler(config.log_file_path),
            logging.StreamHandler()
        ]
    )


def get_logger(name: str) -> logging.getLogger:
    return logging.getLogger(name)


setup_logging()
