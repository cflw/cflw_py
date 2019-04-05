import functools
import cflw网络设备 as 设备
import 网络设备.通用_访问控制列表 as 通用访问列表
import 网络设备.通用_实用 as 通用实用
c不 = "undo"
c允许 = "permit"
c拒绝 = "deny"
c允许元组 = (c允许, c拒绝)
c源地址 = "source"
c源端口 = "source-port"
c目的地址 = "destination"
c目的端口 = "destination-port"
#生成
def f生成规则序号(a序号):
	v命令 = 设备.C命令("rule")
	if a序号:
		v命令 += a序号
	return v命令
f生成协议4 = 通用访问列表.f生成协议4
f生成允许 = functools.partial(通用访问列表.f生成允许, c允许元组)
def f生成端口(a前置: str, a端口):
	return a前置 + " " + 通用访问列表.f生成端口(g到字符串, a端口)
def f生成地址(a前置: str, a地址):
	return a前置 + " " + 通用访问列表.f生成地址和通配符4(a地址)
#到字符串
class C到字符串(设备.I端口号到字符串):
	def f大于(self, a值):
		return "gt " + str(a值)
	def f小于(self, a值):
		return "lt " + str(a值)
	def f等于(self, a序列):
		return "eq %d" % (a序列[0], )
	def f范围(self, a值: range):
		return "range %d %d" % (a值.start, a值.stop - 1)
g到字符串 = C到字符串()
class I访问控制列表(设备.I访问控制列表):
	def __init__(self, a, m名称, a协议 = ""):
		设备.I访问控制列表.__init__(self, a)
		self.m名称 = m名称
		self.m协议 = a协议
	def fg模式参数(self):
		return (self.m类型, self.m名称)
	def fg进入命令(self):
		v命令 = 设备.C命令("acl")
		v命令 += self.m协议
		if type(self.m名称) == int:
			v命令 += "number %s" % (self.m名称,)
		else:
			v命令 += "name %s" % (self.m名称,)
		return v命令
	def fg显示命令(self):
		v命令 = 设备.C命令("diplay acl")
		v命令 += self.m协议
		if type(self.m名称) == int:
			v命令 += self.m名称
		else:
			v命令 += "name %s" % (self.m名称,)
		return v命令
	def f删除规则(self, a序号: int):
		v命令 = self.fg进入命令()
		v命令.f前面添加(c不)
		self.f执行当前模式命令(v命令)
	def fs规则(self, a序号 = None, a规则 = None, a操作 = 设备.E操作.e设置):
		v操作 = 通用实用.f解析操作(a操作)
		if 通用实用.fi加操作(v操作):
			self.f添加规则(a序号, a规则)
		elif 通用实用.fi减操作(v操作):
			self.f删除规则(a序号)
class C基本4(I访问控制列表):
	def __init__(self, a, a名称):
		I访问控制列表.__init__(self, a, a名称)
	def f添加规则(self, a序号 = None, a规则 = None):
		v命令 = f生成规则序号(a序号)
		v命令 += f生成允许(a规则.m允许)
		if a规则.m源地址:
			v命令 += f生成地址(c源地址, a规则.m源地址)
		self.f执行当前模式命令(v命令)
class C高级4(I访问控制列表):
	def __init__(self, a, a名称):
		I访问控制列表.__init__(self, a, a名称)
	def f添加规则(self, a序号 = None, a规则 = None):
		v命令 = f生成规则序号(a序号)
		v命令 += f生成允许(a规则.m允许)
		v命令 += f生成协议4(a规则.m协议)
		if a规则.m源地址:
			v命令 += f生成地址(c源地址, a规则.m源地址)
		if a规则.m源端口:
			v命令 += f生成端口(c源端口, a规则.m源端口)
		if a规则.m目的地址:
			v命令 += f生成地址(c目的地址, a规则.m目的地址)
		if a规则.m目的端口:
			v命令 += f生成端口(c目的端口, a规则.m目的端口)
		self.f执行当前模式命令(v命令)
class C基本6(I访问控制列表):
	def __init__(self, a, a名称):
		I访问控制列表.__init__(self, a, a名称, "ipv6")
class C高级6(I访问控制列表):
	def __init__(self, a, a名称):
		I访问控制列表.__init__(self, a, a名称, "ipv6")
class C助手(设备.I访问控制列表助手):
	def F计算(a起始):
		@staticmethod
		def f(n):
			return n + a起始
		return f
	def F反算(a起始):
		@staticmethod
		def f(n):
			return n - a起始
		return f
	f计算标准4 = F计算(2000)
	f计算扩展4 = F计算(3000)
	f反算标准4 = F反算(2000)
	f反算扩展4 = F反算(3000)
	@staticmethod
	def ft特定序号(n, a类型):
		if a类型 == 设备.E访问控制列表类型.e标准4:
			return C助手.f计算标准4(n)
		elif a类型 == 设备.E访问控制列表类型.e扩展4:
			return C助手.f计算扩展4(n)
		return n
	@staticmethod
	def ft统一序号(n, a类型):
		if a类型 == 设备.E访问控制列表类型.e标准4:
			return C助手.f反算标准4(n)
		elif a类型 == 设备.E访问控制列表类型.e扩展4:
			return C助手.f反算扩展4(n)
		return n