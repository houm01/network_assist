#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# github: https://github.com/houm01
# blog: https://houm01.com

import os
from split_file import split_tech_support
# import pprint

work_dir = os.listdir(os.chdir(os.getcwd() + '/' + 'raw_info'))  # 查看工作目录都有哪些文件

file_list = []
dir_list = []
for x in work_dir:   # 判断目录内是文件 or 目录
    if os.path.isfile(x):
        file_list.append(x)
    else:
        dir_list.append(x)


for x in file_list:
    print('文件:',x)     # 待优化打印效果
    split_tech_support(x)


for x in dir_list:    # 待优化打印效果
    print('目录',x)




