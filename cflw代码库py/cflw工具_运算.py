def f字典按值找键(a字典: dict, a值):
	for v键, v值 in a字典.items():
		if v值 == a值:
			return v键
	return None
def f原值(a):	#不做任何处理的函数
	return a
#2个参数的比较
class C二元比较:
	"2元比较,例如:f大于=F大于();f大于(1,2);"
	class I:
		def __call__(self, a0, a1):
			raise NotImplementedError
	@staticmethod
	def f大于(a0, a1):
		return a0 > a1
	@staticmethod
	def f小于(a0, a1):
		return a0 < a1
	@staticmethod
	def f大于等于(a0, a1):
		return a0 >= a1
	@staticmethod
	def f小于等于(a0, a1):
		return a0 <= a1
	@staticmethod
	def f等于(a0, a1):
		return a0 == a1
	@staticmethod
	def f不等于(a0, a1):
		return a0 != a1
class C向右比较:
	"参数 比 存储值"
	class I:
		def __init__(self, a):
			self.m = a
		def __call__(self, a):
			raise NotImplementedError
	class F大于(I):
		def __call__(self, a):
			return a > self.m
	class F小于(I):
		def __call__(self, a):
			return a < self.m
	class F大于等于(I):
		def __call__(self, a):
			return a >= self.m
	class F小于等于(I):
		def __call__(self, a):
			return a <= self.m
	class F等于(I):
		def __call__(self, a):
			return a == self.m
	class F不等于(I):
		def __call__(self, a):
			return a != self.m