import functools
#===============================================================================
# 常见的对象标识符
#===============================================================================
sysName  	= "1.3.6.1.2.1.1.5"
sysDescr 	= "1.3.6.1.2.1.1.1"
ifNumber 	= "1.3.6.1.2.1.2.1"
ifDescr 	= "1.3.6.1.2.1.2.2.1.2"
ifInOctet 	= "1.3.6.1.2.1.2.2.1.10"
ifOutOctet 	= "1.3.6.1.2.1.2.2.1.16"
ifInUcastPkts = "1.3.6.1.2.1.2.2.1.11"
ifOutUcastPkts = "1.3.6.1.2.1.2.2.1.17"
ipNetToMediaPhysAddress = "1.3.6.1.2.1.4.22.1.2"
ipOperStatus = "1.3.6.1.2.1.2.2.1.8"
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
	@staticmethod
	def fc值(*aa值):
		return S对象标识符(aa值)
	@staticmethod
	def fc字符串(a: str):
		return S对象标识符(a.split("."))
	def f添加(self, a值):
		return S对象标识符(self.ma值 + [a值])
	def f删除末尾(self):
		return S对象标识符(self.ma值[:-1])
	def f末尾加一(self):
		return S对象标识符(self.ma值[:-1] + [self.ma值[-1] + 1])