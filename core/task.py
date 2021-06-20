#!/usr/bin/env/python3
# -*- coding:utf-8 -*-

import locale
from pathlib import Path
from subprocess import PIPE, run
from xml.etree import ElementTree as ET

from dirs import *


def create_task():
    def create_task_xml():
        xml_file = source_dir / 'SetDisplayMode.xml'
        ET.register_namespace(
            '', 'http://schemas.microsoft.com/windows/2004/02/mit/task')
        xml = ET.parse(xml_file)
        root = xml.getroot()
        for i in root.iter():
            if i.tag == '{http://schemas.microsoft.com/windows/2004/02/mit/task}Command':
                i.text = fr'{root_dir}\.venv\scripts\pythonw.exe'
            if i.tag == '{http://schemas.microsoft.com/windows/2004/02/mit/task}Arguments':
                i.text = fr'{root_dir}\core\launch.py'
        xml.write(xml_file, encoding="utf-16", xml_declaration=True)

    p = run('schtasks /query', shell=True, stdout=PIPE, stderr=PIPE)
    system_encoding = locale.getpreferredencoding()
    if 'SetDisplayMode' not in p.stdout.decode(system_encoding,
                                               errors='ignore'):
        create_task_xml()
        xml_file = source_dir / 'SetDisplayMode.xml'
        cmd = f'schtasks /create /tn SetDisplayMode /xml {xml_file}'
        run(cmd, shell=True, stdout=PIPE, stderr=PIPE)


def start_task():
    cmd = 'schtasks /run /tn SetDisplayMode'
    run(cmd, shell=True, stdout=PIPE, stderr=PIPE)


if __name__ == '__main__':
    flag_file = Path(r'C:\Windows\System32\Tasks\SetDisplayMode')
    if not flag_file.exists():
        create_task()

    start_task()
