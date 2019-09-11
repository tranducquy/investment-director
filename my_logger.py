import os
import time
import datetime
import json
from logging import config, getLogger

class Logger :
    logger = None
    def myLogger(self, name='test'):
        if None == self.logger:
            config.dictConfig(json.loads(open(os.path.dirname(os.path.abspath(__file__)) + "config_log.json", encoding='UTF-8').read()))
            self.logger = getLogger(name)
        return self.logger

