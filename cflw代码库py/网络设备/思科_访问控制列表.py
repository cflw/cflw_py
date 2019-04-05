import functools
import ipaddress
import cflw网络设备 as 设备
import cflw网络地址 as 地址
import cflw字符串 as 字符串
import 网络设备.通用_实用 as 通用实用
import 网络设备.通用_访问控制列表 as 通用访问列表
from 网络设备.思科_常量 import *
c允许 = "permit"
c拒绝 = "deny"
c允许元组 = (c允许, c拒绝)
#===============================================================================
# 生成&解析
#===============================================================================
#访问控制列表序号范围
ca标准范围 = (range(1, 100), range(1300, 2000))
ca扩展范围 = (range(100, 200), range(2000, 2700))
class F序号范围检查:
	def __init__(self, aa范围, a异常文本):
		self.ma范围 = aa范围
		self.m异常文本 = a异常文本
	def __call__(self, a序号, a异常 = True):
		if type(a序号) == int:
			for v in aa范围:
				if a序号 in v:
					return True
			if a异常:
				raise ValueError(a错误文本)
			return False
		return False
fi标准范围 = F序号范围检查(ca标准范围, "标准访问控制列表号码范围应为1~99,1300~1999")
fi扩展范围 = F序号范围检查(ca扩展范围, "扩展访问控制列表号码范围应为100~199,2000~2699")
#端口号
class C端口号到字符串(设备.I端口号到字符串):
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
f生成端口 = functools.partial(通用访问列表.f生成端口, g端口号到字符串)
#规则序号
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
#允许
f生成允许 = functools.partial(通用访问列表.f生成允许, c允许元组)
def f解析允许(a允许: str):
	if a允许 == c允许:
		return True
	elif a允许 == c拒绝:
		return False
	else:
		raise ValueError()
#地址
def f生成地址4(a地址):
	"转成字符串"
	v地址 = 地址.S网络地址4.fc自动(a地址)
	if v地址.fi主机掩码():
		return "host %s" % (v地址.fg地址s())
	elif v地址.fi空掩码():
		return "any"
	else:
		return "%s %s" % (v地址.fg网络号s(), v地址.fg反掩码s())
def f生成地址6(a地址):
	v地址 = 地址.S网络地址6.fc自动(a地址)
	if v地址.fi主机掩码():
		return "host %s" % (v地址.fg地址s())
	elif v地址.fi空掩码():
		return "any"
	else:
		return "%s %s" % (v地址.fg网络号s(), v地址.fg前缀长度())
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
	def __init__(self, a, a名称, a类型: str = "", a协议: str = "ip"):
		设备.I访问控制列表.__init__(self, a)
		self.m名称 = a名称
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
	def fs规则(self, a序号 = 通用访问列表.c空序号, a规则 = 通用访问列表.c空规则, a操作 = 设备.E操作.e添加):
		v操作 = 通用实用.f解析操作(a操作)
		if 通用实用.fi加操作(v操作):
			self.f添加规则(a序号, a规则)
		elif 通用实用.fi减操作(v操作):
			self.f删除规则(a序号)
	def fe规则0(self, af解析):
		v输出 = self.f执行显示命令(self.fg显示命令())
		for v in v输出[1:]:
			yield af解析(v)
	def fe规则(self):
		return self.fe规则0(self.f解析规则)
class C标准4(I访问控制列表):
	def __init__(self, a, a名称):
		I访问控制列表.__init__(self, a, a名称, a类型 = "standard")
	def f添加规则(self, a序号, a规则):
		v序号 = f生成规则序号4(a序号)
		v允许 = f生成允许(a规则.m允许)
		v源地址 = f生成地址4(a规则.m源地址)
		v命令 = "%s %s %s" % (v序号, v允许, v源地址)
		self.f执行当前模式命令(v命令)
	@staticmethod
	def f解析规则(a规则: str):
		va词 = a规则.split()
		i = 0
		v规则 = 设备.S访问控制列表规则()
		if va词[i].isdigit(): #规则序号
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
	def __init__(self, a, a名称):
		I访问控制列表.__init__(self, a, a名称, a类型 = "extended")
	def f添加规则(self, a序号, a规则):
		v命令 = 设备.C命令()
		v命令 += f生成规则序号4(a序号)
		v命令 += f生成允许(a规则.m允许)
		#确定
		if a规则.m协议 == 设备.E协议.ipv4:
			v命令 += "ip"
			v层 = 3
		elif a规则.m协议 == 设备.E协议.tcp:
			v命令 += "tcp"
			v层 = 4
		elif a规则.m协议 == 设备.E协议.udp:
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
	@staticmethod
	def f解析规则(a规则: str):
		raise NotImplementedError()
class C六(I访问控制列表):
	def __init__(self, a, a名字):
		I访问控制列表.__init__(self, a, a名字, a协议 = "ipv6")
	def f添加规则(self, a序号, a规则):
		v序号 = f生成规则序号6(a序号)
		v允许 = f生成允许(a规则.m允许)
		v源地址 = f生成地址6(a规则.m源地址)
		v命令 = "%s %s %s" % (v序号, v允许, v源地址)
		self.f执行当前模式命令(v命令)
	def f删除规则(self, a序号):
		self.f执行当前模式命令(c不 + str(v序号))
	@staticmethod
	def f解析规则(a规则: str):
		raise NotImplementedError()
class C助手(设备.I访问控制列表助手):
	#元组结构含意:(序号开始, 序号结束, 到目标序号的增加值)
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
	f计算标准4 = F计算((0, 99, 1), (100, 799, 1200))
	f计算扩展4 = F计算((0, 99, 100), (100, 799, 1900))
	f反算标准4 = F计算((1, 100, -1), (1301, 2000, -1200))
	f反算扩展4 = F计算((100, 200, -100), (2000, 2700, -1900))
	@staticmethod
	def ft特定序号(n, a类型):
		if a类型 == 设备.E访问控制列表类型.e标准4:
			return C助手.f计算标准4(n)
		elif a类型 == 设备.E访问控制列表类型.e扩展4:
			return C助手.f计算扩展4(n)
		else:
			raise ValueError("类型错")
	@staticmethod
	def ft统一序号(n, a类型):
		if a类型 == 设备.E访问控制列表类型.e标准4:
			return C助手.f反算标准4(n)
		elif a类型 == 设备.E访问控制列表类型.e扩展4:
			return C助手.f反算扩展4(n)
		else:
			raise ValueError("类型错")