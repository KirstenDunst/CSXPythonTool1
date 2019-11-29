# 导入文件

import os
import shutil
import md5_file as md5
import www_oss as oss_tool
import access_infor as information_access

from os.path import realpath
from settings import Settings
from differ_file import Differ_name
from auto_package_ios import AutoArchive

def hotfix_run(hf_settings, autoPackageios, envir_dir_name_ios, app_version_ios, archive, description, project_name, package_envior):
        """执行热更新差分包处理,如果是自动打包传过来的就会直接读取，否则按照热更新的执行，一一询问"""

        # 记录打包对象时iOS还是安卓（True是iOS）
        device_source = True
        envir_dir_name = envir_dir_name_ios
        # 记录打包版本号
        app_version = app_version_ios

        if not autoPackageios :
            device_source = information_access.get_packaging_type()
            envir_dir_name = information_access.get_packaging_enviorment()
            app_version = information_access.get_packaging_version()

        # 初始化区别值对象
        differ_file_name = Differ_name(device_source)
        print('当前的打包对象：' + differ_file_name.get_source_type() + '\n')

        script_name = information_access.get_packaging_script_name(device_source, envir_dir_name, hf_settings)
        print('当前打包www的环境：' + envir_dir_name + '\n执行脚本script名称：' + script_name)

        print('当前打包的版本号：' + app_version)

        # 取当前目录上一级目录（热更新的资源文件夹就和这一路径平级逐步往下）
        front_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        print('父级目录：' + front_path)

        try:
            os.system('cd' + ' ' + hf_settings.h5_base_path + ' && npm run ' + script_name)
        except Exception as e:
            raise e
        finally:
            oss_tool.gen_tool(front_path, differ_file_name)
        # """执行gen脚本"""
        # os.system('cd' + ' ' + hf_settings.gen_base_path + ' && source ~/.bash_profile && gradle run')

        father_path = front_path + '/' + differ_file_name.get_source_type()
        child_path = father_path + '/' + envir_dir_name + '/' + app_version
        if not os.path.exists(child_path):
            # 多级文件创建，保证文件路径存在
            os.makedirs(child_path)
        print('创建当前存储的子路径：' + child_path)

        # 执行计算当前需要添加的文件目录(一次计算出来的，从低到高处理,每个版本设定最大1000个热更新包)
        current_number = 0
        while current_number <= 1000:
            last_path = child_path + '/' + str(current_number)
            if not os.path.exists(last_path):
                break
            else:
                current_number += 1

        print('资源存放路径：' + last_path)
        # 多级文件创建，保证文件路径存在
        os.makedirs(last_path)

        # 处理生成资源文件之后的iOS文件夹以及资源配置文件的移动处理
        cell_file = front_path + '/Temp/' + 'resource'
        cell_json = front_path + '/Temp/' + differ_file_name.get_json_mainfest()
        # 创建拆分包存在的文件夹
        patch_path = cell_file + '/' + 'patch'
        if not os.path.exists(patch_path):
            os.makedirs(patch_path)

        if os.path.exists(cell_file):
            if os.path.exists(cell_json):
                # 移动文件
                shutil.move(cell_json, last_path)
                # 移动文件夹
                shutil.move(cell_file, last_path)

        if current_number == 0:
            exit()

        # 获取包含py的文件夹位置
        now_file_path = os.path.dirname(os.path.realpath(__file__))
        # 可执行文件的拆分文件路径
        bsdiff_path = now_file_path + '/' + 'bsdiff' + '/' + 'bsdiff'
        if not os.path.exists(bsdiff_path):
            os.system('cd' + ' ' + now_file_path + '/' + 'bsdiff' + ' && make')

        # 循环差量包生成制作
        for number in range(0, current_number, 1):
            print('差量包生成文件夹次数：' + str(number))
            old_zip_path = child_path + '/' + str(number) + '/resource/assets/' + differ_file_name.get_zip_name()
            now_zip_path = last_path + '/resource/assets/' + differ_file_name.get_zip_name()
            now_patch_path = last_path + '/resource/patch/' + md5.get_filemd5(old_zip_path) + '.patch'
            # 差量包生成器
            os.system(bsdiff_path + ' ' + old_zip_path + ' ' + now_zip_path + ' ' + now_patch_path)

        if autoPackageios :
            # 处理好的压缩包移动替换项目操作
            archive.replace_zip_project(hf_settings, project_name, now_zip_path)

            # 打包上传
            archive.clean(hf_settings, project_name, description, child_path , current_number, package_envior)



if __name__ == '__main__':
    hf_settings = Settings()

    package_type = information_access.autopackage_or_onlyhotfix()
    if package_type :
        # 自动打包
        description = input("请输入打包版本更新内容:")
        archive = AutoArchive()
        archive.get_new_code_orignal(hf_settings)
        # 获取项目中的版本号(这里的版本号主要是针对热更新包的版本号，与项目无关)
        # app_version = archive.get_project_version(hf_settings)
        app_version = information_access.get_packaging_version()

        # 获取项目名
        project_name = archive.get_project_name(hf_settings)
        # 获取打包环境
        envir_dir_name = information_access.get_packaging_enviorment()

        description = information_access.alerm_upload_message(envir_dir_name, description)

        # 打包适用环境 (release, debug)
        package_envior = information_access.package_envoir(envir_dir_name)

        # 替换打包接口文件
        archive.change_iosproject_enviorment(hf_settings, project_name, information_access.get_project_envior_file_name(envir_dir_name, hf_settings))
        # 执行热更新操作生成压缩包
        hotfix_run(hf_settings, True, envir_dir_name, app_version, archive, description, project_name, package_envior)

    else:
        # 单纯执行热更新
        hotfix_run(hf_settings, False, '', '', '', '')

