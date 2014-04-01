#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
André Silva 1st April 2014  
'''

LOG_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': ('%(asctime)s [%(process)d] [%(levelname)s] ' +
                       'pathname=%(pathname)s lineno=%(lineno)s ' +
                       'funcname=%(funcName)s %(message)s'),
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': 'lineno=%(lineno)s funcname=%(funcName)s %(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'root': {
            'handlers': ['console'],
            'level':'DEBUG'
    },
}

import logging
from logging.config import dictConfig
dictConfig(LOG_CONFIG)
logger = logging.getLogger()
