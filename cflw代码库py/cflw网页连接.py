import enum
import urllib.parse
from selenium import webdriver	#selenium
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities	#selenium
class E浏览器(enum.IntEnum):
	ie = enum.auto()
	edge = enum.auto()
	firefox = enum.auto()
	e火狐 = firefox
	chrome = enum.auto()
	e谷歌 = chrome
def f创建浏览器(a浏览器, a地址 = ""):
	#去掉ssl提示:https://stackoverflow.com/questions/24507078/how-to-deal-with-certificates-using-selenium
	if a浏览器 == E浏览器.firefox:
		v能力 = webdriver.DesiredCapabilities.FIREFOX.copy()
		v能力['acceptInsecureCerts'] = True
		v帐户 = webdriver.FirefoxProfile()
		v帐户.accept_untrusted_certs = True
		v浏览器 = webdriver.Firefox(capabilities = v能力, firefox_profile = v帐户)
		if a地址:
			v浏览器.get(a地址)
	elif a浏览器 == E浏览器.chrome:
		v能力 = webdriver.DesiredCapabilities.CHROME.copy()
		v选项 = webdriver.ChromeOptions()
		v选项.add_argument('--allow-running-insecure-content')
		v选项.add_argument('--ignore-certificate-errors')
		v选项.add_argument('--allow-insecure-localhost')
		v选项.add_argument('--unsafely-treat-insecure-origin-as-secure')
		v浏览器 = webdriver.Chrome(capabilities = v能力, chrome_options = v选项)
		if a地址:
			v浏览器.get(a地址)
	elif a浏览器 == E浏览器.ie:
		v能力 = webdriver.DesiredCapabilities.INTERNETEXPLORER.copy()
		v能力['acceptSslCerts'] = True
		v浏览器 = webdriver.Ie(capabilities = v能力)
		if a地址:
			v浏览器.get(a地址)
		if any((s in v浏览器.title) for s in ("证书错误", "Certificate error")):
			v浏览器.get("javascript:document.getElementById('invalidcert_continue').click()")
	elif a浏览器 == E浏览器.edge:
		v能力 = webdriver.DesiredCapabilities.EDGE.copy()
		v能力['javascriptEnabled'] = True
		v浏览器 = webdriver.Edge(capabilities = v能力)
		if a地址:
			v浏览器.get(a地址)
		if any((s in v浏览器.title) for s in ("证书错误", "Certificate error")):
			v浏览器.get("javascript:document.getElementById('invalidcert_continue').click()")
	else:
		raise ValueError("无法识别的参数")
	return v浏览器
def f创建地址(a地址, a用户名 = "", a密码 = ""):
	v地址 = urllib.parse.urlparse(a地址)
	if (a用户名 or a密码) and (not "@" in v地址.netloc):
		v主机名 = f"{a用户名}:{a密码}@{v地址.netloc}"
	else:
		v主机名 = v地址.netloc
	v地址 = urllib.parse.urljoin(v地址.geturl(), "//" + v主机名)
	return v地址
def f创建连接(a地址, a浏览器 = E浏览器.firefox):
	v地址 = f创建地址(a地址)
	v网页 = f创建浏览器(a浏览器, a地址)
	return v网页