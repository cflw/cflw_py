import cflw字符串 as 字符串
#硬件信息
class C板属性:
	"""display elabel
	适用于: s3700"""
	def __init__(self, a):
		self.m字符串 = 字符串.f提取字符串之间(a, "[Board Properties]\n", "\n\n")
	def fg板类型(self):
		v字符串 = 字符串.f提取字符串之间(self.m字符串, "BoardType=", "\n")
		return v字符串
	def fg板代码(self):
		v字符串 = 字符串.f提取字符串之间(self.m字符串, "BarCode=", "\n")
		return v字符串
	def fg项目(self):
		v字符串 = 字符串.f提取字符串之间(self.m字符串, "Item=", "\n")
		return v字符串
	def fg描述(self):
		v字符串 = 字符串.f提取字符串之间(self.m字符串, "Description=", "\n")
		v长度 = len(v字符串)
		try:
			if v长度 == 10:	#YYYY-MM-DD
				v日期 = time.strptime("%Y-%m-%d")
			elif v长度 == 8:	#YY-MM-DD
				v日期 = time.strptime("%y-%m-%d")
			else:
				return v字符串
			return v日期
		except:
			return v字符串
	def fg生产日期(self):
		v字符串 = 字符串.f提取字符串之间(self.m字符串, "Manufactured=", "\n")
	def fg厂商名(self):
		v字符串 = 字符串.f提取字符串之间(self.m字符串, "VendorName=", "\n")
		return v字符串
class C电子标签信息s3700:
	"""display elabel
	适用于: s3700"""
	def __init__(self, a):
		self.m主板 = C板属性(a)
	def fg序列号(self):
		return self.m主板.fg板代码()
