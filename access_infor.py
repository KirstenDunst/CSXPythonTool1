#执行热更新的操作

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
	elif hotfix_type.upper() == 'Q':
		exit()
	else :
		exit('输入不合法，请重新运行main.py重新开始')
	return envir_dir_name


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

