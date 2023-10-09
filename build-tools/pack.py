from datetime import datetime
from subprocess import run
import sys
sys.path.append('.')
from version import VERSION_STRING

run([
    'flet',
    'pack',
    'main.py',
    '--name',
    'lovemilkMCCMLFT',
    '--icon',
    'resources/icon.ico',
    '--add-data',
    'resources:resources',
    '--product-name',
    'lovemilkMCCMLFT',
    '--product-version',
    VERSION_STRING,
    '--file-version',
    VERSION_STRING,
    '--file-description',
    '一个基于修改 Hosts 让中国大陆用户登录 Minecraft 国际版(Java / 基岩) 不再困难的软件',
    '--copyright',
    'LoveMilk©2023 / BSD 3 LICENSE',
    ])

# https://blog.csdn.net/caoyang_he/article/details/108372398
run(f'build-tools/7zr a release/release.{VERSION_STRING}-{datetime.now().strftime("%Y%m%d%H%M%S")}.zip ./dist/* ./resources')
