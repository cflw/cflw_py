import re
from bs4 import BeautifulSoup	#beautifulsoup4
import requests	#requests
c超文本传输协议错误正则表达式 = re.compile(r"\d\d\d")
def fc解析器bs(a文本):
	return BeautifulSoup(a文本, "html.parser")
def f获取文档(a地址, a请求头 = None, a失败重试次数 = 5):
	e = RuntimeError("失败重试次数过多")
	for i in range(a失败重试次数):
		try:
			v请求 = requests.get(url = a地址, headers = a请求头)
			v请求.encoding = v请求.apparent_encoding
			v页面 = v请求.text
			if f检测超文本传输协议错误(v页面):
				raise RuntimeError()
			return v页面
		except Exception as e:
			continue	#重试
	raise e
def f检测超文本传输协议错误(a文档)->int:
	if len(a文档) > 1000:	#大文档应该没问题
		return 0
	v匹配结果 = c超文本传输协议错误正则表达式.search(a文档)
	if v匹配结果:
		return int(v匹配结果.group(0))
	return 0	#没错误返回0
class I文档:
	def __init__(self):
		self.m文档 = None
	def f重新载入(self):
		self.m文档 = fc解析器bs(f获取文档(self.fg地址()))
	def f载入(self):
		if not self.m文档:
			self.f重新载入()
	def fg地址(self):
		raise NotImplementedError()