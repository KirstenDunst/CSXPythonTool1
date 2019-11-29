#处理差异文件

class Differ_name():
	"""处理差异化文件的统一处理"""
	def __init__(self, device_source):
		"""存储差异化的对象，统一处理需要差异化的名称"""
		super(Differ_name, self).__init__()
		self.device_source = device_source




	def get_source_type(self):
		# 获取当前的打包对象类型
		return 'iOS' if(self.device_source) else 'Android'

	def get_json_mainfest(self):
		# 获取总配置的json名称
		return 'ios-update-manifest.json' if (self.device_source) else 'android_portal_manifest.json'

	def get_zip_name(self):
		# 获取压缩包名称
		return 'ios-www.zip' if (self.device_source) else 'www.zip'

	def get_add_h5path(self):
		# 获取h5项目打包出来的www包路径基于跟路径的差异化补充
		return '' if (self.device_source) else '/platforms/android/assets'



		



