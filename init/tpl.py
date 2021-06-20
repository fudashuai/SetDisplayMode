#!/usr/bin/env/python3
# -*- coding:utf-8 -*-

dirs_str = '''#!/usr/bin/env/python3
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
'''

gitignore_str = '''# Pycache
__pycache__

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# PEP 582; used by e.g. github.com/David-OConnor/pyflow
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/

# personal
.vscode
log/
output/'''

launch_str = '''#!/usr/bin/env/python3
# -*- coding:utf-8 -*-

import locale
import os
import platform
import time
from pathlib import Path
from subprocess import PIPE, run


def creat_py_venv():
    venv_dir = root_dir / '.venv'

    flags = True
    while True:
        os_platform = platform.system()
        if os_platform == 'Windows':
            base_python_path = 'python'
            venv_python_path = venv_dir / 'scripts' / 'python.exe'
            venv_pip_path = venv_dir / 'scripts' / 'pip.exe'

        if os_platform == 'Linux':
            base_python_path = 'python3'
            venv_python_path = venv_dir / 'bin' / 'python3'
            venv_pip_path = venv_dir / 'bin' / 'pip3'

        if not all([venv_python_path.exists(), venv_pip_path.exists()]):
            if flags:
                run(f'{base_python_path} -m venv .venv',
                    shell=True,
                    stdout=PIPE,
                    stderr=PIPE)
                flags = False
                print(f'create python venv')

            else:
                raise ValueError(f\'\'\'failed to create python venv

the command maybe as follows:

windows:
cd {root_dir}
python -m venv .venv

linux:
cd {root_dir}
python3 -m venv .venv
\'\'\')
        else:
            break

    return venv_python_path, venv_pip_path


def init(flags, *, module=None):
    system_encoding = locale.getpreferredencoding()
    venv_python_path, venv_pip_path = creat_py_venv()

    if flags == 0:
        cmd_list = (
            f'{venv_pip_path} install -i https://mirrors.aliyun.com/pypi/simple/ pip -U',
            f'{venv_pip_path} config set global.index-url https://mirrors.aliyun.com/pypi/simple/',
            f'{venv_pip_path} config set global.trusted-host mirrors.aliyun.com',
            f'{venv_pip_path} config set global.timeout 6000',
            f'{venv_pip_path} install chardet')
        for cmd in cmd_list:
            run(cmd, shell=True, stdout=PIPE, stderr=PIPE)

        from chardet import detect
        requirements_file = root_dir / 'requirements.txt'
        try:
            with open(requirements_file, 'rb') as file:
                content = file.read()
                file_encoding = detect(content)['encoding']
                requirements = content.decode(file_encoding, errors='ignore')
        except:
            requirements = None

        if requirements:
            p = run(f'{venv_pip_path} list',
                    shell=True,
                    stdout=PIPE,
                    stderr=PIPE)
            installed_packages = p.stdout.decode(system_encoding,
                                                 errors='ignore')

            for line in requirements.split('\\n'):
                try:
                    package, _ver = line.strip().split('==')
                except ValueError:
                    continue

                if package not in installed_packages:
                    run(f'{venv_pip_path} install {line}',
                        shell=True,
                        stdout=PIPE,
                        stderr=PIPE)

                    print(f'install package: {package}')
                    time.sleep(1)

    else:
        if not module:
            raise ValueError('module name cannot be none')

        p = run(f'{venv_pip_path} install {module}',
                shell=True,
                stdout=PIPE,
                stderr=PIPE)

        if p.stderr:
            raise NotImplementedError(
                p.stderr.decode(system_encoding, errors='ignore'))

        print(f'install package: {module}')

        run(f'{venv_pip_path} freeze >requirements.txt',
            shell=True,
            stdout=PIPE,
            stderr=PIPE)


if __name__ == '__main__':
    pwd = Path(__file__).resolve()
    root_dir = pwd.parent.parent
    os.chdir(root_dir)

    flags = 0
    while True:
        try:
            from main import main
            main()
            break
        except ModuleNotFoundError as e:
            module = str(e).split("'")[-2]
            init(flags, module=module)
        finally:
            flags += 1
'''

log_str = '''#!/usr/bin/env/python3
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
'''

main_str = '''#!/usr/bin/env/python3
# -*- coding:utf-8 -*-

# Author: $author
# CreateDate: $createdate
# Description: $description

from dirs import *
from log import log

# write your code here ...


def main():
    ...


if __name__ == '__main__':
    main()
'''

readme_str = '''## $appname

*$description*

### 用法

* 双击 **start.bat** 启动程序
* 程序运行结束，打开 **output** 目录查看运行结果

### 文件

* start.bat： 启动程序

### 目录

* .venv： Python虚拟环境
* conf： 配置信息
* core： 主程序
* init：程序初始化、打包
* log： 运行日志
* output： 运行结果
* source： 引用资源'''

start_str_cmd = r'''@echo off

cd %~dp0

if not exist .venv\scripts\python.exe (
    python -m venv .venv 1>nul 2>nul
    if not exist .venv\scripts\python.exe (
        init\python.exe /passive /quiet TargetDir=%LocalAppData%\Programs\Python\Python3X-32 1>nul 2>nul
        %LocalAppData%\Programs\Python\Python3X-32\python -m venv .venv 1>nul 2>nul)
)

.venv\scripts\python.exe core\launch.py'''

start_str_dash = r'''stty -echo

cd `dirname $0`

if [ ! -e ./.venv/bin/python3 ]; then
    python3 -m venv .venv
    if [ ! -e ./.venv/bin/python3 ]; then
        echo install python3 and run this script again
    fi
fi

./.venv/bin/python3 ./core/launch.py'''
