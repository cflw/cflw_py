import functools
#===============================================================================
# 接口
#===============================================================================
class I简单网管:
	def f获取(self, a标识):
		"""snmpget"""
		raise NotImplementedError()
	def f遍历(self, a开始, a结束):
		"""snmpwalk"""
		raise NotImplementedError()
	def f设置(self, a标识, a值):
		"""snmpset"""
		raise NotImplementedError()
	def f陷阱(self, a标识):
		"""snmptrap"""
		raise NotImplementedError()
#===============================================================================
# 结构
#===============================================================================
@functools.total_ordering
class S对象标识符:
	def __init__(self, aa值):
		self.ma值 = list(aa值)
	def __eq__(self, a):
		return self.ma值 == a
	def __lt__(self, a):
		return self.ma值 < a
	def __len__(self):
		return len(self.ma值)
	def __getitem__(self, k):
		return self.ma值[k]
	def __setitem__(self, k, v):
		self.ma值[k] = v
	def __str__(self):
		return "." + ".".join(map(str, self.ma值))
	@staticmethod
	def fc自动(*a):
		v长度 = len(a)
		if v长度 > 1:	#视为多个值
			return S对象标识符.fc值(*a)
		v = a[0]
		v类型 = type(v)
		if v类型 == str:
			return S对象标识符.fc字符串(v)
		elif v类型 in (tuple, list):
			return S对象标识符.fc值(*v)
		elif v类型 == S对象标识符:
			return v
		else:
			raise TypeError("无法解析的类型")
	@staticmethod
	def fc值(*aa值):
		return S对象标识符(aa值)
	@staticmethod
	def fc字符串(a: str):
		if a[0] == '.':
			return S对象标识符(map(int, a[1:].split(".")))
		else:
			return S对象标识符(map(int, a.split(".")))
	def f添加(self, a值):
		return S对象标识符(self.ma值 + [a值])
	def f删除末尾(self):
		return S对象标识符(self.ma值[:-1])
	def f末尾加一(self):
		return S对象标识符(self.ma值[:-1] + [self.ma值[-1] + 1])