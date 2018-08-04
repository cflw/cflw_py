import time
import math
import random
import cflw数学 as 数学
#===============================================================================
# 随机数引擎
#===============================================================================
class I随机数引擎:
	def f生成i(self):
		'生成一个随机数'
		raise NotImplementedError
	def f生成f(self):
		return self.f生成i() / self.fg最大值()
	def fs种子(self):
		'设置随机数引擎的种子'
		raise NotImplementedError
	def f丢弃(self, a次数 = 1):
		i = 0
		while i < a次数:
			self.f生成i()
			i += 1
	def fs种子(self, a种子):
		raise NotImplementedError
	def fg最大值(self):
		'一个随机数引擎所能生成的最大值'
		raise NotImplementedError
	def fg状态(self):
		"取随机数引擎状态"
		raise NotImplementedError
	def fs状态(self, a):
		"设置状态"
		raise NotImplementedError
#具体随机数引擎
class C默认引擎(I随机数引擎):
	def __init__(self):
		self.m值 = 0
	def f生成i(self):
		self.m值 = random.random()
		return self.m值
	def f生成f(self):
		self.m值 = random.random()
		return self.m值
	def fs种子(self, a种子):
		random.seed(a种子)
	def fg最大值(self):
		return 1
	def fg状态(self):
		return random.getstate()
	def fs状态(self, a状态):
		random.setstate(a状态)
class C线性同余(I随机数引擎):
	c构造参数0 = (16807, 1, 2147483647)
	c构造参数1 = (48271, 1, 2147483647)
	def __init__(self, a倍数, a加数, a除数):
		self.m倍数 = int(a倍数)
		self.m加数 = int(a加数)
		self.m除数 = int(a除数)
		self.m值 = 0
	def f生成i(self):
		self.m值 = (self.m值 * self.m倍数 + self.m加数) % self.m除数
		return self.m值
	def fs种子(self, a种子):
		self.m值 = int(a种子) % self.m除数
	def fg最大值(self):
		return self.m除数
class C次数叠加同余(I随机数引擎):
	c最大值 = 2 ** 32 - 1
	def __init__(self, a余数0, a余数1):
		self.m余数0 = a余数0
		self.m余数1 = a余数1
		self.m次数 = 0
		self.m值 = 0
	def f生成i(self):
		self.m值 = (self.m次数 + 1) * (self.m次数 % self.m余数0 + 1) + self.m值 * (self.m次数 % self.m余数1 + 1)
		self.m值 %= C次数叠加同余.c最大值
		self.m次数 += 1
		return self.m值
	def fg状态(self):
		return (self.m值, self.m次数)
	def fs状态(self, a):
		self.m值 = a[0]
		self.m次数 = a[1]
	def fs种子(self, a种子):
		self.m值 = int(a种子) % C次数叠加同余.c最大值
		self.m次数 = int(math.log(self.m值))
	def fg最大值(self):
		return C次数叠加同余.c最大值
#===============================================================================
# 随机数分布
#===============================================================================
class I随机数分布:
	def f转换(self, a):
		raise NotImplementedError
#具体分布
class C整数区间(I随机数分布):
	'得到[a, b)区间内的随机数'
	def __init__(self, a最小值, a最大值):
		#检查参数合法性
		if a最小值 > a最大值:
			raise ValueError
		#赋初始值
		self.m最小值 = int(a最小值)
		self.m最大值 = int(a最大值)
	def f转换(self, a):
		v差 = self.m最大值 - self.m最小值
		v余数 = a * v差
		return self.m最小值 + int(v余数)
class C实数区间(I随机数分布):
	'得到[a, b)区间内的随机数'
	def __init__(self, a最小值, a最大值):
		#检查参数合法性
		if a最小值 > a最大值:
			raise ValueError
		#赋初始值
		self.m最小值 = float(a最小值)
		self.m最大值 = float(a最大值)
	def f转换(self, a):
		v差 = self.m最大值 - self.m最小值
		v余数 = a * v差
		return self.m最小值 + float(v余数)
class C百分比(I随机数分布):
	'0到1'
	def f转换(self, a):
		return float(a)
