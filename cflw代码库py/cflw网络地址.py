import ipaddress
import re
import struct
import math
import cflw字符串 as 字符串
#===============================================================================
# 常量
#===============================================================================
cipv4正则 = re.compile(r"(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}")
cipv6正则 = re.compile(r"([a-f0-9]{1,4}(:[a-f0-9]{1,4}){7}|[a-f0-9]{1,4}(:[a-f0-9]{1,4}){0,7}::[a-f0-9]{0,4}(:[a-f0-9]{1,4}){0,7})")
c前缀正则 = re.compile(r"\/\d{1,3}\s")
#===============================================================================
# 创建地址对象
#===============================================================================
def f解析地址字符串(a地址: str, a严格: bool = True):	#返回地址或网络号对象
	if '/' in a地址:
		return ipaddress.IPv4Network(a地址, a严格)
	elif '-' in a地址:
		return C连续地址4(a地址)
	else:
		return ipaddress.IPv4Address(a地址)
class C互联网协议4:
	"静态类,对ipaddress模块的完善"
	@staticmethod
	def fc网络(a地址, a严格: bool = True):
		v类型 = type(a地址)
		if v类型 == ipaddress.IPv4Network:
			return a地址
		elif v类型 == tuple:
			return ipaddress.IPv4Network('%s/%s' % a地址[0:2], a严格)
		elif v类型 == list:
			return ipaddress.IPv4Network('%s/%s' % tuple(a地址[0:2]), a严格)
		elif v类型 == str:
			return ipaddress.IPv4Network(a地址, a严格)
		elif hasattr(v类型, '__str__'):
			return ipaddress.IPv4Network(str(a地址), a严格)
		else:
			raise TypeError()
	@staticmethod
	def fc接口(a地址):
		v类型 = type(a地址)
		if v类型 == ipaddress.IPv4Interface:
			return a地址
		elif v类型 == tuple:
			return ipaddress.IPv4Interface('%s/%s' % a地址[0:2])
		elif v类型 == list:
			return ipaddress.IPv4Interface('%s/%s' % tuple(a地址[0:2]))
		elif v类型 == str:
			return ipaddress.IPv4Interface(a地址)
		elif hasattr(v类型, '__str__'):
			return ipaddress.IPv4Interface(str(a地址))
		else:
			raise TypeError()
	@staticmethod
	def fc掩码_长度(a长度):
		return ipaddress.IPv4Address(2 ** 32 - 2 ** (32 - a长度))
	@staticmethod
	def fc反掩码_长度(a长度):
		return ipaddress.IPv4Address(2 ** (32 - a长度) - 1)
	@staticmethod
	def f补全地址(a完整地址: str, a空缺地址: str):
		'''使用完整地址的前缀来填补空缺地址的前缀
	例如：有2个地址"192.168.0.1"、"2"，可以把第2个地址补为"192.168.0.2"'''
		v地址0 = a完整地址.split('.')
		v地址1 = a空缺地址.split('.')
		while True:
			v数量 = len(v地址1)
			assert(v数量 <= 4)
			if v地址1[0] == '':
				v地址1[0] = v地址0[4 - v数量]
			if v数量 == 4:
				break
			else:
				v地址1.insert(0, v地址0[3 - v数量])
		return '%s.%s.%s.%s' % tuple(v地址1)
	@staticmethod
	def f分割地址掩码(a地址):
		v类型 = type(a地址)
		if v类型 in (ipaddress.IPv4Network, ipaddress.IPv4Interface):
			return a地址.with_netmask.split('/')
		else:
			raise TypeError()
	@staticmethod
	def f分割地址反掩码(a地址):
		v类型 = type(a地址)
		if v类型 in (ipaddress.IPv4Network, ipaddress.IPv4Interface):
			v反掩码 = C互联网协议4.fc反掩码_长度(a地址.prefixlen)
			return (a地址.network_address, v反掩码)
		else:
			raise TypeError()
	@staticmethod
	def f互补(a地址):
		v类型 = type(a地址)
		if v类型 == ipaddress.IPv4Address:
			v地址 = a地址
		elif v类型 in (ipaddress.IPv4Network, ipaddress.IPv4Interface):
			v地址 = a地址.network_address
		else:
			raise TypeError()
		v整数 = 2 ** 32 - 1 - int(v地址)
		return ipaddress.IPv4Address(v整数)
