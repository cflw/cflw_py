import time
import cflw小说下载 as 小说下载
c地址 = "http://www.biqutxt.com"
def f计算地址(a小说编号 = "", a章节编号 = ""):
	v地址 = c地址 + "/"
	if not a小说编号:
		return v地址
	v地址 += a小说编号 + "/"
	if not a章节编号:
		return v地址
	v地址 += a章节编号
	return v地址 + ".html"
def f提取链接(a链接: str):
	v链接 = a链接
	v小说编号 = ""
	v章节编号 = ""
	#删域名
	if c地址 in v链接:
		v链接 = v链接[len(c地址):]
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
class C小说(小说下载.I小说):
	c章节列表标识名 = "list"
	c信息标识名 = "info"
	def __init__(self, a小说编号: str):
		小说下载.I小说.__init__(self)
		self.m小说编号 = a小说编号
		self.m信息 = {}
	def fg地址(self):
		return f计算地址(self.m小说编号)
	def fe目录(self):
		self.f载入()
		v目录元素 = self.m文档.find(name = "div", id = C小说.c章节列表标识名)
		va章节列表 = v目录元素.find_all(name = "dd")
		#去除前面的最新章节
		va章节列表 = va章节列表[9:]
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
			# va信息 = self.m文档.find(name = "div", id = C小说.c信息标识名).contents
			# self.m信息["作者"] = va信息[0].string[3:]
			# self.m信息["分类"] = va信息[1].string[3:]
			# self.m信息["状态"] = va信息[2].string[3:]
			# self.m信息["字数"] = int(va信息[3].string[3:])
			# self.m信息["最后更新时间"] = time.strptime(va信息[4].string[5:], "%Y-%m-%d %H:%M:%S")
		return self.m信息
class C章节(小说下载.I章节):
	c正文标识名 = "content"
	def __init__(self, a小说编号: str, a章节编号: str):
		小说下载.I章节.__init__(self)
		self.m小说编号 = a小说编号
		self.m章节编号 = a章节编号
	def fg地址(self):
		return f计算地址(self.m小说编号, self.m章节编号)
	def fg章节名(self):
		self.f载入()
		return self.m文档.find("h1").string
	def fg正文(self):
		self.f载入()
		v正文元素 = self.m文档.find("div", id = C章节.c正文标识名)
		v正文文本 = ""
		for v行 in v正文元素.strings:
			vi添加 = True
			if vi添加:
				v正文文本 += v行 + "\n"
		return 小说下载.f处理正文(v正文文本)