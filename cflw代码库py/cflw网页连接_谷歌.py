from selenium import webdriver	#selenium
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities	#selenium
class C谷歌(webdriver.Chrome):
	def __init__(self):
		v能力 = webdriver.DesiredCapabilities.CHROME.copy()
		v选项 = webdriver.ChromeOptions()
		v选项.add_argument('--allow-running-insecure-content')
		v选项.add_argument('--ignore-certificate-errors')
		v选项.add_argument('--allow-insecure-localhost')
		v选项.add_argument('--unsafely-treat-insecure-origin-as-secure')
		v选项.add_experimental_option({
			'profile.default_content_settings.popups': 0, 
			'download.default_directory': os.getcwd(),
		})
		webdriver.Chrome.__init__(self,capabilities = v能力, chrome_options = v选项)
	def f打开(self, a地址):
		self.get(a地址)
	def fs下载路径(self, a路径):
		raise NotImplementedError()