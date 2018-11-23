import pathlib
import sys
import time
import re
import cflw爬虫 as 爬虫
c开头缩进正则 = re.compile(r"^\s")
class I文档:	#用来继承
	def __init__(self):
		self.m文档 = None
	def f重新载入(self):
		self.m文档 = 爬虫.fc解析器bs(爬虫.f获取文档(self.fg地址()))
	def f载入(self):
		if not self.m文档:
			self.f重新载入()
	def fg地址(self):
		raise NotImplementedError()
class I小说(I文档):
	def __init__(self):
		I文档.__init__(self)
	def fe目录(self):
		"返回(章节名, I章节 对象)"
		raise NotImplementedError()
class I章节(I文档):
	def __init__(self):
		I文档.__init__(self)
	def fg正文(self):
		"返回字符串"
		raise NotImplementedError()
class C写文件:
	def __init__(self, a文件名):
		self.m文本名 = a文件名
		self.m文件 = open(a文件名, "w", encoding = "utf-8")
	def f写章节(self, a章节名, a正文):
		self.m文件.write(a章节名 + "\n" + a正文 + "\n")
def f一键下载(a小说, a保存路径):
	#信息
	for i in range(5):
		try:
			v小说名 = a小说.fg小说名()
			print("下载《" + v小说名 + "》")
			va目录 = list(a小说.fe目录())
		except Exception as e:
			if i == 4:
				raise RuntimeError("失败次数过多")
			else:
				time.sleep(1)
				a小说.f重新载入()
				continue
		else:
			break
	#路径
	v路径 = pathlib.Path(a保存路径)
	v路径 /= v小说名 + ".txt"
	v路径字符串 = str(v路径)
	print("保存到: " + v路径字符串)
	v写文件 = C写文件(v路径字符串)
	#循环
	v数量 = len(va目录)
	i = 0
	for v in va目录:
		v章节名 = v[0]
		v章节 = v[1]
		for i1 in range(5):
			try:
				v正文 = v章节.fg正文()
				v写文件.f写章节(v章节名, v正文)
			except Exception as e:
				if i1 == 4:
					raise RuntimeError("失败次数过多")
				else:
					time.sleep(1)
					v章节.f重新载入()
					continue
			else:
				break
		i += 1
		sys.stdout.write("已下载:%d/%d(%.2f%%)" % (i, v数量, i / v数量 * 100) + " " * 10 + "\r")
		sys.stdout.flush()
	print("\n下载完成")
def f处理正文(a文本):
	v正文文本 = a文本
	c开头缩进正则.sub(v正文文本, "")	#清除缩进
	v正文文本 = v正文文本.replace("\xa0", "")	#清除缩进
	v正文文本 = v正文文本.replace("\u3000", "")	#清除缩进
	v正文文本 = v正文文本.replace("\r", "\n")	#
	v正文文本 = v正文文本.replace("\n \n", "\n")	#清除多余换行
	while "\n\n" in v正文文本:
		v正文文本 = v正文文本.replace("\n\n", "\n")	#清除多余换行
	return v正文文本
def f删除链接后缀(a链接: str):
	v链接 = a链接
	v后缀位置 = v链接.find(".htm")
	if v后缀位置 > 0:
		v链接 = v链接[:v后缀位置]
	return v链接