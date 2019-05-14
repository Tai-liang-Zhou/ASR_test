# coding=UTF-8
'''
Created on 2016年11月10日

@author: chingyu
'''
import os
import logging.config

def setup_logging(conf):
    log_dict = {
        'version': 1,
        'disable_existing_loggers': False,
        'root': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'detail',
                'level': conf['verbose']
            },
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'detail',
                'level': conf['verbose'],
                'filename': '%s/info.log' % conf['log_path'],
                'maxBytes': 10 * 1024 * 1024,
                'backupCount': 10
            }
        },
        'formatters': {
            'detail': {
                'format': u'[%(asctime)s][%(process)d][%(threadName)10.10s]'
                '[%(levelname).1s][%(filename)s:%(funcName)s:%(lineno)s] :'
                ' %(message)s'
            },
            'simple': {
                'format': u'[%(asctime)s][%(process)d][%(threadName)10.10s]'
                '[%(levelname).1s][%(filename)s:%(lineno)s] : %(message)s'
            }
        }
    }
    if not os.path.exists(conf['log_path']):
        os.makedirs(conf['log_path'])
    logging.config.dictConfig(log_dict)