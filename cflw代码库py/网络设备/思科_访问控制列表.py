import functools
import ipaddress
import cflw网络设备 as 设备
import cflw网络地址 as 地址
import cflw字符串 as 字符串
from . import 通用_访问控制列表 as 通用
c不 = "no"
c允许 = "permit"
c拒绝 = "deny"
c允许元组 = (c允许, c拒绝)
#===============================================================================
# 生成&解析
#===============================================================================
class C端口号到字符串(设备.I访问控制列表端口号到字符串):
	def f大于(self, a值):
		return "gt " + str(a值)
	def f小于(self, a值):
		return "lt " + str(a值)
	def f等于(self, a序列):
		return "eq " + " ".join(字符串.ft字符串序列(a序列))
	def f不等于(self, a序列):
		return "neq " + " ".join(字符串.ft字符串序列(a序列))
	def f范围(self, a值: range):
		return "range %d %d" % (a值.start, a值.stop - 1)
g端口号到字符串 = C端口号到字符串()
def f生成规则序号4(a序号):
	if a序号 == None or a序号 < 0:
		return ""
	else:
		return a序号
def f生成规则序号6(a序号):
	if a序号 == None or a序号 < 0:
		return ""
	else:
		return "sequence " + str(a序号)
f生成允许 = functools.partial(通用.f生成允许, c允许元组)
def f生成地址4(a地址):
	"转成字符串"
	v地址 = a地址
	v类型 = type(v地址)
	if v类型 == 地址.S网络地址4:
		return "%s %s" % (v地址.fg网络号s(), v地址.fg掩码s())
	elif v类型 == ipaddress.IPv4Address:
		return "host %s" % (v地址,)
	elif v类型 == ipaddress.IPv4Network:
		return "%s %s" % (v地址.network_address, v地址.hostmask)
	elif v类型 == str:
		return v地址
	elif a地址 == None:
		return "any"
	else:
		raise TypeError("无法生成的类型")
def f生成地址6(a地址):
	v地址 = a地址
	v类型 = type(v地址)
	if v类型 == 地址.S网络地址6:
		return "%s %s" % (v地址.fg地址s(), v地址.fg前缀长度())
	elif v类型 == ipaddress.IPv6Address:
		return "host %s" % (v地址,)
	elif v类型 == ipaddress.IPv6Network:
		return "%s %s" % (v地址.network_address, v地址.hostmask)
	elif v类型 == str:
		return v地址
	elif a地址 == None:
		return "any"
	else:
		raise TypeError("无法生成的类型")
f生成端口 = functools.partial(通用.f生成端口, g端口号到字符串)
def f解析允许(a允许: str):
	if a允许 == c允许:
		return True
	elif a允许 == c拒绝:
		return False
	else:
		raise ValueError()
def f解析地址(a地址: str, a通配符: str):
	if a地址 == "any":
		return None
	v地址 = 地址.S网络地址4.fc地址字符串(a地址)
	if a通配符:
		v地址.m前缀长度 = 地址.S网络地址4.f掩码字符串转前缀长度(a通配符)
	return v地址
#===============================================================================
# 类
#===============================================================================
class I访问控制列表(设备.I访问控制列表):
	def __init__(self, a, m名称, a类型 = "", a协议 = "ip"):
		设备.I访问控制列表.__init__(self, a)
		self.m名称 = m名称
		self.m类型 = a类型
		self.m协议 = a协议
	def fg模式参数(self):
		return (self.m类型, self.m名称)
	def fg进入命令(self):
		return "%s access-list %s %s" % (self.m协议, self.m类型, self.m名称)
	def fg显示命令(self):
		return "show ip access-list %s" % (self.m名称,)
	def f删除规则(self, a序号: int):
		self.f执行当前模式命令(c不 + str(a序号))
	def fe规则0(self, af解析):
		v输出 = self.f执行显示命令(self.fg显示命令())
		for v in v输出[1:]:
			yield af解析(v)
