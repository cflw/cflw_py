import re
import pathlib
import time
from bs4 import BeautifulSoup	#beautifulsoup4
import requests	#requests

def f创建解析器(a文本):
	return BeautifulSoup(a文本, "html.parser")
def f获取文档(a地址):
	v请求 = requests.get(url = a地址)
	v页面 = v请求.text
	time.sleep(1)
	return v页面
c开头缩进正则 = re.compile(r"^\s")
def f处理正文(a文本):
	v正文文本 = a文本
	v正文文本 = c开头缩进正则.sub("\n", v正文文本)	#清除缩进
	v正文文本 = v正文文本.replace("\xa0", "")	#清除缩进
	v正文文本 = v正文文本.replace("\u3000", "")	#清除缩进
	v正文文本 = v正文文本.replace("\r", "\n")	#
	v正文文本 = v正文文本.replace("\n \n", "\n")	#清除多余换行
	while "\n\n" in v正文文本:
		v正文文本 = v正文文本.replace("\n\n", "\n")	#清除多余换行
	return v正文文本
def f一键下载(a小说, a保存路径):
	v小说名 = a小说.fg小说名()
	#路径
	v路径 = pathlib.Path(a保存路径)
	v路径 /= v小说名 + ".txt"
	v文件名 = str(v路径)
	print("保存到: " + v文件名)
	v文件 = open(v文件名, "w", encoding = "utf-8")
	#循环
	for v章节名, v章节 in a小说.fe目录():
		v正文 = v章节.fg正文()
		v文件.write(v章节名 + "\n" + v正文 + "\n")
	print("下载完成")
class I文档:
	def __init__(self):
		self.m文档 = None
	def f重新载入(self):
		self.m文档 = f创建解析器(f获取文档(self.fg地址()))
	def f载入(self):
		if not self.m文档:
			self.f重新载入()
	def fg地址(self):
		raise NotImplementedError()
class I小说:
	def __init__(self):
		I文档.__init__(self)
	def fe目录(self):
		"返回(章节名, I章节 对象)"
		raise NotImplementedError()

class I章节:
	def __init__(self):
		I文档.__init__(self)
	def fg正文(self):
		"返回字符串"
		raise NotImplementedError()

c地址前缀 = "https://www.biqukan.com"
class C小说(I文档, I小说):
	c章节列表类名 = "listmain"
	def __init__(self, a地址):
		I文档.__init__(self)
		I小说.__init__(self)
		self.m地址 = a地址
	def fg地址(self):
		return self.m地址
	def fe目录(self):
		self.f载入()
		v目录元素 = self.m文档.find(name = "div", class_ = C小说.c章节列表类名)
		va章节列表 = v目录元素.find_all(name = "dd")
		#去除前面的最新章节和最后的重复章节
		va章节列表 = va章节列表[12:]
		for v in va章节列表:
			v链接 = v.a.get("href")	#章节链接
			v文本 = v.a.string	#章节名
			if "biqukan" in v文本:	#去除最后的重复章节
				continue
			yield v文本, C章节(c地址前缀 + v链接)
	def fg小说名(self):
		self.f载入()
		return self.m文档.find("h2").string

class C章节(I文档, I章节):
	c正文标识名 = "content"
	def __init__(self, a地址):
		I文档.__init__(self)
		I章节.__init__(self)
		self.m地址 = a地址
	def fg地址(self):
		return self.m地址
	def fg正文(self):
		self.f载入()
		v正文元素 = self.m文档.find("div", id = C章节.c正文标识名)
		v正文文本 = ""
		for v行 in v正文元素.strings:
			if "biqukan" in v行:	#去除广告
				continue
			v正文文本 += v行 + "\n"
		return f处理正文(v正文文本)

c地址 = "https://www.biqukan.com/38_38989/"
c章节地址 = "https://www.biqukan.com/1_1408/16046054.html"
def main():
	v小说 = C小说(c地址)
	# for v章节名, v章节 in v小说.fe目录():
	# 	print(v章节名, v章节.fg地址())
	# v章节 = C章节(c章节地址)
	# print(v章节.fg正文())
	f一键下载(v小说, "d:\小说")
if __name__ == "__main__":
	main()
