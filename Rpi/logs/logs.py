import logging


class Logs(object):

    def __init__(self):
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        self.pimain = self.setup_logger(name='pimain', log_file='logs/pimain.log', formatter=formatter)
        self.cloudcomm = self.setup_logger(name='cloudcomm', log_file='logs/cloudcomm.log', formatter=formatter)
        self.serialcomm = self.setup_logger(name='serialcomm', log_file='logs/serialcomm.log', formatter=formatter)
        self.spectrometer = self.setup_logger(name='spectrometer', log_file='logs/spectrometer.log',
                                              formatter=formatter)

    def setup_logger(self, name, log_file, formatter, level=logging.INFO):
        handler = logging.FileHandler(log_file)
        handler.setFormatter(formatter)

        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(handler)

        return logger


logs = Logs()
