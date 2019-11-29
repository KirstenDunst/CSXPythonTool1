#执行热更新的操作

def autopackage_or_onlyhotfix():
	"""获取当前是iOS自动打包还是单纯的热更新"""
	hotfix_type = input('准备打热更新包还是ios自动打包？自动打包:True、单纯的热更新:False。或输入Q退出：[T/F/Q]')
	if hotfix_type.upper() == 'T':
		type_choose = True
	elif hotfix_type.upper() == 'F':
		type_choose = False
	elif hotfix_type.upper() == 'Q':
		exit()
	else :
		exit('输入不合法，请重新运行main.py重新开始')
	return type_choose

def alerm_upload_message(envior, descrption):
	"""上传的信息补充"""
	if envior == 'Dev':
		envior_package_add = "测试环境："
	elif envior == 'Beta':
		envior_package_add = "Beta环境："
	elif envior == 'Release':
		envior_package_add = "正式环境："
	return envior_package_add + descrption

def package_envoir(envior):
	"""打包适用环境"""
	if envior == 'Dev':
		envior_package = "Debug"
	elif envior == 'Beta':
		envior_package = "Release"
	elif envior == 'Release':
		envior_package = "Release"
	return envior_package

def get_packaging_type():
	"""获取当前的打包类型"""
	hotfix_type = input('准备打Android热更新包还是iOS热更新包？iOS:True、Android:False。或输入Q退出：[T/F/Q]')
	if hotfix_type.upper() == 'T':
		device_source = True
	elif hotfix_type.upper() == 'F':
		device_source = False
	elif hotfix_type.upper() == 'Q':
		exit()
	else :
		exit('输入不合法，请重新运行main.py重新开始')
	return device_source


def get_packaging_enviorment():
	"""获取当前打包的环境文件夹的名称"""
	page_envir = input('准备打包什么环境？Dev? Beta? Release?。或输入Q退出：[D/B/R/Q]')
	if page_envir.upper() == 'D':
		envir_dir_name = 'Dev'
	elif page_envir.upper() == 'B':
		envir_dir_name = 'Beta'
	elif page_envir.upper() == 'R':
		envir_dir_name = 'Release'
	elif page_envir.upper() == 'Q':
		exit()
	else :
		exit('输入不合法，请重新运行main.py重新开始')
	return envir_dir_name


def get_project_envior_file_name(envior, hf_settings):
	"""获取ios项目中对应环境所使用的文件名称"""
	if envior == 'Dev':
		file_name = hf_settings.iOS_test_filename
	elif envior == 'Beta':
		file_name = hf_settings.iOS_beta_filename
	elif envior == 'Release':
		file_name = hf_settings.iOS_release_filename
	return file_name


def get_packaging_script_name(device_source, envior, hf_settings):
	if envior == 'Dev':
		if device_source:
			script_name = hf_settings.iOS_test
		else:
			script_name = hf_settings.Android_test
	elif envior == 'Beta':
		if device_source:
			script_name = hf_settings.iOS_beta
		else:
			script_name = hf_settings.Android_beta
	elif envior == 'Release':
		if device_source:
			script_name = hf_settings.iOS_release
		else:
			script_name = hf_settings.Android_release
	return script_name


def get_packaging_version():
	"""获取当前打包的版本"""
	#记录打包版本号
	app_version = input('要打包版本号？eg:0.0.1。或输入Q退出：')
	if app_version.upper() == 'Q':
		exit()
	return app_version

