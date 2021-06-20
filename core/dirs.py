#!/usr/bin/env/python3
# -*- coding:utf-8 -*-

from pathlib import Path

pwd = Path(__file__).resolve()
root_dir = pwd.parent.parent
conf_dir = root_dir / 'conf'
log_dir = root_dir / 'log'
output_dir = root_dir / 'output'
source_dir = root_dir / 'source'

dir_tuple = (conf_dir, log_dir, output_dir, source_dir)
for dir in dir_tuple:
    dir.mkdir(exist_ok=True, parents=True)
