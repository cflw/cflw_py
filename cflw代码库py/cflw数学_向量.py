import math
from . import cflw数学 as 数学
from . import cflw数学_矩阵 as 矩阵
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
		if v类型 == S向量2:
			x = self.x + a.x
			y = self.y + a.y
		elif v类型 == S极向量2:
			raise NotImplementedError()
		else:
			raise TypeError()
		return S向量2(x, y)
	def __sub__(self, a):
		"向量2 - 向量2"
		v类型 = type(a)
		if v类型 == S向量2:
			x = self.x - a.x
			y = self.y - a.y
		elif v类型 == S极向量2:
			raise NotImplementedError()
		else:
			raise TypeError()
		return S向量2(x, y)
	def __mul__(self, a):
		"向量2 * 实数"
		v = float(a)
		x = self.x * v
		y = self.y * v
		return S向量2(x, y)
	def __truediv__(self, a):
		"向量2 / 实数"
		v = float(a)
		x = self.x / v
		y = self.y / v
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
	def f点乘(self, a向量):
		return self.x * a向量.x + self.y * a向量.y
	def ft向量3(self, az = 0):
		return S向量3(self.x, self.y, az)
	def ft向量4(self, az = 0, aw = 0):
		return S向量4(self.x, self.y, az, aw)
	def ft元组(self):
		return (self.x, self.y)
	def ft极向量2(self):
		return S极向量2.fc直角(self.x, self.y)
	m大小 = property(fg大小, fs大小, None, "向量大小")
	m方向r = property(fg方向r, fs方向r, None, "向量方向(弧度)")
	m方向d = property(fg方向d, fs方向d, None, "向量方向(度)")
S向量2.c零 = S向量2(0, 0)
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
		return 数学.f平方和的平方根(self.x, self.y, self.z)
	def fs大小(self, a大小):
		v倍数 = a大小 / self.fg大小()
		self.x *= v倍数
		self.y *= v倍数
		self.z *= v倍数
	def f点乘(self, a向量):
		return self.x * a向量.x + self.y * a向量.y + self.z * a向量.z
	def f叉乘(self, a向量):
		return S向量3(
			self.y * a向量.z - self.z * a向量.y,
			self.z * a向量.x - self.x * a向量.z,
			self.x * a向量.y - self.y * a向量.z
		)
	def ft向量2(self):
		return S向量2(self.x, self.y)
	def ft向量4(self, aw = 0):
		return S向量4(self.x, self.y, self.z, aw)
	def ft元组(self):
		return (self.x, self.y, self.z)
	m大小 = property(fg大小, fs大小, None, "向量大小")
S向量3.c零 = S向量3(0, 0, 0)
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
		v类型 = type(a)
		if isinstance(a, 矩阵.S矩阵):
			if a.fg行数() != 4 or a.fg列数 != 4:
				raise ValueError("矩阵行列数不匹配")
			v = S向量4()
			for i in range(4):
				for j in range(4):
					v[k] = self[i] * a.fg值(j, i)
			return v
		elif v类型 in (float, int):
			x = self.x * a
			y = self.y * a
			z = self.z * a
			w = self.w * a
			return S向量4(x, y, z, w)
		else:
			raise TypeError()
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
	def __iter__(self):
		yield self.x
		yield self.y
		yield self.z
		yield self.w
	def fg大小(self):
		return 数学.f平方和的平方根(self.x, self.y, self.z, self.w)
	def fs大小(self, a大小):
		v倍数 = a大小 / self.fg大小()
		self.x *= v倍数
		self.y *= v倍数
		self.z *= v倍数
		self.w *= v倍数
	def f点乘(self, a向量):
		return self.x * a向量.x + self.y * a向量.y + self.z * a向量.z + self.w * a向量.w
	def ft向量2(self):
		return S向量2(self.x, self.y)
	def ft向量3(self):
		return S向量3(self.x, self.y, self.z)
	def ft元组(self):
		return (self.x, self.y, self.z, self.w)
	m大小 = property(fg大小, fs大小, None, "向量大小")
S向量4.c零 = S向量4(0, 0, 0, 0)
#===============================================================================
# 极向量2
#===============================================================================
class S极向量2:
	"用极坐标表示的向量"
	def __init__(self, ar, at):
		self.r = ar
		self.t = at
	@staticmethod
	def fc直角(self, ax, ay):
		t = math.atan2(ay, ax)
		r = 数学.f平方和的平方根(ax, ay)
		return S极向量2(r, t)
	def __add__(self, a):
		"极向量加极向量"
		v类型 = type(a)
		if v类型 == S极向量2:
			raise NotImplementedError()
		elif v类型 == S向量2:
			raise NotImplementedError()
		else:
			raise TypeError()
	def __mul__(self, a):
		"极向量乘实数"
		v = float(a)
		r = self.r * v
		return S极向量2(r, self.t)
	def ft向量2(self):
		return S向量2.fc方向r(self.r, self.t)