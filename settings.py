#引入一些常用的操作


class Settings():
	"""热更新安卓和iOS差量包操作的一些常用设置"""
	def __init__(self):
		"""初始化"""
		super(Settings, self).__init__()

		# h5项目的本地路径
		self.h5_base_path = '/Users/caoshixin/Desktop/FubeiHotFix/life-circle-merchant-front'
		# 项目地址路径（目前仅支持ios项目路径）
		self.project_base_path = '/Users/caoshixin/公司/2018.4.23--杭州首展科技有限公司/项目开发/fubei-app-ios'

		# 总配置资源的一些常量定义
		# 渠道类型
		self.bundleType = 'H5'
		# 版本优化描述
		self.desc = '有升级！'
		# 是否强制升级
		self.forceUpdate = True
		# 升级版本
		self.version = '1.0.0'
		# 输出的文件夹
		self.export_directory = 'archive'

		# nodejs执行脚本名
		# iOS 测试包
		self.iOS_test = 'ios:hot_test'
		# iOS beta包
		self.iOS_beta = 'ios:hot_beta'
		# iOS 正式包
		self.iOS_release = 'ios:hot_release'
		# Android 测试包
		self.Android_test = 'md:hot_test'
		# Android beta包
		self.Android_beta = 'md:hot_beta'
		# Android 正式包
		self.Android_release = 'md:hot_release'


		# ios自动打包对应的不同环境文件名
		# iOS 打包使用的接口定义文件名
		self.iOS_now_filename = '/Classes/Others/FBHeaderDef/FBModuleAPI_Now.h'
		# iOS 测试接口文件名
		self.iOS_test_filename = '/Classes/Others/FBHeaderDef/FBModuleAPI_Dev.h'
		# iOS beta接口文件名
		self.iOS_beta_filename = '/Classes/Others/FBHeaderDef/FBModuleAPI_Beta.h'
		# iOS 正式接口文件名
		self.iOS_release_filename = '/Classes/Others/FBHeaderDef/FBModuleAPI_Release.h'
		# iOS info.plist文件名
		self.iOS_info_plist_path = '/JSbrige/Classes/systemFile/Info.plist'




