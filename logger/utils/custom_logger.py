from logging import getLogger, config
import json
from configparser import ConfigParser
import os


class Logger():

    def get_logger(self, logger_name='Default'):
        logger = getLogger(logger_name)
        return logger

    def read_conf_file(self, file_name='conf/conf.json'):
        with open(file_name, 'r', encoding='utf-8') as f:
            f_ = json.load(f)
            config.dictConfig(f_)

#実行方法    
# exec_file_name =  os.path.basename(__file__)[:-3]
# log_obj = Logger()
# log_obj.read_conf_file()
# logger = log_obj.get_logger(exec_file_name)
# logger.warning('hogheoge')