class C标准4(I访问控制列表):
	def __init__(self, a, a名字):
		I访问控制列表.__init__(self, a, a名字, a类型 = "standard")
	def f添加规则(self, a序号 = -1, a规则 = 设备.C访问控制列表规则(a允许 = False)):
		v序号 = f生成规则序号4(a序号)
		v允许 = f生成允许(a规则.m允许)
		v源地址 = f生成地址4(a规则.m源地址)
		v命令 = "%s %s %s" % (v序号, v允许, v源地址)
		self.f执行当前模式命令(v命令)
	def fe规则(self):
		return self.fe规则0(C标准4.f解析规则)
	@staticmethod
	def f解析规则(a规则: str):
		va词 = a规则.split()
		i = 0
		v规则 = 设备.C访问控制列表规则()
		if str.isdigit(va词[i]): #规则序号
			v规则.m序号 = int(va词[i])
			i += 1
		#允许
		v规则.m允许 = f解析允许(va词[i])
		i += 1
		#地址
		v地址 = va词[i]
		v通配符 = "" if i+1 == len(va词) else va词[i+1]
		v规则.m源地址 = f解析地址(v地址, v通配符)
		return v规则
class C扩展4(I访问控制列表):
	def __init__(self, a, a名字):
		I访问控制列表.__init__(self, a, a名字, a类型 = "extended")
	def f添加规则(self, a序号 = -1, a规则 = 设备.C访问控制列表规则(a允许 = False)):
		v命令 = 设备.C命令()
		v命令 += f生成规则序号4(a序号)
		v命令 += f生成允许(a规则.m允许)
		#确定
		if a规则.m协议 == 设备.C访问控制列表规则.E协议.ipv4:
			v命令 += "ip"
			v层 = 3
		elif a规则.m协议 == 设备.C访问控制列表规则.E协议.tcp:
			v命令 += "tcp"
			v层 = 4
		elif a规则.m协议 == 设备.C访问控制列表规则.E协议.udp:
			v命令 += "udp"
			v层 = 4
		else:
			raise ValueError("无法识别的协议")
		#按层
		if v层 == 3:
			v命令 += f生成地址4(a规则.m源地址)
			v命令 += f生成地址4(a规则.m目的地址)
		elif v层 == 4:
			v命令 += f生成地址4(a规则.m源地址)
			v命令 += f生成端口(a规则.m源端口)
			v命令 += f生成地址4(a规则.m目的地址)
			v命令 += f生成端口(a规则.m目的端口)
		else:
			raise NotImplementedError("迷之逻辑")
		#执行命令
		self.f执行当前模式命令(v命令)
	def fe规则(self):
		return self.fe规则0(C扩展4.f解析规则)
	@staticmethod
	def f解析规则(a规则: str):
		pass
class C六(I访问控制列表):
	def __init__(self, a, a名字):
		I访问控制列表.__init__(self, a, a名字, a协议 = "ipv6")
	def f添加规则(self, a序号 = -1, a规则 = 设备.C访问控制列表规则(a允许 = False)):
		v序号 = f生成规则序号6(a序号)
		v允许 = f生成允许(a规则.m允许)
		v源地址 = f生成地址6(a规则.m源地址)
		v命令 = "%s %s %s" % (v序号, v允许, v源地址)
		self.f执行当前模式命令(v命令)
	def f删除规则(self, a序号):
		self.f执行当前模式命令(c不 + str(v序号))
class C助手(设备.I访问控制列表助手):
	def F计算(a0, a1):
		@staticmethod
		def f(n):
			v类型 = type(n)
			if v类型 == int:
				if n in range(a0[0], a0[1]):
					return n + a0[2]
				elif n in range(a1[0], a1[1]):
					return n + a1[2]
				else:
					raise ValueError("n超出范围")
			else:
				return n
		return f
	f计算序号_标准4 = F计算((0, 99, 1), (100, 799, 1200))
	f计算序号_扩展4 = F计算((0, 99, 100), (100, 799, 1900))
	f反算序号_标准4 = F计算((1, 100, -1), (1301, 2000, -1200))
	f反算序号_扩展4 = F计算((100, 200, -100), (2000, 2700, -1900))