#===============================================================================
# 网络地址4
#===============================================================================
class S网络地址4:
	"ipv4地址结构"
	c最大前缀长度 = 32
	c全f = 0xffffffff
	def __init__(self):
		self.m地址 = 0
		self.m前缀长度 = 0
	def __str__(self):
		v字符串 = self.fg地址s()
		v长度 = self.fg前缀长度()
		if v长度 > 0:
			v字符串 += "/" + str(v长度)
		return v字符串
	@staticmethod
	def fc自动(*a):
		"""
		可用字符串格式：x.x.x.x/n
			例如："1.1.1.1/24"
		可用的其它类型：ipaddress模块中的ipv4相关类\n
		可用的多参数：(地址, 掩码)
		"""
		v这 = S网络地址4()
		v长度 = len(a)
		if v长度 > 1:
			v1 = a[1]
		else:
			v1 = 32
		v0 = a[0]
		v类型0 = type(v0)
		if v类型0 == S网络地址4:	#参数类型(S网络地址4)
			if v长度 > 1:
				raise TypeError("参数太多")
			v这.m地址 = v0.m地址
			v这.m前缀长度 = v0.m前缀长度
		elif v类型0 == str:
			#取参数
			if "/" in v0:
				if v0.count("/") != 1:
					raise ValueError("斜杠太多")
				v地址, v1 = v0.split("/")
			else:
				v地址 = v0
			#赋值
			if type(v1) == str:
				v这.m前缀长度 = S网络地址4.f掩码字符串转前缀长度(v1)
			else:
				v这.m前缀长度 = int(v1)
			v这.m地址 = S网络地址4.f地址字符串转整数(v地址)
		elif v类型0 == int:	#地址是整数
			v这.m地址 = v0
			v这.m前缀长度 = S网络地址4.f掩码字符串转前缀长度(v1)
		elif v类型0 in (ipaddress.IPv4Network, ipaddress.IPv4Interface):
			v地址, v1 = v0.with_prefixlen
			v这.m地址 = S网络地址4.f地址字符串转整数(v地址)
			v这.m前缀长度 = int(v1)
		elif v类型0 == ipaddress.IPv4Address:
			v这.m地址 = int(v0)
			v这.m前缀长度 = v1
		else:
			raise TypeError("无法解析参数类型")
		return v这
	@staticmethod
	def fc地址字符串(a地址):
		v这 = S网络地址4()
		v这.m地址 = S网络地址4.f地址字符串转整数(a地址)
		return v这
	@staticmethod
	def fc地址前缀长度(a地址, a前缀长度):
		v这 = S网络地址4()
		if type(a地址) == str:
			v这.m地址 = S网络地址4.f地址字符串转整数(a地址)
		else:
			v这.m地址 = int(a地址)
		v这.m前缀长度 = int(a前缀长度)
		return v这
	@staticmethod
	def fc地址掩码(a地址, a掩码):
		v这 = S网络地址4()
		if type(a地址) == str:
			v这.m地址 = S网络地址4.f地址字符串转整数(a地址)
		else:
			v这.m地址 = int(a地址)
		if type(a掩码) == str:
			v这.m前缀长度 = S网络地址4.f掩码字符串转前缀长度(a掩码)
		else:
			v这.m前缀长度 = S网络地址4.f掩码整数转前缀长度(int(a掩码))
		return v这
	@staticmethod
	def f地址字符串转整数(a):
		assert(type(a) == str)
		if a.count(".") != 3:
			raise ValueError()
		v = a.split(".")
		return int(v[0]) * 2 ** 24 + int(v[1]) * 2 ** 16 + int(v[2]) * 2 ** 8 + int(v[3])
	@staticmethod
	def f掩码字符串转前缀长度(a):
		"处理正掩码,反掩码,前缀长度3种格式"
		if "." in a:
			v整数 = S网络地址4.f地址字符串转整数(a)
			#1..0
			if v整数 & 0x80000000:
				v整数 = 0xffffffff - v整数
			#0..1
			elif v整数 & 0x00000001:
				pass
			else:	#未知格式
				v整数 = 0
			return 32 - int(math.log2(v整数 + 1))
		else:
			return int(a)
	@staticmethod
	def f掩码整数转前缀长度(a):
		"参数必需是正掩码或前缀长度"
		if a > 32:
			return 32 - math.log2(a + 1)
		else:
			return a
	@staticmethod
	def f字节转整数(a):
		struct.unpack(">L", a)
	@staticmethod
	def f地址整数转字符串(a):
		if type(a) != int:
			raise TypeError("参数必需是整数")
		va = ["0", "0", "0", "0"]
		v数字 = a
		for i in range(4):	#数字转字符串后需要反转
			va[i] = str(v数字 % 256)
			v数字 //= 256
		va.reverse()
		return ".".join(va)
	@staticmethod
	def fi地址格式(a):
		v类型 = type(a)
		if v类型 == str:
			v点数 = a.count(".")
			if v点数 != 3:
				return False
			va列表 = a.split(".")
			try:
				for v in va列表:
					v数字 = int(v)
					if v数字 > 255:
						return False
			except:
				return False
			#没问题
			return True
		elif v类型 in (S网络地址4, ipaddress.IPv4Address, ipaddress.IPv4Interface, ipaddress.IPv4Network):
			return True
		else:
			return False
	def fg地址s(self):
		return S网络地址4.f地址整数转字符串(self.fg地址i())
	def fg地址i(self):
		return self.m地址
	def fg网络号(self):
		'返回地址'
		v地址 = self.fg网络号i()
		return S网络地址4(v地址, self.m前缀长度)
	def fg网络号s(self):
		return S网络地址4.f地址整数转字符串(self.fg网络号i())
	def fg网络号i(self):
		'返回整数'
		return self.m地址 & self.fg掩码i()
	def fg广播地址(self):
		'返回地址'
		v地址 = self.fg广播地址i()
		return S网络地址4(v地址, self.m前缀长度)
	def fg广播地址i(self):
		'返回整数'
		return self.m地址 | self.fg反掩码i()
	def fg掩码s(self):
		return S网络地址4.f地址整数转字符串(self.fg掩码i())
	def fg掩码i(self):
		return S网络地址4.c全f - 2 ** (S网络地址4.c最大前缀长度 - self.m前缀长度) + 1
	def fg反掩码s(self):
		return S网络地址4.f地址整数转字符串(self.fg反掩码i())
	def fg反掩码i(self):
		return 2 ** (S网络地址4.c最大前缀长度 - self.m前缀长度) - 1
	def fg前缀长度(self):
		return self.m前缀长度
	def fg主机地址数(self):
		return 2 ** (S网络地址4.c最大前缀长度 - self.m前缀长度) - 2
	def fe主机地址(self):
		v范围 = range(self.fg网络号i() + 1, self.fg广播地址i())
		for i in v范围:
			yield S网络地址4(i, self.m前缀长度)
	def fi范围内(self, a地址, a真子集 = False):
		if self.m前缀长度 < a地址.m前缀长度:
			return False
		if self.m前缀长度 == a地址.m前缀长度 and a真子集:
			return False
		return self.fg网络号i() == a地址.m地址 & self.fg掩码i()
