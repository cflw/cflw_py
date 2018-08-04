import math
#===============================================================================
# 任意矩阵
#===============================================================================
class S多维矩阵:
	def __init__(self, a数量: tuple, a值):
		v总数量 = 1
		self.m数量 = []	#表示每一维度的数量
		for v in a数量:
			v数量 = int(v)
			if v数量 < 1:
				raise ValueError
			self.m数量.append(v数量)
			v总数量 *= v数量
		self.m = [0] * v总数量	#值
		v数量 = min(v总数量, len(a值))
		for i in range(v数量):
			self.m[i] = a值[i]
	def __getitem__(self, k):
		v类型 = type(k)
		v维数 = self.fg维数()
		if v类型 == int:
			return self.m[k]
		elif v类型 == tuple:
			return self.fg值(*k)
		elif v类型 == slice:
			if k.step:
				self.fx维数(k.start)
				self.fx维数(k.end)
				v步进类型 = type(k.step)
				if v步进类型 == int:
					v步进值 = (k.step,) * v维数
				elif v步进类型 == tuple:
					self.fx维数(k.step)
				else:
					raise TypeError("无法解析的类型")
			else:
				v步进值 = (1,) * v维数
			def f递归(d, i, l):
				l.append(i)
				if d < v维数 - 1:	#继续递归
					for j in range(k.start[d], k.end[d], k.step[d]):
						f递归(d + 1, j, l)
				else:	#到底
					raise NotImplementedError()
				l.pop()
			for i in range(k.start[0], k.end[0], k.step[0]):
				f递归(0, i, [])
		else:
			raise TypeError("无法解析的类型")
	def fg维数(self):
		return len(self.m数量)
	def fg数量(self):
		return self.m数量
	def fg总数量(self):
		v总 = 1
		for v in self.m数量:
			v总 *= v
		return v总
	def fg值(self, *t):
		return self.m[self.f计算索引(*t)]
	def fx维数(self, t, x = True):
		if self.fg维数() != len(t):
			if x:
				raise ValueError("维数不一致")
			return False
		return True
	def f计算索引(self, *t):
		if not hasattr(self, "mf计算索引"):	#生成乘表
			self.mf计算索引 = F计算矩阵索引(self.m数量)
		return self.mf计算索引(*t)
class F计算矩阵索引:
	def __init__(self, a数量: tuple):
		self.m数量 = a数量
		self.m乘表 = [1] * self.m数量
		v积 = 1
		for i in range(v维数 - 2, -1, -1):
			v积 *= self.m数量[i]
			self.m乘表[i] = v积
	def __call__(self, *a):
		if len(a) != self.m数量:
			raise ValueError("维数不一致")
		v索引 = 0
		for i in range(self.m数量):
			v索引 += self.m乘表[i] * a[i]
		return v索引
