import urllib.parse
import selenium.webdriver	#selenium
def f创建地址(a地址, a用户名 = "", a密码 = ""):
	v地址 = urllib.parse.urlparse(a地址)
	if (a用户名 or a密码) and (not "@" in v地址.netloc):
		v主机名 = f"{a用户名}:{a密码}@{v地址.netloc}"
	else:
		v主机名 = v地址.netloc
	v地址 = urllib.parse.urljoin(v地址.geturl(), v主机名)
	return v地址
def f创建连接(a地址, at浏览器 = selenium.webdriver.Firefox):
	v网页 = at浏览器()
	v网页.get(a地址.geturl())
	return v网页