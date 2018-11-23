import cflw小说下载 as 小说下载
c地址 = "http://www.555x.org/"
def f计算地址(a小说编号 = "", a章节编号 = ""):
	v地址 = c地址 + "read/"
	v地址 += a小说编号
	if a章节编号:
		v地址 += "_" + a章节编号
	return v地址 + ".html"
def f提取链接(a链接: str):
	#小说页http://www.555x.org/html/yanqing/txt45842.html
	#目录页http://www.555x.org/read/45842.html
	#正文页http://www.555x.org/read/45842_1.html
	v小说编号 = ""
	v章节编号 = ""
	#小说页
	v开始位置 = a链接.find("txt")
	if v开始位置 > 0:
		v开始位置 += len("txt")
		v结束位置 = a链接.find(".html")
		v小说编号 = a链接[v开始位置, v结束位置]
	#目录页,正文页
	v开始位置 = a链接.find("read/")
	if v开始位置 > 0:
		v开始位置 += len("read/")
		v中间位置 = a链接.find("_")
		v结束位置 = a链接.find(".html")
		if v中间位置 > 0:	#在正文页
			v小说编号 = a链接[v开始位置 : v中间位置]
			v章节编号 = a链接[v中间位置+1 : v结束位置]
		else:	#在目录页
			v小说编号 = a链接[v开始位置 : v结束位置]
	return (v小说编号, v章节编号)
def f获取小说(a: str):
	if "/" in a:
		v小说编号 = f提取链接(a)[0]
	else:
		v小说编号 = a
	return C小说(v小说编号)
class C小说(小说下载.I小说):
	c章节列表类名 = "read_list"
	def __init__(self, a小说编号: str):
		小说下载.I小说.__init__(self)
		self.m小说编号 = a小说编号
	def fg地址(self):
		return f计算地址(self.m小说编号)
	def fe目录(self):
		self.f载入()
		v目录元素 = self.m文档.find(name = "div", class_ = C小说.c章节列表类名)
		va章节列表 = v目录元素.find_all("a")
		for v in va章节列表:
			v链接 = v.get("href")
			v文本 = v.string
			vi返回 = True
			if vi返回:
				yield v文本, C章节(*f提取链接(v链接))
class C章节(小说下载.I章节):
	c正文标识名 = "view_content_txt"
	def __init__(self, a小说编号: str, a章节编号: str):
		小说下载.I章节.__init__(self)
		self.m小说编号 = a小说编号
		self.m章节编号 = a章节编号
	def fg地址(self):
		return f计算地址(self.m小说编号, self.m章节编号)
	def fg章节名(self):
		return ""
	def fg正文(self):
		self.f载入()
		v正文元素 = self.m文档.find(name = "div", id = C章节.c正文标识名)
		v正文文本 = ""
		for v行 in v正文元素.strings:
			vi添加 = True
			if "555x.org" in v行:
				vi添加 = False
			elif "小说（正文）正文" in v行:
				vi添加 = False
			elif "-用户上传之内容开始-" in v行:
				vi添加 = False
			elif "本文每页显示" in v行:
				break	#已经结束
			if vi添加:
				v正文文本 += v行 + "\n"
		return 小说下载.f处理正文(v正文文本)
