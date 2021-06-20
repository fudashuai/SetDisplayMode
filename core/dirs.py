#!/usr/bin/env/python3
# -*- coding:utf-8 -*-

from pathlib import Path

pwd = Path(__file__).resolve()
root_dir = pwd.parent.parent
conf_dir = root_dir / 'conf'
log_dir = root_dir / 'log'
output_dir = root_dir / 'output'
source_dir = root_dir / 'source'
