import os
from selenium import webdriver	#selenium >= 4
c驱动程序 = "chromedriver"
class C谷歌(webdriver.Chrome):
	c连接特性 = 0x0002
	def __init__(self, a驱动路径 = None):
		#选项
		v选项 = webdriver.ChromeOptions()
		v选项.add_argument('--allow-running-insecure-content')
		v选项.add_argument('--ignore-certificate-errors')
		v选项.add_argument('--allow-insecure-localhost')
		v选项.add_argument('--unsafely-treat-insecure-origin-as-secure')
		# v选项.add_experimental_option('profile.default_content_settings.popups', 0)	#InvalidArgumentException
		# v选项.add_experimental_option('download.default_directory', os.getcwd())	#InvalidArgumentException
		#服务
		v服务 = webdriver.ChromeService(executable_path = a驱动路径)
		#创建对象
		webdriver.Chrome.__init__(self, options = v选项, service = v服务)
	def f打开(self, a地址):
		self.get(a地址)
	def fs下载路径(self, a路径):
		raise NotImplementedError()