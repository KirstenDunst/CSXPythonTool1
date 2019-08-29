#导入文件
 
import os
import shutil
import md5_file as md5
import www_oss as oss_tool

from os.path import realpath
from settings import Settings


def hotfix_run():
	"""执行热更新差分包处理"""

	hf_settings = Settings()
	#记录打包对象时iOS还是安卓（True是iOS）
	device_source = False

	hotfix_type = input('准备打Android热更新包还是iOS热更新包？iOS:True、Android:False。或输入Q退出：[T/F/Q]')
	if hotfix_type.upper() == 'T':
		device_source = True
	elif hotfix_type.upper() == 'F':
		device_source = False
	elif hotfix_type.upper() == 'Q':
		exit()
	else :
		exit('输入不合法，请重新运行main.py重新开始')
	pakge_name_type = 'ios ' if(device_source) else 'Android '
	print('当前的打包对象：' + pakge_name_type + '\n')

	page_envir = input('准备打包什么环境？Dev? Beta? Release?。或输入Q退出：[D/B/R/Q]')
	if page_envir.upper() == 'D':
		envir_dir_name = 'Dev'
		if device_source:
			script_name = hf_settings.iOS_test
		else:
			script_name = hf_settings.Android_test
	elif page_envir.upper() == 'B':
		envir_dir_name = 'Beta'
		if device_source:
			script_name = hf_settings.iOS_beta
		else:
			script_name = hf_settings.Android_beta
	elif page_envir.upper() == 'R':
		envir_dir_name = 'Release'
		if device_source:
			script_name = hf_settings.iOS_release
		else:
			script_name = hf_settings.Android_release
	elif hotfix_type.upper() == 'Q':
		exit()
	else :
		exit('输入不合法，请重新运行main.py重新开始')
	print('当前打包www的环境：' + page_envir +'/n执行脚本script名称：' + script_name)

	#记录打包版本号
	app_version = input('要打包版本号？eg:0.0.1。或输入Q退出：')
	if app_version.upper() == 'Q':
		exit()
	print('当前打包的版本号：' + app_version)

	#取当前目录上一级目录（热更新的资源文件夹就和这一路径平级逐步往下）
	front_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
	print('父级目录：' + front_path)

	try:
		os.system('cd' + ' ' + hf_settings.h5_base_path + ' && npm run ' + script_name)
	except Exception as e:
		raise e
	finally:
		oss_tool.gen_tool(front_path, device_source)
		# """执行gen脚本"""
		# os.system('cd' + ' ' + hf_settings.gen_base_path + ' && source ~/.bash_profile && gradle run')
	
	if device_source:
		father_path = front_path + '/' + 'iOS'
	else:
		father_path = front_path + '/' + 'Android'
		
	if not os.path.exists(father_path):
			#多级文件创建，保证文件路径存在
		os.makedirs(father_path)

	child_path = father_path + '/' + envir_dir_name + '/' + app_version
	if not os.path.exists(child_path):
		#多级文件创建，保证文件路径存在
		os.makedirs(child_path)
	
	print('创建当前存储的子路径：' + child_path)
	#执行计算当前需要添加的文件目录(一次计算出来的，从低到高处理,每个版本设定最大1000个热更新包)
	current_number = 0
	while current_number <= 1000:
		last_path = child_path + '/' + str(current_number)
		if not os.path.exists(last_path):
			break
		else:
			current_number += 1

	print('资源存放路径：' + last_path)
	#多级文件创建，保证文件路径存在
	os.makedirs(last_path)

 	#处理生成资源文件之后的iOS文件夹以及资源配置文件的移动处理
	cell_file = front_path + '/Temp/' + 'resource'
	manifest_type_name = 'ios-update-manifest.json' if (device_source) else 'android_portal_manifest.json'
	cell_json = front_path + '/Temp/' + manifest_type_name
	#创建拆分包存在的文件夹
	os.makedirs(cell_file + '/' + 'patch')

	if os.path.exists(cell_file):
		if os.path.exists(cell_json):
 			#移动文件
 			shutil.move(cell_json,last_path)
 			#移动文件夹
 			shutil.move(cell_file,last_path)


	if current_number == 0:
		return

	#获取包含py的文件夹位置
	now_file_path = os.path.dirname(os.path.realpath(__file__))
	#可执行文件的拆分文件路径
	bsdiff_path = now_file_path + '/' + 'bsdiff' + '/' + 'bsdiff'
	if not os.path.exists(bsdiff_path):
		os.system('cd' + ' ' + now_file_path + '/' + 'bsdiff' + ' && make')

 	#循环差量包生成制作
	for number in range(0,current_number,1):
		print('差量包生成文件夹次数：' + str(number))
		zip_add_name = 'ios-www.zip' if (device_source) else 'www.zip'
		old_zip_path = child_path + '/' + str(number) + '/resource/assets/' + zip_add_name
		now_zip_path = last_path + '/resource/assets/' + zip_add_name
		now_patch_path = last_path + '/resource/patch/' + md5.get_filemd5(old_zip_path) + '.patch'
		os.system(bsdiff_path + ' ' + old_zip_path + ' ' + now_zip_path + ' ' + now_patch_path)


hotfix_run()