#===============================================================================
# 网络地址6
#===============================================================================
class S网络地址6:
	"ipv6地址"
	c最大前缀长度 = 128
	c全f = 0xffffffffffffffffffffffffffffffff
	c多个零正则 = re.compile(r"(\:0){2,6}")
	def __init__(self):
		self.m地址 = 0
		self.m前缀长度 = 0
	def __str__(self):
		return self.ft字符串()
	@staticmethod
	def fc自动(*a):
		"""
		字符串格式："x:x:x:x:x:x:x:x/64"（可以使用缩写地址）
		"""
		v这 = S网络地址6()
		v长度 = len(a)
		if v长度 > 1:
			v前缀长度 = a[1]
		else:
			v前缀长度 = 128
		v0 = a[0]
		v类型 = type(v0)
		if v类型 == str:
			#取参数
			if "/" in v0:
				if v0.count("/") != 1:
					raise ValueError("斜杠太多")
				v地址, v前缀长度 = a.split("/")
			else:
				v地址 = v0
			#赋值
			v这.m前缀长度 = int(v前缀长度)
			v这.m地址 = S网络地址6.f地址字符串转整数(v地址)
		elif v类型 == int:
			v这.m地址 = v0
			v这.m前缀长度 = int(v前缀长度)
		elif v类型 in (ipaddress.IPv6Network, ipaddress.IPv6Interface):
			v地址, v前缀长度 = v0.with_prefixlen
			v这.m地址 = S网络地址6.f地址字符串转整数(v地址)
			v这.m前缀长度 = int(v前缀长度)
		elif v类型 == ipaddress.IPv6Address:
			v这.m地址 = int(v0)
			v这.m前缀长度 = 128
		return v这
	@staticmethod
	def fc地址前缀长度(a地址, a前缀长度):
		v这 = S网络地址6()
		if type(a地址) == str:
			v这.m地址 = S网络地址6.f地址字符串转整数(a地址)
		else:
			v这.m地址 = int(a地址)
		v这.m前缀长度 = a前缀长度
		return v这
	@staticmethod
	def f地址字符串转整数(a):
		v类型 = type(a)
		if v类型 == str:
			v字符串 = str(a)
			v冒号数量 = v字符串.count(":")
			if v冒号数量 < 2 or v冒号数量 > 8:
				raise ValueError("冒号太少或太多")
			#填充,把::改为:0:0:0:0
			v位置 = a.find("::")
			v插入字符串 = ":0" * (8 - v冒号数量)
			v字符串 = v字符串[:v位置] + v插入字符串 + v字符串[v位置+1:]
			#转换
			v数字 = 0
			v分割 = v字符串.split(":")
			for v in v分割:
				v长度 = len(v)
				if v长度 > 4:
					raise ValueError("字符数量太多")
				v数字 = v数字 * 0x10000 + int(v, 16)
			return v数字
		else:
			raise TypeError
	@staticmethod
	def fi地址格式(a):
		return True
	def fg网络号(self):
		v地址 = self.fg网络号i()
		return S网络地址6.fc地址前缀长度(v地址, self.m前缀长度)
	def fg网络号i(self):
		return self.m地址 & (S网络地址6.c全f - 2 ** (128 - self.m前缀长度) + 1)
	def fg广播地址(self):
		v地址 = self.fg广播地址i()
		return S网络地址6.fc地址前缀长度(v地址, self.m前缀长度)
	def fg广播地址i(self):
		return self.m地址 | (2 ** (128 - self.m前缀长度) - 1)
	def ft字符串(self):
		v分段 = [0, 0, 0, 0, 0, 0, 0, 0]
		#地址分割
		v地址 = self.m地址
		for i in range(8):
			v数字 = v地址 % 0x10000
			v分段[7-i] = v数字
			v地址 //= 0x10000
		#地址转字符串
		for i in range(8):
			v分段[i] = hex(v分段[i])[2:]	#去掉0x
		v字符串 = ":".join(v分段)
		v字符串 = S网络地址6.c多个零正则.sub(":", v字符串, 1)
		return v字符串
	def fg主机地址数(self):
		return 2 ** (S网络地址6.c最大前缀长度 - self.m前缀长度) - 2
	def fg前缀长度(self):
		return self.m前缀长度
