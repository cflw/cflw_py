from selenium import webdriver	#selenium
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities	#selenium
def f跳过证书(a浏览器):
	if any((s in a浏览器.title) for s in ("证书错误", "Certificate error")):
		a浏览器.get("javascript:document.getElementById('invalidcert_continue').click()")
class Cie(webdriver.Ie):
	c连接特性 = 0x0002
	def __init__(self):
		v能力 = webdriver.DesiredCapabilities.INTERNETEXPLORER.copy()
		v能力['acceptSslCerts'] = True
		webdriver.Ie.__init__(self, capabilities = v能力)
	def f打开(self, a地址):
		self.get(a地址)
		f跳过证书(self)
	def fs下载路径(self, a路径):
		raise NotImplementedError()
class Cedge(webdriver.Edge):
	c连接特性 = 0x0002
	def __init__(self):
		v能力 = webdriver.DesiredCapabilities.EDGE.copy()
		v能力['javascriptEnabled'] = True
		webdriver.Edge.__init__(self, capabilities = v能力)
	def f打开(self, a地址):
		self.get(a地址)
		f跳过证书(self)
	def fs下载路径(self, a路径):
		raise NotImplementedError()