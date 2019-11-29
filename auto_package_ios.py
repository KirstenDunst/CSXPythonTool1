#!/usr/bin/env python
# encoding: utf-8

# @Time    : 2019-11-06 15:28
# @Author  : 'caoshixin'
# @Site    :
# @File    : mainOne.py
# @Software: PyCharm


import os
import shutil
import requests
import webbrowser
import subprocess
import time
import smtplib
from email.mime.text import MIMEText
from email import encoders
from email.header import Header
from email.utils import parseaddr, formataddr

from git_branch_change import branch_change
from differ_file import Differ_name
import xml.etree.ElementTree as ET


ipa_download_url = 'https://www.pgyer.com/vbhE' #蒲公英的APP地址

# 蒲公英账号USER_KEY、API_KEY
USER_KEY = '664761a2fa18180424a37b63a6a3359d'
API_KEY = '5c3deeb5d3b60e1baecf69e919b48761'

from_address = 'XXXXXXXXXXXXXXXXXXXX@qq.com'    # 发送人的地址
password = 'XXXXXXXXXXXXXXXXXXXX'  # 邮箱密码换成他提供的16位授权码
to_address = 'XXXXXXXXXXXXXXXXXXXX@qq.com'    # 收件人地址,可以是多个的
smtp_server = 'smtp.qq.com'    # 因为我是使用QQ邮箱..