#===============================================================================
# 物理地址
#===============================================================================
class S物理地址:
	"mac地址"
	c查找符号 = re.compile(r"[\.\-\:]")
	def __init__(self, a值 = 0):
		self.m值 = a值
	@staticmethod
	def fc整数(a: int):
		return S物理地址(a)
	@staticmethod
	def fc字符串(a: str):
		v类型 = type(a)
		if v类型 == str:
			v字符串 = re.sub(S物理地址.c查找符号, "", a)
			if len(v字符串) == 12:
				return S物理地址(int(v字符串, 16))
			else:
				raise ValueError()
		raise TypeError()
	def __str__(self):
		return self.fg字符串()
	def fg字符串(self, a分隔符 = "", a分隔位数 = 4):
		v字符串 = hex(self.m值)[2:]	#去掉0x
		v长度 = len(v字符串)
		if v长度 < 12:
			v字符串 = "0" * (12 - v长度) + v字符串
		if a分隔符:
			return 字符串.f隔段插入字符串(v字符串, a分隔符, a分隔位数)
		else:
			return v字符串
#===============================================================================
# 连续地址类
#===============================================================================
class C连续地址4:
	def __init__(self, *a地址):
		if '-' in a地址[0]:
			v地址 = a地址[0].split('-')
			self.m地址0 = ipaddress.IPv4Address(v地址[0])
			self.m地址1 = ipaddress.IPv4Address(f补全地址(v地址[0], v地址[1]))
		elif len(a地址) == 2:
			self.m地址0 = ipaddress.IPv4Address(a地址[0])
			self.m地址1 = ipaddress.IPv4Address(a地址[1])
		else:
			raise ValueError()
	def __iter__(self):
		self.m迭代计数 = int(self.m地址0)
		self.m迭代结束 = int(self.m地址1)
		return self
	def __next__(self):
		if self.m迭代计数 <= self.m迭代结束:
			v地址 = ipaddress.IPv4Address(self.m迭代计数)
			self.m迭代计数 += 1
			return v地址
		else:
			raise StopIteration()
#===============================================================================
# 其他
#===============================================================================
#类型别名
Cip地址 = S网络地址4
Cipv6地址 = S网络地址6
Cmac地址 = S物理地址