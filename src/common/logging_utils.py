import logging

DEFAULT_LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


def setup_logger(name, level=logging.INFO, log_file=None, log_format=None):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if log_format is None:
        log_format = DEFAULT_LOG_FORMAT
    formatter = logging.Formatter(log_format)

    # Create a console handler
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # Optionally, create a file handler
    if log_file:
        fh = logging.FileHandler(log_file)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger
