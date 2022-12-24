import enum
import urllib.parse
from . import cflw网页连接_微软 as 微软
from . import cflw网页连接_火狐 as 火狐
from . import cflw网页连接_谷歌 as 谷歌
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
		v浏览器 = 火狐.C火狐()
	elif a浏览器 == E浏览器.chrome:
		v浏览器 = 谷歌.C谷歌()
	elif a浏览器 == E浏览器.ie:
		v浏览器 = 微软.Cie()
	elif a浏览器 == E浏览器.edge:
		v浏览器 = 微软.Cedge()
	else:
		raise ValueError("无法识别的参数")
	if a地址:
		v浏览器.f打开(a地址)
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
	# v地址 = f创建地址(a地址)
	v网页 = f创建浏览器(a浏览器, a地址)
	return v网页