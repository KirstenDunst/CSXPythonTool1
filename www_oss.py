#由www包文件生成oss上传资源使用
import os
import shutil
import time
import json
import socket
import md5_file as md5
import zip_file as dir_zip 
from os.path import realpath

from settings import Settings


def gen_tool(file_path, device_source):
	"""执行www包文件的md5资源文件以及压缩包处理"""
	hf_settings = Settings()

	try:
		page_json(file_path, hf_settings, device_source)
	except Exception as e:
		raise e
	finally:
		oss_resource(file_path, hf_settings, device_source)


def page_json(file_path, hf_settings, device_source):
	"""总配"""
	object_json = {}
	object_json['type'] = hf_settings.bundleType
	object_json['entry'] = 'index.html'
	object_json['checksum'] = resource_json(hf_settings, device_source)
	version_str = hf_settings.version + '.' + time.strftime("%Y%m%d%H%M%S", time.localtime())
	object_json['version'] = version_str

	android_add_file_path = hf_settings.h5_base_path if(device_source) else hf_settings.h5_base_path + '/platforms/android/assets'
	file_name = android_add_file_path + '/www/' + 'resource-bundle.manifest'
	with open (file_name, 'w', encoding='utf-8') as f_obj:
		json.dump(object_json, f_obj, ensure_ascii=False, indent=4)
		print('保存资源文件成功')

	portal_resource_json(file_path, hf_settings, version_str)


def resource_json(hf_settings, device_source):
	"""内部资源清单"""
	checksum_json = {}
	android_add_file_path = hf_settings.h5_base_path if(device_source) else hf_settings.h5_base_path + '/platforms/android/assets'
	file_dir = android_add_file_path + '/www'
	for parent, dirnames, filenames in os.walk(file_dir,  followlinks=True):
		for filename in filenames:
			#遍历所有的文件名filename
			#文件的绝对路径
			file_path = os.path.join(parent, filename)
			#文件的相对路径
			relative_path = str(file_path).replace(file_dir + '/','')
			#排除mac的文件夹生成的配置信息
			if filename == '.DS_Store':
				os.remove(file_path)
			elif filename in ['resource-bundle.manifest', 'last-commit', 'www.zip']:
				print('不计入资源完备文件的md5值')
			else:
				checksum_json[relative_path] = md5.get_file_md5(file_path)

	return checksum_json



def oss_resource(file_path, hf_settings, device_source):
	temp_path = file_path + '/Temp'
	if not os.path.exists(temp_path):
		#多级文件创建，保证文件路径存在
		os.makedirs(temp_path)

	zip_resource(temp_path, hf_settings, device_source)
	oss_json(temp_path, hf_settings, device_source)
	

def oss_json(file_path, hf_settings, device_source):
	"""生成资源文件"""
	manifest_json = {}
	zip_name_add = 'ios-www.zip' if (device_source) else 'www.zip'
	zip_file_path = file_path + '/resource/assets/' + zip_name_add
	manifest_json['bundleArchiveChecksum'] = md5.get_file_md5(zip_file_path)
	android_add_file_path = hf_settings.h5_base_path if(device_source) else hf_settings.h5_base_path + '/platforms/android/assets'
	bundle_file_path = android_add_file_path + '/www/resource-bundle.manifest'
	manifest_json['bundleManifestChecksum'] = md5.get_file_md5(bundle_file_path)
	manifest_json['bundlePlatform'] = 'iOS' if (device_source) else 'Android'
	manifest_json['bundleType'] = hf_settings.bundleType
	manifest_json['desc'] = hf_settings.desc
	manifest_json['forceUpdate'] = hf_settings.forceUpdate
	manifest_json['version'] = hf_settings.version
	manifest_json['entireBundleUrl'] = 'http://' + str(get_host_ip()) + '/resource/assets/www.zip'
	manifest_json['patchRootUrl'] = 'http://' + str(get_host_ip()) + '/resource/patch/'

	file_name_add = '/ios-update-manifest.json' if (device_source) else '/android_portal_manifest.json'
	file_name = file_path + file_name_add
	with open (file_name, 'w', encoding='utf-8') as f_obj:
		json.dump(manifest_json, f_obj, ensure_ascii=False, indent=4)
		print('保存资源文件成功')


def zip_resource(file_path, hf_settings, device_source):
	zip_file_path = file_path + '/resource/assets'
	if not os.path.exists(zip_file_path):
		#多级文件创建，保证文件路径存在
		os.makedirs(zip_file_path)
	android_add_file_path = hf_settings.h5_base_path if(device_source) else hf_settings.h5_base_path + '/platforms/android/assets'
	zip_name_add = '/ios-www.zip' if (device_source) else '/www.zip'
	dir_zip.zip_temp_dir(android_add_file_path + '/www', zip_file_path + zip_name_add)


def portal_resource_json(file_path, hf_settings, version_str):
	portal_file_path = file_path + '/Temp/resource/assets'
	if not os.path.exists(portal_file_path):
		#多级文件创建，保证文件路径存在
		os.makedirs(portal_file_path)

	portal_json = {}
	portal_json['checksum'] = {}
	portal_json['entry'] = 'index.html'
	portal_json['type'] = hf_settings.bundleType
	portal_json['version'] = version_str
	file_name = file_path + '/Temp/resource/assets/portal.manifest'
	with open (file_name, 'w', encoding='utf-8') as f_obj:
		json.dump(portal_json, f_obj, ensure_ascii=False, indent=4)
		print('保存配置资源文件成功')


def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip	





