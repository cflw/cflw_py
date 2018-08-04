import math
import cflw数学_矩阵 as 矩阵
#===============================================================================
# 任意向量
#===============================================================================
class S向量:
	def __init__(self, n, *t):
		self.m值 = list(t)
def fc向量(a数量, *a值):
	if a数量 < 2:
		raise ValueError()
	elif a数量 == 2:
		return S向量2(*a值)
	elif a数量 == 3:
		return S向量3(*a值)
	elif a数量 == 4:
		return S向量4(*a值)
	else:
		return S向量(a数量, a值)
#===============================================================================
# 向量2
#===============================================================================
class S向量2:
	def __init__(self, ax = 0, ay = 0):
		self.x = ax
		self.y = ay
	def __str__(self):
		return "(" + str(self.x) + ", " + str(self.y) + ")"
	@staticmethod
	def fc方向r(a大小, a方向):
		return S向量2(math.cos(a方向) * a大小, math.sin(a方向) * a大小)
	@staticmethod
	def fc方向d(a大小, a方向):
		v方向 = math.radians(a方向)
		return S向量2.fc方向r(a大小, a方向)
	def __add__(self, a):
		"向量2 + 向量2"
		v类型 = type(a)
		if a == S向量2:
			x = self.x + a.x
			y = self.y + a.y
		else:
			raise TypeError()
		return S向量2(x, y)
	def __mul__(self, a):
		"向量2 * 实数"
		v = float(a)
		x = self.x * v
		y = self.y * v
		return S向量2(x, y)
	def fg大小(self):
		return math.hypot(self.x, self.y)
	def fg方向r(self):
		return math.atan2(self.y, self.x)
	def fg方向d(self):
		return math.degrees(self.fg方向r())
	def fg到点距离(self, a点):
		x = self.x - a点.x
		y = self.y - a点.y
		return math.hypot(x, y)
	def fg到点方向r(self, a点):
		x = a点.x - self.x
		y = a点.y - self.y
		return math.atan2(y, x)
	def fg到点方向d(self, a点):
		return math.degrees(self.fg到点方向r(a点))
	def fs大小(self, a大小):
		v倍数 = a大小 / self.fg大小()
		self.x *= v倍数
		self.y *= v倍数
	def fs方向r(self, a方向):
		v大小 = fg大小()
		self.x = math.cos(a方向) * a大小
		self.y = math.sin(a方向) * a大小
	def fs方向d(self, a方向):
		self.fs方向r(math.radians(a方向))
	m大小 = property(fg大小, fs大小, None, "向量大小")
	m方向r = property(fg方向r, fs方向r, None, "向量方向(弧度)")
	m方向d = property(fg方向d, fs方向d, None, "向量方向(度)")
#===============================================================================
# 向量3
#===============================================================================
class S向量3:
	def __init__(self, ax = 0, ay = 0, az = 0):
		self.x = ax
		self.y = ay
		self.z = az
	def __add__(self, a):
		"向量3 + 向量3"
		v类型 = type(a)
		if v类型 == S向量3:
			return S向量3(self.x + a.x, self.y + a.y, self.z + a.z)
		else:
			raise TypeError()
	def __mul__(self, a):
		"向量3 * 实数"
		v = float(a)
		return S向量3(self.x * v, self.y * v, self.z * v)
	def fg大小(self):
		return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
	def fs大小(self, a大小):
		v倍数 = a大小 / self.fg大小()
		self.x *= v倍数
		self.y *= v倍数
		self.z *= v倍数
	def f点乘(self, a):
		return self.x * a.x + self.y * a.y + self.z * a.z
	def f叉乘(self, a):
		return S向量3(
			self.y * a.z - self.z * a.y,
			self.z * a.x - self.x * a.z,
			self.x * a.y - self.y * a.z
		)

	m大小 = property(fg大小, fs大小, None, "向量大小")
#===============================================================================
# 向量4
#===============================================================================
class S向量4:
	def __init__(self, ax = 0, ay = 0, az = 0, aw = 0):
		self.x = ax
		self.y = ay
		self.z = az
		self.w = aw
	def __mul__(self, a):
		if isinstance(a, 矩阵.S矩阵):
			if a.fg行数() != 4 or a.fg列数 != 4:
				raise ValueError("矩阵行列数不匹配")
			v = S向量4()
			for i in range(4):
				for j in range(4):
					v[k] = self[i] * a.fg值(j, i)
			return v
	def __getitem__(self, k):
		if k == 0:
			return self.x
		elif k == 1:
			return self.y
		elif k == 2:
			return self.z
		elif k == 3:
			return self.w
		else:
			raise IndexError()
	def __setitem__(self, k, v):
		if k == 0:
			self.x = v
		elif k == 1:
			self.y = v
		elif k == 2:
			self.z = v
		elif k == 3:
			self.w = v
		else:
			raise IndexError()
	def fg大小(self):
		return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2 + self.w ** 2)
	def fs大小(self, a大小):
		v倍数 = a大小 / self.fg大小()
		self.x *= v倍数
		self.y *= v倍数
		self.z *= v倍数
		self.w *= v倍数
	m大小 = property(fg大小, fs大小, None, "向量大小")