class C概率(C百分比):
	'有多少的概率得到true'
	def __init__(self, a概率):
		#检查参数合法性
		v概率 = float(a概率)
		if v概率 < 0 or v概率 > 1:
			raise ValueError
		#赋初始值
		self.m概率 = v概率
	def f转换(self, a):
		return float(a) >= self.m概率
class C二项分布(I随机数分布):
	'根据次数和成功率得到成功的次数(随机数)'
	def __init__(self, a次数, a概率):
		#检查参数合法性
		v次数 = int(a次数)
		if v次数 < 1:
			raise ValueError
		v概率 = float(a概率)
		if v概率 < 0 or v概率 > 1:
			raise ValueError
		#赋初始值
		self.m次数 = v次数
		self.m概率 = v概率
	def f转换(self, a):
		v总概率 = self.m概率 * float(a)
		return int(self.m次数 * v总概率)
class C圆形区域(I随机数分布):
	def __init__(self, a圆形):
		self.m圆形 = a圆形
	def f转换(self, a):
		v分割 = C分割随机数.f分割2(a)
		v大小 = v分割[0] * self.m圆形.m半径
		v方向 = v分割[1] * math.pi
		return 数学.S向量2.fc方向r(v大小, v方向)
#===============================================================================
# 随机数工具
#===============================================================================
#生成种子
class C生成种子:
	@staticmethod
	def f时间(a最大值):
		v当前时间 = time.time()
		v小数 = math.modf(v当前时间)[0]
		v整数 = math.floor(v小数 * a最大值)
		return int(v整数)
#生成随机数
class C生成随机数:
	def __init__(self, a0, a1):
		#检查参数
		if isinstance(a0, I随机数引擎):
			if isinstance(a1, I随机数分布):
				v引擎 = a0
				v分布 = a1
			else:
				raise TypeError
		elif isinstance(a0, I随机数分布):
			v分布 = a0
			if isinstance(a1, I随机数引擎):
				v引擎 = a1
			else:
				v引擎 = C默认引擎()
		#赋初始值
		self.m引擎 = v引擎
		self.m分布 = v分布
	def fs种子(self, a种子 = None):
		if a种子 == None:
			self.m引擎.fs种子(C生成种子.f时间(self.m最大值))
		else:
			self.m引擎.fs种子(a种子)
	def f生成(self):
		return self.m分布.f转换(self.m引擎.f生成f())
#随机工具
class C随机工具:
	def __init__(self, a引擎):
		if not issubclass(a引擎, I随机数引擎):
			raise TypeError
		self.m引擎 = a引擎
	def fs种子(self, a种子 = None):
		if a种子 == None:
			self.m引擎.fs种子(C生成种子.f时间(self.m最大值))
		else:
			self.m引擎.fs种子(a种子)
	def f选择(self, a序列):
		'和random.choice()相同功能'
		v索引 = self.m引擎.f生成i() * len(a序列) / (self.m引擎.fg最大值() + 1)
		return a序列[v索引]
class C分割随机数:
	@staticmethod
	def f分割2(a):
		v0 = a
		v1 = 1 / a % 1
		return (v0, v1)
	@staticmethod
	def f分割3(a):
		v0 = a
		v1 = 1 / a % 1
		v2 = 1 / v1 % 1
		return (v0, v1, v2)
	@staticmethod
	def f分割n(a, n):
		a = []
		v = a
		for i in range(n):
			a.append(v)
			v = 1 / v % 1
		return a
def f测试随机质量(a随机数引擎, a次数 = 10000):
	d = {}
	v和 = 0
	v开始时间 = time.time()
	for i in range(a次数):
		v = a随机数引擎.f生成f()
		v和 += v
	#结算
	v结束时间 = time.time()
	d["次数"] = a次数
	d["时间"] = v结束时间 - v开始时间
	d["平均值"] = v和 / a次数
	return d
#===============================================================================
def main():
	#v引擎 = C次数叠加同余(16807, 48271)
	#v引擎 = C线性同余(*C线性同余.c构造参数0)
	v引擎 = C默认引擎()
	v引擎.fs种子(time.time())
	for i in range(10):
		d = f测试随机质量(v引擎, 100000)
		print(d)
if __name__ == "__main__":
	main()