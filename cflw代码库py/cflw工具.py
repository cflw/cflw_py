import math
import re
c数字正则 = re.compile(r"\d+")
class S版本号:
	def __init__(self, aa版本):
		self.ma版本 = list(int(v) for v in aa版本)
	def __str__(self):
		return ".".join(str(v) for v in self.ma版本)
	def __repr__(self):
		return "<S版本号: " + repr(self.ma版本) + ">"
	def __cmp__(self, a):
		v类型 = type(a)
		if v类型 == S版本号:
			v长度0 = len(self.ma版本)
			v长度1 = len(a.ma版本)
			for i in range(min(v长度0, v长度1)):
				v比较 = self.ma版本[i] - a.ma版本[i]
				if v比较 != 0:
					return v比较
			return v长度0 - v长度1
		elif v类型 == int:
			return self.ma版本[0] - a
		elif v类型 == float:
			v版本号 = S版本号.fc小数(a)
			return self.__cmp__(v版本号)
		elif v类型 == str:
			v版本号 = S版本号.fc字符串(a)
			return self.__cmp__(v版本号)
		elif v类型 in (list, tuple):
			v版本号 = S版本号.fc元组(a)
			return self.__cmp__(v版本号)
		else:
			raise TypeError("无法解析的类型")
	def __eq__(self, a):
		return self.__cmp__(a) == 0
	def __ne__(self, a):
		return self.__cmp__(a) != 0
	def __lt__(self, a):
		return self.__cmp__(a) < 0
	def __le__(self, a):
		return self.__cmp__(a) <= 0
	def __gt__(self, a):
		return self.__cmp__(a) > 0
	def __ge__(self, a):
		return self.__cmp__(a) >= 0
	def __getitem__(self, k):
		if k >= len(self.ma版本):
			return 0
		else:
			return self.ma版本[k]
	def __setitem__(self, k, v):
		v长度 = len(self.ma版本)
		if k >= v长度:
			self.ma版本.extend([0] * (v长度 - k))
			self.ma版本.append(v)
		else:
			self.ma版本[k] = v
	def __len__(self):
		return len(self.ma版本)
	@staticmethod
	def fc自动(*a):
		v长度 = len(a)
		if v长度 == 0:
			raise ValueError("必需有参数")
		if v长度 > 1:
			return S版本号(a)
		v = a[0]
		v类型 = type(v)
		if v类型 == int:
			return S版本号.fc整数(v)
		elif v类型 == float:
			return S版本号.fc小数(v)
		elif v类型 == str:
			return S版本号.fc字符串(v)
		elif v类型 in (list, tuple):
			return S版本号.fc元组(v)
		elif v类型 == S版本号:
			return S版本号(v.ma版本)
		else:
			raise TypeError("无法解析的类型")
	@staticmethod
	def fc字符串(a字符串: str):
		va分割 = a字符串.split(".")
		def f处理(a段):
			va数字 = c数字正则.findall(a段)
			return int(va数字[0])
		v元组 = tuple(f处理(v) for v in va分割)
		return S版本号.fc分段(*v元组)
	@staticmethod
	def fc分段(*a元组):
		return S版本号(a元组)
	@staticmethod
	def fc数字(a):
		v类型 = type(a)
		if v类型 == int:
			return S版本号.fc整数(a)
		elif v类型 == float:
			return S版本号.fc小数(a)
		else:
			raise TypeError("无法解析的类型")
	@staticmethod
	def fc整数(a: int):
		return S版本号((a,))
	@staticmethod
	def fc小数(a: float):
		v整数 = math.floor(a)
		v小数 = a - v整数
		if v小数 > 0:	#可能有0.0
			v小数 = v小数 * 10 ** math.ceil(-math.log10(v小数))
		return S版本号.fc分段(v整数, v小数)
	@staticmethod
	def fc元组(a元组: tuple):
		return S版本号(a元组)
	def ft元组(self):
		return self.ma版本