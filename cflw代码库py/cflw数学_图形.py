import math
import cflw数学 as 数学
class S颜色:
	def __init__(self, r = 0, g = 0, b = 0, a = 1):
		self.r = float(r)
		self.g = float(g)
		self.b = float(b)
		self.a = float(a)
	@staticmethod
	def fc红绿蓝全彩(r, g, b, a饱合度 = 1, a亮度 = 1, a = 1):
		v最大 = max(r, g, b)
		assert(v最大 > 0)
		r = 数学.f插值(1, r / v最大, a饱合度) * a亮度
		g = 数学.f插值(1, g / v最大, a饱合度) * a亮度
		b = 数学.f插值(1, b / v最大, a饱合度) * a亮度
		return S颜色(r, g, b, a)
	@staticmethod
	def fc色环(a色环, a饱合度 = 1, a亮度 = 1, a = 1):
		"0~1:红~红"
		return fc色环(a色环 * 3, a饱合度, a亮度, a)
	@staticmethod
	def fc三基色环(a环, a饱合度 = 1, a亮度 = 1, a = 1):
		"0红1绿2蓝"
		v = 数学.f循环(a环, 0, 3)
		if v < 1:
			r = 数学.f插值(1, 0, v)
			g = 数学.f插值(0, 1, v)
			b = 0
		elif v < 2:
			v插值 = v - 1
			r = 0
			g = 数学.f插值(1, 0, v插值)
			b = 数学.f插值(0, 1, v插值)
		else:	#v <= 3
			v插值 = v - 2
			r = 数学.f插值(0, 1, v插值)
			g = 0
			b = 数学.f插值(1, 0, v插值)
		return fc红绿蓝全彩(r, g, b, a饱合度, a亮度, a)
	@staticmethod
	def fc彩虹(a环, a饱合度 = 1, a亮度 = 1, a = 1):
		v = 数学.f循环(a环, 0, 7)
		if v < 2:	#红->黄
			v插值 = v / 2
			r = 1
			g = 数学.f插值(0, 1, v插值)
			b = 0
		elif v < 3:	#黄->绿
			v插值 = v - 2
			r = 数学.f插值(0, 1, v插值)
			g = 1
			b = 0
		elif v < 5:	#绿->蓝
			v插值 = (v - 3) / 2
			r = 0
			g = 数学.f插值(1, 0, v插值)
			b = 数学.f插值(0, 1, v插值)
		else:	#5~7:蓝->红
			v插值 = (v - 5) / 2
			r = 数学.f插值(0, 1, v插值)
			g = 0
			b = 数学.f插值(1, 0, v插值)
		return fc红绿蓝全彩(r, g, b, a饱合度, a亮度, a)
	def __getitem__(self, k):
		if k == 0:
			return self.r
		elif k == 1:
			return self.g
		elif k == 2:
			return self.b
		elif k == 3:
			return self.a
		else:
			raise KeyError()
	def __setitem__(self, k, v):
		if k == 0:
			self.r = float(v)
		elif k == 1:
			self.g = float(v)
		elif k == 2:
			self.b = float(v)
		elif k == 3:
			self.a = float(v)
		else:
			raise KeyError()
	def __eq__(self, a):
		return self.r == a.r and self.g == a.g and self.b == a.b and self.a == a.a
	def __ne__(self, a):
		return self.r != a.r or self.g != a.g or self.b != a.b or self.a != a.a
	def f分量乘(self, a颜色: S颜色):
		r = self.r * a颜色.r
		g = self.g * a颜色.g
		b = self.b * a颜色.b
		a = self.a * a颜色.a
		return S颜色(r, g, b, a)
	def ft元组(self):
		return (self.r, self.g, self.b, self.a)
	def ft元组rgb(self):
		return (self.r, self.g, self.b)
	ft元组rbga = S颜色.ft元组