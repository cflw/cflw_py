import cflw小说下载 as 小说下载
c地址 = "https://www.23us.so"
c小说地址 = c地址 + "/xiaoshuo/"
c文件地址 = c地址 + "/files/article/html/"
def f计算地址(a小说编号: str, a章节编号: str = None):
	v地址 = c文件地址
	if not a小说编号:
		raise ValueError("a小说编号 不能为空")
	v地址 += "%s/%s" %(a小说编号[:-3], a小说编号)
	if not a章节编号:
		return v地址 + "/index.html"
	v地址 += "/" + a章节编号
	return v地址 + ".html"
def f提取链接(a链接: str):
	v链接 = a链接
	v链接 = 小说下载.f删除链接后缀(v链接)
	if c小说地址 in v链接:
		v链接 = v链接[len(c小说地址):]
	if c文件地址 in v链接:
		v链接 = v链接[len(c文件地址):]
		v位置 = v链接.find("/")
		v链接 = v链接[v位置+1:]
	v分割 = v链接.split("/")
	return v分割
def f获取小说(a: str):
	if "/" in a:
		v小说编号 = f提取链接(a)[0]
	else:
		v小说编号 = a
	return C小说(v小说编号)
class C小说(小说下载.I小说):
	c章节列表类名 = "L"
	def __init__(self, a小说编号: str):
		小说下载.I小说.__init__(self)
		self.m小说编号 = a小说编号
	def fg地址(self):
		return f计算地址(self.m小说编号)
	def fe目录(self):
		self.f载入()
		va章节 = self.m文档.find_all("td", class_ = C小说.c章节列表类名)
		for v章节 in va章节:
			v元素 = v章节.find("a")
			v链接 = v元素.get("href")
			v文本 = v元素.string
			yield v文本, C章节(*f提取链接(v链接))
class C章节(小说下载.I章节):
	c正文标识名 = "contents"
	def __init__(self, a小说编号: str, a章节编号: str):
		小说下载.I章节.__init__(self)
		self.m小说编号 = a小说编号
		self.m章节编号 = a章节编号
	def fg地址(self):
		return f计算地址(self.m小说编号, self.m章节编号)
	def fg正文(self):
		self.f载入()
		v元素 = self.m文档.find("dd", id = C章节.c正文标识名)
		v正文 = ""
		for v in v元素.strings:
			if "阅读网址" in v:
				break
			v正文 += v
		v正文 = 小说下载.f处理正文(v正文)
		return v正文