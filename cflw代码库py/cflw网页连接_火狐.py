from selenium import webdriver	#selenium
from selenium.webdriver.firefox.options import Options as FirefoxOptions	#selenium >= 4
class C火狐(webdriver.Firefox):
	c连接特性 = 0x0002
	def __init__(self):
		v选项 = FirefoxOptions()	#selenium4的写法
		#能力
		v选项.set_capability('acceptInsecureCerts', True)
		#档案
		v选项.accept_insecure_certs = True
		v选项.set_preference("browser.download.folderList", 1)	#下载路径：0桌面，1默认，2自定义
		v选项.set_preference("browser.download.manager.showWhenStarting", False)	#是否显示开始
		v选项.set_preference("browser.download.manager.useWindow", False)
		v选项.set_preference("browser.download.manager.alertonEXEopen", False)
		v选项.set_preference("browser.download.manager.showAlertonComplete", False)
		v选项.set_preference("browser.download.manager.closeWhenDone", False)
		v选项.set_preference('browser.helperApps.alwaysAsk.force', False)
		va文件类型 = [
			"binary/octet-stream",
			"application/octet-stream",
			"application/zip",
			"text/plain",
			"application/x-msdownload",
		]
		v选项.set_preference("browser.helperApps.neverAsk.saveToDisk", ",".join(va文件类型))	#不询问下载路径的文件类型
		v选项.set_preference("security.tls.version.min", 1)	#允许tls1.0
		#创建对象
		webdriver.Firefox.__init__(self, options = v选项)
	def f打开(self, a地址):
		self.get(a地址)
	def fs下载路径(self, a路径):
		self.firefox_profile.set_preference("browser.download.folderList", 2)	#设置成2则可以保存到指定目录
		self.firefox_profile.set_preference("browser.download.dir", a路径)	#下载到指定目录
