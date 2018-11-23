import re
import cflw爬虫 as 爬虫
c地址 = "http://www.txtbook.com.cn"	#这个网站全是广告下载不了小说
c在线阅读正则 = re.compile(r"""<a> href="(.+)" target="_blank">【在线阅读】<\/a>""")
def f提取阅读地址(a地址):
	v文档 = 爬虫.f获取文档(a地址):
	v结果 = c在线阅读正则.search(v文档)
	return v结果.group(1)
