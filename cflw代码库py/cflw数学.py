import math
#
def f循环(a值, a最小值, a最大值):
	assert(a最小值 < a最大值)
	v差 = a最大值 - a最小值
	v基本倍 = math.floor(a值 / v差)
	v循环倍 = math.ceil(a最小值 / v差)
	return a值 - v差 * (v基本倍 - v循环倍)
def f限制(a值, a最小值, a最大值):
	assert(a最小值 < a最大值)
	if a值 < a最小值:
		return a最小值
	elif a值 > a最大值:
		return a最大值
	else:
		return a值
def fi限制内(a值, a最小值, a最大值):
	assert(a最小值 <= a最大值)
	if a值 < a最小值:
		return False
	elif a值 > a最大值:
		return False
	else:
		return True
def fi限制外(a值, a最小值, a最大值):
	assert(a最小值 < a最大值)
	if a值 < a最小值:
		return True
	elif a值 > a最大值:
		return True
	else:
		return False
def f镜面(a值: float, a最小值: float, a最大值: float):
	"""像镜子一样循环"""
	assert(a最小值 < a最大值)
	v差 = a最大值 - a最小值
	v基本倍 = math.floor(a值 / v差)
	v循环倍 = math.ceil(a最小值 / v差)
	v倍差 = v基本倍 - v循环倍
	v循环 = a值 - v差 * v倍差
	return f对称(v循环, (a最大值 + a最小值) / 2) if v倍差 % 2 else v循环
def f整数镜面(a值: int, a最小值: int, a最大值: int):
	"""[最小值, 最大值]
	1,2,3|3,2,1|1,2,3 这样的"""
	assert(a最小值 < a最大值)
	v结束 = a最大值 + 1
	v差 = v结束 - a最小值
	v基本倍 = a值 // v差
	v相对位置 = a值 - v差 * v基本倍
	return a最大值 - v相对位置 if v基本倍 % 2 else a最小值 + v相对位置	
def f对称(a值, a对称):
	"值关于对称点对称"
	return 2 * a对称 - a值	# a对称 - (a值 - a对称) 
def f插值(a0, a1, a插值):
	return a0 + (a1 - a0) * a插值
def ft合适(a):
	if "." in a:
		return float(a)
	if "∞" in a:
		return math.inf * (-1 if a[0] == "-" else 1)
	return int(a)
#===============================================================================
def f算术平均数(*a):
	return sum(a) / len(a)
def f几何平均数(*a):
	m = 1
	for v in a:
		m *= v
	return math.sqrt(m)
def f平方和的平方根(*a):
	return math.sqrt(sum(v ** 2 for v in a))
#===============================================================================
class S区间:
	def __init__(self, a左值, a左闭, a右值, a右闭):
		self.m左值 = a左值
		self.m左闭 = a左闭
		self.m右值 = a右值
		self.m右闭 = a右闭
	@staticmethod
	def fc左右(a左: tuple, a右: tuple):
		def f(a):
			if type(a) == tuple:
				return a[0], a[1]
			else:
				return a, True
		return S区间(*f(a左), *f(a右))
	@staticmethod
	def fc字符串(a: str, at值 = ft合适):
		v = str(a)
		v左闭 = a[0] == "["
		v右闭 = a[-1] == "]"
		v左值, v右值 = a[1:-1].split(",")
		v左值, v右值 = at值(v左值), at值(v右值)
		return S区间(v左值, v左闭, v右值, v右闭)
	def __str__(self):
		v左符号 = "[" if self.m左闭 else "("
		v右符号 = "]" if self.m右闭 else ")"
		return "%s%d, %d%s" % (v左符号, self.m左值, self.m右值, v右符号) 
	def fi区间内(self, a数字):
		return (self.m左值.__le__ if self.m左闭 else self.m左值.__lt__)(a数字) and (self.m右值.__ge__ if self.m右闭 else self.m右值.__gt__)(a数字)