#!/usr/bin/env python
# encoding: utf-8

# @Time    : 2019-11-28 10:16
# @Author  : 'caoshixin'
# @Site    :
# @File    : gitBranchChange.py
# @Software: PyCharm

import os
import subprocess

def branch_change(project_path, project_alarm):
    """执行分支切换"""
    temp_branch_dict = get_brancheDits(project_path)
    temp_branch_list = get_brancheLists(project_path)

    branch_str = ""
    for key, value in temp_branch_dict.items():
        branch_str += (key + " : " + value + "\n")

    branch_select_key = input('请选择你想要打包使用的' + project_alarm + '远端代码分支\n' + branch_str + ':')
    branch_name_origin = temp_branch_dict[branch_select_key]
    branch_name_local = branch_name_origin.replace('origin/','')
    print('选中的分支名：' + branch_name_origin)
    try:
        # 转到工程路径下
        os.chdir(project_path)
    except Exception as e:
        print("工程路径出错：" + e)
    print(temp_branch_list)

    if branch_name_local not in temp_branch_list:
        # 同步远端最新的分支，更新本地远端的分支显示数据，拉取分支到本地
        os.system(
            ' git fetch origin && git remote update origin --prune && ' + 'git checkout -b ' + branch_name_local + ' ' + branch_name_origin)
    else:
        os.system(' git checkout ' + branch_name_local + ' && git pull')

    # 在拉取代码耗时过程中不会执行下面的代码，代码拉取成功之后才会向下继续执行





def get_brancheDits(project_dir):
    try:
        # 转到工程路径下
        os.chdir(project_dir)
    except Exception as e:
        print("工程路径出错：" + e)
    branches_str = subprocess.check_output(["git", "branch", "-r"]).decode()
    # 终端运行“git branch”命令，并且将终端的输出str转存到branches_str里
    branches = branches_str.split('\n')
    # 使用str的split方法将其按照'\n'分割
    branch_dict = {}
    step = 0
    for branch in branches[0:-1]:
        branch_dict[str(step)] = branch.lstrip('* ');
        step += 1
        # 使用str的lstrip方法将字符串的前的空格和当前branch前的“*”标记去除
    return branch_dict

def get_brancheLists(project_dir):
    try:
        # 转到工程路径下
        os.chdir(project_dir)
    except Exception as e:
        print("工程路径出错：" + e)
    branches_str = subprocess.check_output(["git", "branch", "-l"]).decode()
    # 终端运行“git branch”命令，并且将终端的输出str转存到branches_str里
    branches = branches_str.split('\n')
    # 使用str的split方法将其按照'\n'分割
    branch_local_list = []
    for branch in branches[0:-1]:
        branch_local_list.append(branch.lstrip('* '));
        # 使用str的lstrip方法将字符串的前的空格和当前branch前的“*”标记去除
    return branch_local_list

