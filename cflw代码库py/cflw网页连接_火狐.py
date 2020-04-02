from selenium import webdriver	#selenium
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities	#selenium
class C火狐(webdriver.Firefox):
	def __init__(self):
		v能力 = webdriver.DesiredCapabilities.FIREFOX.copy()
		v能力['acceptInsecureCerts'] = True
		v帐户 = webdriver.FirefoxProfile()
		v帐户.accept_untrusted_certs = True
		v帐户.set_preference("browser.download.folderList", 2)
		v帐户.set_preference("browser.helperApps.neverAsk.saveToDisk", "binary/octet-stream")
		webdriver.Firefox.__init__(self, capabilities = v能力, firefox_profile = v帐户)
	def f打开(self, a地址):
		self.get(a地址)
	def fs下载路径(self, a路径):
		self.firefox_profile.set_preference("browser.download.dir", a路径)