class AutoArchive(object):
    """自动打包并上传到蒲公英,发邮件通知"""

    def __init__(self):
        pass

    def clean(self, hf_settings, project_name, description, zip_base_path, now_page_number, package_envior):
        print("\n\n===========开始clean操作===========")
        start = time.time()
        clean_command = 'xcodebuild clean -workspace %s/%s.xcworkspace -scheme %s -configuration %s' % (
            hf_settings.project_base_path, project_name, project_name, package_envior)
        clean_command_run = subprocess.Popen(clean_command, shell=True)
        clean_command_run.wait()
        end = time.time()
        # Code码
        clean_result_code = clean_command_run.returncode
        if clean_result_code != 0:
            print("=======clean失败,用时:%.2f秒=======" % (end - start))
            return False
        else:
            print("=======clean成功,用时:%.2f秒=======" % (end - start))

            print("\n\n===========开始archive操作===========")

            # 删除之前的文件
            subprocess.call(['rm', '-rf', '%s/%s' % (hf_settings.project_base_path, hf_settings.export_directory)])
            time.sleep(1)
            # 创建文件夹存放打包文件
            subprocess.call(['mkdir', '-p', '%s/%s' % (hf_settings.project_base_path, hf_settings.export_directory)])
            time.sleep(1)

            start = time.time()
            archive_command = 'xcodebuild archive -workspace %s/%s.xcworkspace -scheme %s -configuration %s -archivePath %s/%s' % (
                hf_settings.project_base_path, project_name, project_name, package_envior, hf_settings.project_base_path,
                hf_settings.export_directory)
            archive_command_run = subprocess.Popen(archive_command, shell=True)
            archive_command_run.wait()
            end = time.time()
            # Code码
            archive_result_code = archive_command_run.returncode
            if archive_result_code != 0:
                print("=======archive失败,用时:%.2f秒=======" % (end - start))
                return False
            else:
                print("=======archive成功,用时:%.2f秒=======" % (end - start))
                # 导出IPA
                print("\n\n===========开始export操作===========")
                print("\n\n==========请你耐心等待一会~===========")
                start = time.time()
                export_command = 'xcodebuild -exportArchive -exportOptionsPlist %s/%s/info.plist -archivePath %s/%s.xcarchive -exportPath %s/%s' % (
                hf_settings.project_base_path, project_name, hf_settings.project_base_path, hf_settings.export_directory,
                hf_settings.project_base_path, hf_settings.export_directory)
                export_command_run = subprocess.Popen(export_command, shell=True)
                export_command_run.wait()
                end = time.time()
                # Code码
                export_result_code = export_command_run.returncode
                if export_result_code != 0:
                    print("=======导出IPA失败,用时:%.2f秒=======" % (end - start))
                    return False
                else:
                    print("=======导出IPA成功,用时:%.2f秒=======" % (end - start))
                    # 删除archive.xcarchive文件
                    subprocess.call(['rm', '-rf',
                                     '%s/%s.xcarchive' % (hf_settings.project_base_path, hf_settings.export_directory)])

                    print("\n\n===========开始上传蒲公英操作===========")
                    ipa_path = '%s/%s/%s.ipa' % (hf_settings.project_base_path, hf_settings.export_directory, project_name)
                    print("路径：" + ipa_path)
                    if ipa_path:
                        # https://www.pgyer.com/doc/api 具体参数大家可以进去里面查看,
                        url = 'https://upload.pgyer.com/apiv1/app/upload'
                        data = {
                            'uKey': USER_KEY,
                            '_api_key': API_KEY,
                            'installType': '1',
                            'updateDescription': description
                        }
                        files = {'file': open(ipa_path, 'rb')}
                        r = requests.post(url, data=data, files=files)
                        if r.status_code == 200:
                            # 打开浏览器
                            self.open_browser(self)
                            # 发送邮件
                            # self.send_email()

                        # 清除之前的压缩包文件，并将当前包文件置为基准文件，并清除生成的差量包
                        current_number = 0
                        while current_number < now_page_number:
                            last_path = zip_base_path + '/' + str(current_number)
                            if os.path.exists(last_path):
                                os.remove(last_path)
                        patch_now_path = zip_base_path + '/' + str(now_page_number) + '/resource/patch'
                        shutil.rmtree(patch_now_path)
                        os.makedirs(patch_now_path)
                        shutil.move(zip_base_path + '/' + str(now_page_number), zip_base_path + '/0')
                        print('当前h5压缩包置换为基准文件成功')

                    else:
                        print("\n\n===========没有找到对应的ipa===========")
                        return



    @staticmethod
    def open_browser(self):
        webbrowser.open(ipa_download_url, new=1, autoraise=True)

    @staticmethod
    def _format_address(self, s):
        name, address = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), address))

    def send_email(self):
        # https://www.pgyer.com/XXX app地址
        # 只是单纯的发了一个文本邮箱,具体的发附件和图片大家可以自己去补充
        msg = MIMEText('Hello' +  '╮(╯_╰)╭应用已更新,请下载测试╮(╯_╰)╭' + '蒲公英的更新会有延迟,具体版本时间以邮件时间为准' +'', 'html', 'utf-8')
        msg['From'] = self._format_address(self, 'iOS开发团队 <%s>' % from_address)
        msg['Subject'] = Header('来自iOS开发团队的问候……', 'utf-8').encode()
        server = smtplib.SMTP(smtp_server, 25)  # SMTP协议默认端口是25
        server.set_debuglevel(1)
        server.login(from_address, password)
        server.sendmail(from_address, [to_address], msg.as_string())
        server.quit()
        print("===========邮件发送成功===========")


    def get_new_code_orignal(self, hf_settings):
        """获取远端的最新分支代码"""
        branch_change(hf_settings.project_base_path, 'ios项目')
        branch_change(hf_settings.h5_base_path, 'h5项目')

    def get_project_version(self, hf_settings):
        """获取iOS项目的版本号，如果项目中找不到版本号要提示错误，修改之后重新运行"""
        info_plist_path = hf_settings.project_base_path + hf_settings.iOS_info_plist_path
        tree = ET.parse(info_plist_path)
        # 前三句导入数据并获取根元素
        root = tree.getroot()
        for movie in root:
            if movie.attrib['title'] == '':
                print()
        return "19.123"


    def get_project_name(self, hf_settings):
        """获取工程的项目名"""
        # 获取文件名
        file_names = os.listdir(hf_settings.project_base_path + '/')
        for filename in file_names :
            if '.xcodeproj' in filename :
                return filename.replace('.xcodeproj', '')
        print('请放置正确的iOS项目，并核对配置项中项目路径是否正确')
        exit()


    def change_iosproject_enviorment(self, hf_settings, project_name, project_envior_file_name):
        """替换项目中的环境文件，传入的是项目中要使用的环境相对路径+文件名"""
        now_project_path = hf_settings.project_base_path + '/' + project_name + hf_settings.iOS_now_filename
        change_project_path = hf_settings.project_base_path + '/' + project_name + project_envior_file_name
        path = shutil.copy(change_project_path, now_project_path)
        print("文件拷贝成功：" + path)


    def replace_zip_project(self, hf_settings, project_name, zip_path):
        """拷贝替换项目中的压缩包"""
        # 初始化区别值对象
        differ_file_name = Differ_name(True)
        path = shutil.copy( zip_path, hf_settings.project_base_path + '/' + project_name + '/' + differ_file_name.get_zip_name())
        print("文件拷贝成功：" + path)





# if __name__ == '__main__':
#     hf_settings = Settings()
#
#     archive = AutoArchive()
#     archive.get_new_code_orignal(hf_settings)
#     # 获取项目中的版本号
#     app_version = archive.get_project_version(hf_settings)
#     # 获取打包环境
#     envir_dir_name = information_access.get_packaging_enviorment()
#     # 执行热更新操作生成压缩包
#     zip_path = hotfix_run(hf_settings, True, envir_dir_name, app_version)
#     # 获取项目名
#     project_name = archive.get_project_name(hf_settings)
#     # 处理好的压缩包移动替换项目操作
#     archive.replace_zip_project(hf_settings, project_name, zip_path)
#
#     archive.clean(hf_settings, project_name)
#     archive.upload('%s/%s/%s.ipa' % (hf_settings.project_base_path, export_directory, project_name))
