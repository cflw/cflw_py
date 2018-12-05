import cflw爬虫 as 爬虫
import cflw小说下载 as 小说下载
c地址 = "http://www.biqukan.cc"
c书 = "book"	#小说编号和域名之间夹了"book"
def f计算地址(a小说编号 = "", a章节编号 = "", a页 = 1):
	v地址 = c地址 + "/"
	if not a小说编号:
		return v地址
	v地址 += a小说编号 + "/"
	if not a章节编号:
		return v地址
	v地址 += a章节编号
	if a页 > 1:
		v地址 += "_" + str(a页)
	return v地址 + ".html"
def f提取链接(a链接: str):
	v链接 = a链接
	v小说编号 = ""
	v章节编号 = ""
	#删前缀
	if c地址 in v链接:
		v链接 = v链接[len(c地址):]
	v书位置 = v链接.find(c书)
	if v书位置 > 0:
		v链接 = v链接[v书位置 + len(c书):]
	#删后缀
	v链接 = 小说下载.f删除链接后缀(v链接)
	#计算索引
	v开始索引 = 0
	if v链接[0] == "/":
		v开始索引 = 1
	#分割
	v分割 = v链接.split("/")
	v小说编号 = v分割[v开始索引+0]
	if v开始索引+1 < len(v分割):
		v章节编号 = v分割[v开始索引+1]
	return (v小说编号, v章节编号)
def f获取小说(a: str):
	if "/" in a:
		v小说编号 = f提取链接(a)[0]
	else:
		v小说编号 = a
	return C小说(v小说编号)
class C小说(爬虫.I文档, 小说下载.I小说):
	c章节列表标识名 = "list-chapterAll"
	c信息标识名 = "info"
	def __init__(self, a小说编号: str):
		爬虫.I文档.__init__(self)
		小说下载.I小说.__init__(self)
		self.m小说编号 = a小说编号
		self.m信息 = {}
	def fg地址(self):
		return f计算地址(self.m小说编号)
	def fe目录(self):
		self.f载入()
		v目录元素 = self.m文档.find(name = "div", id = C小说.c章节列表标识名)
		va章节列表 = v目录元素.find_all(name = "dd")
		for v in va章节列表:
			v链接 = v.a.get("href")
			v文本 = v.a.string
			vi返回 = True
			if vi返回:
				yield v文本, C章节(*f提取链接(v链接))
	def fg小说信息(self):
		if not self.m信息:
			self.f载入()
			self.m信息["名称"] = self.m文档.find("h1").string
		return self.m信息
class C章节(小说下载.I章节):
	def __init__(self, a小说编号: str, a章节编号: str):
		小说下载.I章节.__init__(self)
		self.m小说编号 = a小说编号
		self.m章节编号 = a章节编号
		self.ma正文页 = []
	def fg正文页(self, a序号: int):
		v数量 = len(self.ma正文页)
		if v数量 > a序号:
			return self.ma正文页[a序号]
		for i in range(v数量, a序号+1):
			v正文页 = C正文页(f计算地址(self.m小说编号, self.m章节编号, i+1))
			self.ma正文页.append(v正文页)
		return self.ma正文页[a序号]
	def fg章节名(self):
		v页0 = self.fg正文页(0)
		v页0.f载入()
		return self.m文档.find("h1").string[:-5]
	def fg分页数(self):
		v页0 = self.fg正文页(0)
		v页0.f载入()
		v字符串 = self.m文档.find("h1").string
		return int(v字符串[-2])
	def fg正文(self):
		v正文文本 = ""
		for i in range(self.fg分页数()):
			v页 = self.fg正文页(i)
			v页.f载入()
			v正文文本 += v页.fg正文()
		return 小说下载.f处理正文(v正文文本)
class C正文页(爬虫.I文档):
	c正文标识名 = "htmlContent"
	def __init__(self, a地址: str):
		爬虫.I文档.__init__(self)
		self.m地址 = a地址
	def fg地址(self):
		return self.m地址
	def fg正文(self):
		self.f载入()
		v正文元素 = self.m文档.find("div", id = C正文页.c正文标识名)
		v正文文本 = ""
		for v行 in v正文元素.strings:
			if "biqukan" in v行:
				continue
			if "本章未完，点击下一页继续阅读" in v行:
				continue
			v下一页箭头位置 = v行.find(" -->>")
			if v下一页箭头位置 > 0:
				v行1 = v行[:v下一页箭头位置]
			else:
				v行1 = v行
			v正文文本 += v行1 + "\n"
		return v正文文本