#===============================================================================
# 任意二维矩阵
#===============================================================================
class S矩阵:
	def __init__(self, a数量: tuple, a值):
		if len(a数量) != 2:
			raise ValueError()
		self.m行 = int(a数量[0])
		self.m列 = int(a数量[1])
		self.m数量 = self.m行 * self.m列
		v参数值数 = len(a值)
		if v参数值数 > self.m数量:
			self.m值 = a值[:self.m数量]
		else:
			self.m值 = a值 + [0] * (self.m数量 - v参数值数)
	def __str__(self):
		s = ""
		for i in range(self.m行):
			v开始 = i * self.m列
			if i == 0:
				v开始字符, v结束字符 = "┌", "┐"
			elif i == self.m行 - 1:
				v开始字符, v结束字符 = "└", "┘"
			else:
				v开始字符, v结束字符 = "│", "│"
			s += v开始字符 + "\t".join([str(v) for v in self.m值[v开始 : v开始 + self.m列]]) + v结束字符 + "\n"
		return s
	def __add__(self, a矩阵):
		if self.m行 != a矩阵.m行 or self.m列 != a矩阵.m列:
			raise ValueError("矩阵行列数不匹配")
		v值 = [0] * self.m数量
		for i in range(self.m行):
			for j in range(self.m列):
				v索引 = i * self.m列 + j
				v值[v索引] = S矩阵.f值相加(self.m值[v索引], a矩阵.m值[v索引])
		return S矩阵((self.m行, self.m列), v值)
	def __mul__(self, a矩阵):
		if self.m列 != a矩阵.m行:
			raise ValueError("矩阵行列数不匹配")
		v行 = self.m行
		v列 = a矩阵.m列
		v总数 = v行 * v列
		v值 = [0] * v总数
		for i in range(v行):
			for j in range(v列):
				ok = i * v列 + j
				for k in range(self.m列):
					ak = i * self.m列 + k
					bk = k * a矩阵.m列 + j
					v值[ok] = S矩阵.f值相加(v值[ok], S矩阵.f值相乘(self.m值[ak], a矩阵.m值[bk]))
		return S矩阵((v行, v列), v值)
	def __getitem__(self, k):
		return self.m值[self.f计算索引(k[0], k[1])]
	def fg行数(self):
		return self.m行
	def fg列数(self):
		return self.m列
	def fg值(self, i, j):
		return self.m值[self.f计算索引(i, j)]
	def f计算索引(self, i, j):
		return i * self.m列 + j
	@staticmethod
	def f值相加(a, b):
		va是数字 = type(a) in (int, float)
		vb是数字 = type(b) in (int, float)
		if va是数字 and vb是数字:
			return a + b
		if va是数字 and a == 0:
			return b
		if vb是数字 and b == 0:
			return a
		return str(a) + "+" + str(b)
	@staticmethod
	def f值相乘(a, b):
		def f加括号(a):
			v = str(a)
			if "+" in v:
				return "(" + v + ")"
			else:
				return v
		va是数字 = type(a) in (int, float)
		vb是数字 = type(b) in (int, float)
		if va是数字 and vb是数字:
			return a * b
		if va是数字:
			if a == 0:
				return 0
			elif a == 1:
				return b
		if vb是数字:
			if b == 0:
				return 0
			elif b == 1:
				return a
		return f加括号(a) + "*" + f加括号(b)
#===============================================================================
# 二阶矩阵
#===============================================================================
class S矩阵2(S矩阵):
	def __init__(self, a值):
		S矩阵.__init__(self, (2, 2), a值)
	@staticmethod
	def fc单位():
		return S矩阵2([
			1, 0,
			0, 1
		])
	@staticmethod
	def fc旋转(a):
		s = math.sin(a)
		c = math.cos(a)
		return S矩阵2x2([
			c, s, 
			s, c
		])
	@staticmethod
	def fc缩放(a):
		v类型 = a
		if v类型 in (tuple, list):
			if len(a) != 2:
				raise ValueError()
			x = a[0]
			y = a[1]
		raise NotImplementedError()
#===============================================================================
# 三阶矩阵
#===============================================================================
class S矩阵3(S矩阵):
	def __init__(self, a值):
		S矩阵.__init__(self, (3, 3), a值)
	@staticmethod
	def fc单位():
		return S矩阵3([
			1, 0, 0,
			0, 1, 0,
			0, 0, 1
		])
#===============================================================================
# 四阶矩阵
#===============================================================================
class S矩阵4(S矩阵):
	def __init__(self, a值):
		S矩阵.__init__(self, (4, 4), a值)
	@staticmethod
	def fc单位():
		return S矩阵4([
			1, 0, 0, 0,
			0, 1, 0, 0,
			0, 0, 1, 0,
			0, 0, 0, 1
		])
#===============================================================================
# 测试代码
#===============================================================================
def main():
	m1 = S矩阵4([
		1, 0, 0, 0, 
		0, "cx", "sx", 0, 
		0, "-sx", "cx", 0, 
		0, 0, 0, 1
	])
	m2 = S矩阵4([
		"cy", 0, "-sy", 0,
		0, 1, 0, 0,
		"sy", 0, "cy", 0,
		0, 0, 0, 1
	])
	m3 = S矩阵4([
		"cz", "sz", 0, 0,
		"-sz", "cz", 0, 0,
		0, 0, 1, 0,
		0, 0, 0, 1
	])
	print(m1 * m2, m1 * m3, m2 * m3, m1 * m2 * m3, sep = '')
if __name__ == "__main__":
	main()