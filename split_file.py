#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# github: https://github.com/houm01
# blog: https://houm01.com

import os
import re
import shutil


def split_tech_support(file_name):
    line_list = []   # line_list 存放 show tech-support的行号
    line_num = 0
    show_line_dict = {}
    show_line_dict_key = []

    with open(file_name, 'r') as f:
        for line in f.readlines():
            line_num = line_num + 1
            if 'show tech-support' in line.strip():
                line_list.append(line_num)   # 找到show tech-support的所在行
            elif '#show' in line.strip() and 'tech' not in line.strip():   # 判断非 show tech-support 的命令
                test = re.search('(.*)#show',line.strip()).groups()[0]  # 得到 hostname
                if test not in show_line_dict.values():
                    show_line_dict[line_num] = test

        # 开始写入 show tech-support 文本
        a = - 1

        while a < len(line_list) - 1:
            xx = line_list[a] - 1
            try:
                yy = line_list[a + 1] - 2
            except IndexError:
                pass

            f = open(file_name, 'r')

            try:
                with open((str(a) + '_sw_tech_support.txt'), 'w') as file:
                    file.write(''.join(f.readlines()[xx:yy]))
                a = a + 1
            finally:
                # pass
                f1 = open(file_name, 'r')
                with open('last_sw_tech_support.txt', 'w') as file2:
                    file2.write(''.join(f1.readlines()[line_list[-1] - 1:]))
                f1.close()
            f.close()
        # 结束写入 show tech-support 文本

        # 开始写入 show 命令的文本
        for key in show_line_dict.keys():
            show_line_dict_key.append(key)

        b = 0
        while b < len(show_line_dict_key) - 1:
            xx2 = show_line_dict_key[b] - 1
            try:
                yy2 = show_line_dict_key[b + 1] - 2
            except IndexError:
                pass
            f = open(file_name, 'r')

            try:
                with open((str(b) + '_sw_cisco_show.txt'), 'w') as file:
                    file.write(''.join(f.readlines()[xx2:yy2]))
                b = b + 1
            finally:
                # pass
                f2 = open(file_name, 'r')
                with open('last_cisco_show.txt', 'w') as file:
                    file.write(''.join(f2.readlines()[show_line_dict_key[-1] - 1:]))
                f2.close()

            f.close()
        # 结束写入 show 命令的文本


def rename_file():
    file_raw = os.listdir()
    for x in file_raw:
        if '_sw_' in x:
            try:
                shutil.move(x, raw_dir + '/' + 'output_dir' + '/' + 'raw_file')
            except shutil.Error:
                print('目标文件已存在',x)
        elif 'cisco_show' in x:
            try:
                shutil.move(x, raw_dir + '/' + 'output_dir' + '/' + 'raw_file')
            except shutil.Error:
                print('目标文件已存在', x)
            # pass
            # os.chdir(raw_dir + '/' + 'output_dir' + '/' + 'raw_file')
    os.chdir(raw_dir + '/' + 'output_dir' + '/' + 'raw_file')
    file_raw1 = os.listdir()
    # print(file_raw1)

    for x in file_raw1:
        if '-1_sw' in x:
            print('待删除:',x)
            os.remove(x)

        elif 'tech_support' in x:
            with open(x,'r') as file_name_sw_raw:
                try:
                    # globals(new_name)
                    new_name = re.search('hostname (.*)',file_name_sw_raw.read()).groups()[0]
                    # print(new_name)
                    os.chdir(raw_dir + '/' + 'output_dir' + '/' + 'raw_file')
                    os.rename(x, new_name)
                except AttributeError:
                    pass
                except FileNotFoundError:
                    pass
        elif 'cisco_show' in x:
            with open(x,'r') as file_name_sw_raw:
                try:
                    new_name = re.search('(.*)#show',file_name_sw_raw.read()).groups()[0]
                    os.chdir(raw_dir + '/' + 'output_dir' + '/' + 'raw_file')
                    os.rename(x, new_name)
                except ArithmeticError:
                    pass
                except FileExistsError:
                    pass


if __name__ == '__main__':
    print('====处理信息开始=====')
    print('')

    # 创建分析后的输出的存放文件夹
    # -----start-----
    try:
        os.mkdir('output_dir' + '/' + 'raw_file')
    except FileExistsError:
        print('output_dir/raw_file 已存在,跳过创建动作')
        print('')
    # ------end-----

    raw_dir = os.getcwd()  # 获取原始原件夹
    print('原始文件夹 ->',raw_dir)
    print('')

    try:
        os.chdir(raw_dir + '/' + 'raw_info')
        to_be_analyzed_file = os.listdir()

        for x in to_be_analyzed_file:
            if '_' in x:
                to_be_analyzed_file.remove(x)

        for i in to_be_analyzed_file:
            print('待处理文件:',i)
            split_tech_support(i)
    except UnicodeDecodeError:
        split_tech_support(i)
        # print('UnicodeDecodeError')
        print('')
        # pass

    # split_tech_support('10.53.70.2')   # file_name是待分析的源文件名称

    rename_file()

    print('')
    print('====处理信息完成=====')