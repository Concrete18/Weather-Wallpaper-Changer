from logging.handlers import RotatingFileHandler
import logging as lg
import requests, time


class Logger:
    log_formatter = lg.Formatter(
        "%(asctime)s %(levelname)s %(message)s", datefmt="%m-%d-%Y %I:%M:%S %p"
    )
    logger = lg.getLogger(__name__)
    logger.setLevel(lg.DEBUG)  # Log Level
    max_bytes = 5 * 1024 * 1024
    log_path = "release.log"
    my_handler = RotatingFileHandler(log_path, maxBytes=max_bytes, backupCount=2)
    my_handler.setFormatter(log_formatter)
    logger.addHandler(my_handler)


class Helper(Logger):
    def request_url(self, url, headers=None, log=True):
        """
        Quick data request with check for success.
        """
        try:
            response = requests.get(url, headers=headers)
        except requests.exceptions.ConnectionError:
            msg = "Connection Error: Internet can't be accessed"
            if log:
                self.logger.warning(msg)
            return False
        if response.status_code == requests.codes.ok:
            return response
        elif response.status_code == 500:
            msg = "Server Error: make sure your api key and steam id is valid."
            if log:
                self.logger.warning(msg)
        elif response.status_code == 404:
            msg = f"Server Error: 404 Content moved or was deleted. URL: {url}"
            if log:
                self.logger.warning(msg)
        elif response.status_code == 429:
            msg = "Server Error: Too Many reqeuests made. Waiting to try again."
            if log:
                self.logger.warning(msg)
                self.logger.warning(response)
            time.sleep(5)
            self.request_url(url, headers=None)
        else:
            msg = f"Unknown Error: {response.status_code}"
            if log:
                self.logger.warning(msg)
        return False
