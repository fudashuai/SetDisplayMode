#!/usr/bin/env/python3
# -*- coding:utf-8 -*-

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def log(log_dir,
        log_filename=None,
        log_level=logging.DEBUG,
        log_maxBytes=5 * 1024 * 1024,
        backupCount=5):
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)

    if not logger.handlers:
        root_dir_name = Path(__file__).resolve().parent.parent.stem
        level_dict = logging._levelToName
        filename = log_filename or root_dir_name
        logfile = f'{filename}-{level_dict[log_level]}.log'
        log_path = Path(log_dir, logfile)

        ch = logging.StreamHandler()
        fh = RotatingFileHandler(log_path,
                                 encoding='utf-8',
                                 maxBytes=log_maxBytes,
                                 backupCount=backupCount)

        if log_level == logging.DEBUG:
            formatter = logging.Formatter(
                fmt=
                '%(asctime)s-%(levelname)s-%(module)s-%(lineno)d  %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S')
        else:
            formatter = logging.Formatter(
                fmt='%(asctime)s-%(levelname)s  %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S')

        ch.setFormatter(formatter)
        ch.setLevel(log_level)
        fh.setFormatter(formatter)
        fh.setLevel(log_level)

        logger.addHandler(ch)
        logger.addHandler(fh)

    return logger


if __name__ == '__main__':
    log_dir = Path(__file__).parent / 'log'
    log_dir.mkdir(exist_ok=True, parents=True)
    logger = log(log_dir)

    logger.debug('debug info')
    logger.info('info info')
    logger.warning('warning info')
    logger.error('error info')
    logger.critical('critical info')
