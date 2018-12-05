import cflw爬虫 as 爬虫
import cflw小说下载 as 小说下载
c地址 = "http://www.qiushu.cc"
c小说地址 = c地址 + "/txt"
c目录地址 = c地址 + "/t/"
def f计算地址(a小说编号 = "", a章节编号 = ""):
	v地址 = c目录地址
	if not a小说编号:
		return v地址
	v地址 += a小说编号 + "/"
	if not a章节编号:
		return v地址
	v地址 += a章节编号
	return v地址 + ".html"
def f提取链接(a链接):
	v链接 = a链接
	v小说编号 = ""
	v章节编号 = ""
	#删域名
	if c小说地址 in v链接:
		v链接 = v链接[len(c小说地址):]
	if c目录地址 in v链接:
		v链接 = v链接[len(c目录地址):]
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
	c目录类名 = "book_con_list"
	def __init__(self, a小说编号):
		爬虫.I文档.__init__(self)
		小说下载.I小说.__init__(self)
		self.m小说编号 = a小说编号
		self.m信息 = {}
	def fg地址(self):
		return f计算地址(self.m小说编号)
	def fe目录(self):
		self.f载入()
		v目录元素 = self.m文档.find_all(name = "div", class_ = C小说.c目录类名)[1]
		va章节列表 = v目录元素.find_all(name = "li")
		for v in va章节列表:
			v链接 = v.a.get("href")
			v文本 = v.a.string
			yield v文本, C章节(self.m小说编号, f提取链接(v链接)[0])
	def fg小说名(self):
		self.f载入()
		return self.m文档.find(name = "div", class_ = "title").find("h1").string
class C章节(爬虫.I文档, 小说下载.I章节):
	c正文标识名 = "content"
	c正文类名 = "book_content"
	def __init__(self, a小说编号, a章节编号):
		爬虫.I文档.__init__(self)
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
		v正文元素 = self.m文档.find("div", id = C章节.c正文标识名, class_ = C章节.c正文类名)
		v正文文本 = ""
		for v in v正文元素.strings:
			if "read_di();" in v:
				break
			v正文文本 += v + "\n"
		return 小说下载.f处理正文(v正文文本)