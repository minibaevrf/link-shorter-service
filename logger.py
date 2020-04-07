import logging
import os


class Logger:

    @staticmethod
    def create_logger():
        log_filename = 'log/logs.log'
        os.makedirs(os.path.dirname(log_filename), exist_ok=True)

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(log_filename)
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        return logger
