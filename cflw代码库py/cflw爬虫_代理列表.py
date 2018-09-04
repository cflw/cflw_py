import cflw爬虫 as 爬虫
c地址 = "http://www.xicidaili.com/nn/"
c请求头 = {
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
	"Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0",
}
def f获取文档():
	return 爬虫.f获取文档(c地址, a请求头 = c请求头)
def f解析列_字符串(a元素):
	return a元素.get_text().strip()
def f解析列_国家(a元素):
	v元素 = a元素.find("img")
	if v元素:
		return v元素.get("src")[-6:-4]
	else:
		return ""
def f解析列_延迟时间(a元素):
	v元素 = a元素.find("div", class_ = "bar")
	return float(v元素.get("title")[:-1])
def F解析列_转换(a类型):
	def f(a元素):
		return a类型(f解析列_字符串(a元素))
	return f
ca不处理列 = (f解析列_字符串,) * 10
ca处理列 = (f解析列_国家, f解析列_字符串, F解析列_转换(int), f解析列_字符串, f解析列_字符串, f解析列_字符串, f解析列_延迟时间, f解析列_延迟时间, f解析列_字符串, f解析列_字符串)
def f解析文档(a文档):
	v文档 = 爬虫.fc解析器bs(a文档)
	v表格 = v文档.find("table", id = "ip_list")
	va = []
	for v行 in v表格.find_all("tr"):
		#取列
		def fe列():
			i = 0
			for v列 in v行.children:
				if i % 2 != 0:
					yield v列
				i += 1
		va列 = [v列 for v列 in fe列()]
		#处理列
		va新列 = []
		va处理列 = ca处理列 if va else ca不处理列	#第1行是标题行时,不处理
		for v列, vf in zip(va列, va处理列):
			va新列.append(vf(v列))
		#添加行
		va.append(va新列)
	return va
def f一键获取列表():
	return f解析文档(f获取文档())
