import time
import cflw字符串 as 字符串
class C版本信息:
	"""show version
	适用于: s3956(v2.2.0B)"""
	def __init__(self, a文本):
		self.m文本
	def fg当前时间(self):
		v字符串 = 字符串.f提取字符串之间(self.m文本, "The current time: ", "\n")    #2019-4-8 10:7:21
		v时间 = time.strptime(v字符串, "%Y-%m-%d %H:%M:%S")
		return v时间