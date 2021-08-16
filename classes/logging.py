from logging.handlers import RotatingFileHandler
import logging as lg


class Logger:

        log_formatter = lg.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%m-%d-%Y %I:%M:%S %p')
        logger = lg.getLogger(__name__)
        logger.setLevel(lg.INFO) # Log Level
        my_handler = RotatingFileHandler('Weather_Wallpaper.log', maxBytes=5*1024*1024, backupCount=2)
        my_handler.setFormatter(log_formatter)
        logger.addHandler(my_handler)
