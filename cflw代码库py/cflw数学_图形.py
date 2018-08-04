import math
class S颜色:
	def __init__(self, r = 0, g = 0, b = 0, a = 1):
		self.r = float(r)
		self.g = float(g)
		self.b = float(b)
		self.a = float(a)
	@staticmethod
	def fc色环(a色环, a饱合度 = 1, a亮度 = 1, a = 1):
		pass
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