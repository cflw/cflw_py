import ipaddress
import hashlib
import struct
import enum
import time
import cflw网络地址 as 地址
import cflw网络连接 as 连接
import cflw网络设备 as 设备
import cflw字符串 as 字符串
from 网络设备 import 华为_访问控制列表 as 访问控制列表
c不 = "undo "
c结束符 = '\x1a'	#ctrl+z
#===============================================================================
# 工厂
#===============================================================================
class E型号(enum.IntEnum):
	s3700 = 23700
	s3928 = 23928
	s5700 = 25700
	s7700 = 27700
	ar201 = 30201
	ar1220 = 31220
	ar2220 = 32220
	ar3620 = 33620
def f创建设备(a连接, a型号 = 0, a版本 = 0):
	return C设备(a连接)
#===============================================================================
# 设备
#===============================================================================
class C设备(设备.I设备):
	def __init__(self, a连接):
		设备.I设备.__init__(self)
		if isinstance(a连接, 连接.I连接):
			self.m连接 = a连接
			self.m连接.fs编码("gb2312")
		else:
			raise TypeError("a连接 必须是 I连接 类型")
		self.f检测命令异常 = 设备.F检测命令异常(ca错误文本与异常类)
	def f退出(self):
		self.f执行命令("quit")
	def f输入_结束符(self):
		self.f输入(c结束符 + "\r")
	def f模式_用户(self):
		self.f刷新()
		self.f输入_结束符()
		self.f输入_回车()
		if not self.ma模式:
			self.ma模式.append(C用户视图(self))
		return self.ma模式[0]
	def f执行命令(self, a命令):
		v输出 = 设备.I设备.f执行命令(self, a命令)
		self.f检测命令异常(self, v输出)
		return v输出
	def f执行显示命令(self, a命令, a自动换页 = False):
		v命令 = str(a命令)
		v输出 = 设备.I设备.f执行显示命令(self, v命令, a自动换页)
		v输出 = 设备.C实用工具.f去头尾行(v输出)
		if v输出.count("\n") < 10:
			self.f检测命令异常(self, v输出)
		return v输出
	def f显示_当前模式配置(self):
		v输出 = self.f执行显示命令("display this", a自动换页 = True)
		v输出 = 设备.C实用工具.f去头尾行(v输出)
		return v输出
ca错误文本与异常类 = [
	("Error: Wrong parameter found at '^' position.", 设备.X命令)
]
#===============================================================================
# 用户视图
#===============================================================================
class C用户视图(设备.I用户模式):
	def __init__(self, a):
		设备.I用户模式.__init__(self, a)
	#模式
	def f模式_全局配置(self):
		return C系统视图(self)
	#显示
	def f显示_版本(self):
		v命令 = "display version"
		v输出 = self.m设备.f执行显示命令(v命令, a自动换页 = True)
		return v输出
	def f显示_启动配置(self):
		v命令 = "display saved-configuration"
		v输出 = self.m设备.f执行显示命令(v命令, a自动换页 = True)
		return C配置内容(v输出)
	def f显示_当前配置(self):
		v命令 = "display current-configuration"
		v输出 = self.m设备.f执行显示命令(v命令, a自动换页 = True)
		return C配置内容(v输出)
	def f显示_时间(self):
		v命令 = "display clock"
		v输出 = self.m设备.f执行显示命令(v命令)
		#2017-02-19 14:09:32
		#Sunday
		#Time Zone(China-Standard-Time) : UTC-08:00

	def f显示_设备名称(self):
		v命令 = "display current-configuration | include sysname"
		v输出 = self.m设备.f执行显示命令(v命令, a等待 = 5)
		return C输出分析.f从配置取设备名称(v输出)
	def f显示_物理地址表(self):
		v命令 = "display mac-address"
		v输出 = self.m设备.f执行显示命令(v命令, a等待 = 5)
	def f显示_地址转换表(self):
		v命令 = "display arp"
		v输出 = self.m设备.f执行显示命令(v命令, a等待 = 5)
	def f显示_运行时间(self):
		"从开机到现在所经过的时间"
		raise NotImplementedError()
	def f显示_开机日期(self):
		raise NotImplementedError()
	def f显示_序列号(self):
		raise NotImplementedError()
	def f显示_出厂日期(self):
		raise NotImplementedError()
#===============================================================================
# 信息
#===============================================================================
class C板属性:
	def __init__(self, a):
		self.m字符串 = 字符串.f提取字符串之间(a, "[Board Properties]\n", "\n\n")
	def fg板类型(self):
		v字符串 = 字符串.f提取字符串之间(self.m字符串, "BoardType=", "\n")
		return v字符串
	def fg板代码(self):
		v字符串 = 字符串.f提取字符串之间(self.m字符串, "BarCode=", "\n")
		return v字符串
	def fg项目(self):
		v字符串 = 字符串.f提取字符串之间(self.m字符串, "Item=", "\n")
		return v字符串
	def fg描述(self):
		v字符串 = 字符串.f提取字符串之间(self.m字符串, "Description=", "\n")
		v长度 = len(v字符串)
		try:
			if v长度 == 10:	#YYYY-MM-DD
				v日期 = time.strptime("%Y-%m-%d")
			elif v长度 == 8:	#YY-MM-DD
				v日期 = time.strptime("%y-%m-%d")
			else:
				return v字符串
			return v日期
		except:
			return v字符串
	def fg生产日期(self):
		v字符串 = 字符串.f提取字符串之间(self.m字符串, "Manufactured=", "\n")
	def fg厂商名(self):
		v字符串 = 字符串.f提取字符串之间(self.m字符串, "VendorName=", "\n")
		return v字符串
class C电子标签信息s3700:	#display elabel
	def __init__(self, a):
		self.m主板 = C板属性(a)
	def fg序列号(self):
		return self.m主板.fg板代码()
#===============================================================================
# 系统视图
#===============================================================================
g接口名称字典 = 设备.fc接口名称字典({})
f创建接口 = 设备.F创建接口(g接口名称字典)
class C系统视图(设备.I全局配置模式):
	def __init__(self, a):
		设备.I全局配置模式.__init__(self, a)
	def fg进入命令(self):
		return "system-view"
	#模式
	def f模式_接口配置(self, a接口):
		v接口 = f创建接口(a接口)
		#检查值
		if v接口.fi属于分类(设备.E接口分类.e以太网):
			if v接口.fg主序号数() != 3:
				raise ValueError("在华为设备,接口序号有3段")
			elif v接口.fi范围():
				return C端口组(self, v接口)
		if v接口.fi属于分类(设备.E接口分类.e环回):
			if v接口.fg主序号数() != 1:
				raise ValueError("环回口的序号只有1段")
		return C接口视图(self, v接口)
	#路由
	def f模式_开放最短路径优先(self, a进程号, a版本 = 设备.E版本.e开放最短路径优先2):
		return Cospf(self, a进程号)
	#其它
	def f模式_访问控制列表(self, a名称, a类型):
		if a类型 == 设备.E访问控制列表类型.ipv4标准:
			return 访问控制列表.C基本4(self, a名称)
		elif a类型 == 设备.E访问控制列表类型.ipv4扩展:
			return 访问控制列表.C高级4(self, a名称)
		elif a类型 == 设备.E访问控制列表类型.ipv6:
			return 访问控制列表.C高级6(self, a名称)
		else:
			raise ValueError("错误的类型")
	def f助手_访问控制列表(self):
		return 访问控制列表.C助手()
	#配置
	def fs设备名(self, a名称):
		self.f执行当前模式命令("sysname " + str(a名称))
#===============================================================================
# 接口
#===============================================================================
class C接口视图(设备.I接口配置模式):
	def __init__(self, a, a接口):
		设备.I接口配置模式.__init__(self, a, a接口)
	@staticmethod
	def f解析参数_网络地址(a地址, a次地址):
		v地址 = 地址.C因特网协议4.fc接口(a地址)
		v分割 = v地址.with_prefixlen.split('/')
		if a次地址:
			v次地址 = 'sub'
		else:
			v次地址 = ''
		return '%s %s %s' % (*v分割, v次地址)
	@staticmethod
	def f解析参数_虚拟局域网(a虚拟局域网):
		if type(a虚拟局域网) == range:
			return '%d to %d' % (a虚拟局域网.start, a虚拟局域网.stop - 1)
		else:
			return str(a虚拟局域网)
	@staticmethod
	def f解析参数_端口安全动作(a动作):
		v类型 = type(a动作)
		if v类型 == str:
			return a动作
		elif v类型 == int:
			return ("shutdown", "restrict", "protect")[a动作]
		elif v类型 == bool:
			if a动作:
				return "restrict"
			else:
				return "shutdown"
		return "restrict"
	#接口操作
	def f开关(self, a开关):
		self.f切换到当前模式()
		if a开关:
			self.m设备.f执行命令("undo shutdown")
		else:
			self.m设备.f执行命令("shutdown")
	def fs网络地址(self, a地址, a次地址 = False):
		"设置地址"
		self.f切换到当前模式()
		self.m设备.f执行命令("ip address " + C接口视图.f解析参数_网络地址(a地址, a次地址))
	#二层
	def f二层中继_允许通过(self, a虚拟局域网):
		self.m设备.f执行命令("port trunk allow-pass vlan " + C接口视图.f解析参数_虚拟局域网(a虚拟局域网))
	#端口安全
	def f端口安全_开关(self, a开关):
		if a开关:
			self.m设备.f执行命令("port-security enable")
		else:
			self.m设备.f执行命令("undo port-security enable")
	def f端口安全_s数量(self, a数量):
		v命令 = "port-security max-mac-num " + int(a数量)
		self.m设备.f执行命令(v命令)
	def f端口安全_s动作(self, a动作):
		v命令 = "port-security protect-action " + C接口视图.f解析参数_端口安全动作(a动作)
		self.m设备.f执行命令(v命令)
class C端口组(C接口视图):
	def __init__(self, a, a接口: 设备.S接口):
		C接口视图.__init__(self, a, a接口)
		#计算哈希
		v范围 = a接口.m序号[2]
		v字节 = struct.pack('iiiii', a接口.m名称, a接口.m序号[0], a接口.m序号[1], v范围.start, v范围.stop)
		v校验 = hashlib.md5()
		v校验.update(v字节)
		self.m哈希 = v校验.hexdigest()
	def fg模式参数(self):	#在这里确定不同厂商的接口名称
		return self.m哈希
	def fg进入命令(self):
		return 'port-group ' + self.fg模式参数()
	def f切换到当前模式(self):
		C接口视图.f切换到当前模式(self)
		#是否绑定端口,没有则绑定
#===============================================================================
# 用户配置
#===============================================================================
class C用户配置(设备.I用户配置模式):
	def __init__(self, a, a用户名):
		设备.I用户配置模式.__init__(self, a, a用户名)
	def fs密码(self, a密码, a加密等级):
		v加密等级 = C实用工具.f加密等级(a加密等级)
		v命令 = 'username %s password %s %s' % (self.m用户名, v加密等级, a密码)
		self.m设备.f执行命令(v命令)
#===============================================================================
# 静态路由
#===============================================================================
class C静态路由(设备.C同级模式, 设备.I静态路由配置模式):
	def __init__(self, a):
		设备.I静态路由配置模式.__init__(self, a)
	@staticmethod
	def f解析参数(a网络号, a出接口):
		v网络号 = 地址.C因特网协议4.fc网络(a网络号, False)
		v分割 = v网络号.with_netmask.split('/')
		v接口 = C实用工具.f接口字符串(a出接口)
		s = '%s %s %s' % (*v分割, v接口)
		return s
	def f添加路由(self, a网络号, a出接口):
		self.m设备.f执行命令('ip route-static ' + C静态路由.f解析参数(a网络号, a出接口))
	def f删除路由(self, a网络号, a出接口):
		self.m设备.f执行命令('undo ip route-static ' + C静态路由.f解析参数(a网络号, a出接口))
#===============================================================================
# 开放最短路径优先
#===============================================================================
class Cospf(设备.I开放最短路径优先):
	def __init__(self, a, a进程号):
		设备.I开放最短路径优先.__init__(self, a, a进程号)
		self.m区域表 = {}
		self.m路由器号 = None
	def fg模式参数(self):
		v命令 = 设备.C命令(self.m进程号)
		if self.m路由器号:
			v命令 += "router-id"
			v命令 += self.m路由器号
		return v命令
	def fg进入命令(self):
		return 设备.C命令("ospf") + self.fg模式参数()
	def f模式_区域(self, a):
		v区域 = Cospf.f计算区域号(a)
		if not v区域 in self.m区域表:
			self.m区域表[v区域] = Cospf区域(self, v区域)
		return self.m区域表[v区域]
	@staticmethod
	def f计算区域号(a区域)->int:
		v类型 = type(a区域)
		if v类型 == int:
			return a区域
		elif v类型 == ipaddress.IPv4Address:
			return int(a区域)
		elif v类型 == str:
			if a区域.count('.') == 3:	#是ia地址格式
				return int(ipaddress.IPv4Address(a区域))
			else:
				return int(a区域)
		else:	#无法识别
			raise ValueError()
	#显示
	def f显示_路由表(self):
		return self.m设备.f执行显示命令("display ip routing-table protocol ospf")
	#操作
	def fs路由器号(self, a):
		self.m路由器号 = a
	def f通告网络(self, a网络号, a区域):
		v区域 = self.f模式_区域(a区域)
		v区域.f通告网络(a网络号)
	def f删除网络(self, a网络号, a区域):
		v区域 = self.f模式_区域(a区域)
		v区域.f删除网络(a网络号)
	def f通告接口(self, a接口, a区域):
		Cospf接口.f执行通告接口命令(a接口, True, self.m进程号, a区域)
	def f删除接口(self, a接口, a区域):
		Cospf接口.f执行通告接口命令(a接口, False, self.m进程号, a区域)
class Cospf区域(设备.I模式):
	def __init__(self, a, a区域号):
		设备.I模式.__init__(self, a)
		self.m区域 = int(a区域号)
	def fg模式参数(self):
		return str(self.m区域)
	def fg进入命令(self):
		return "area " + self.fg模式参数()
	def fg进程号(self):
		return self.fg上级模式().m进程号
	@staticmethod
	def f生成通告网络命令(a网络号):
		v地址 = ipaddress.IPv4Network(a网络号, False)
		v分割 = 地址.C因特网协议4.f分割地址反掩码(v地址)
		return "network %s %s" % v分割
	def f通告网络(self, a网络号):
		v命令 = Cospf区域.f生成通告网络命令(a网络号)
		self.f执行当前模式命令(v命令)
	def f删除网络(self, a网络号):
		v命令 = c不 + Cospf区域.f生成通告网络命令(a网络号, self.m区域)
		self.f执行当前模式命令(v命令)
	def f通告接口(self, a接口):
		Cospf接口.f执行通告接口命令(a接口, True, self.fg进程号(), self.m区域)
	def f删除接口(self, a接口):
		Cospf接口.f执行通告接口命令(a接口, False, self.fg进程号(), self.m区域)
class Cospf接口(设备.I开放最短路径优先接口):
	def __init__(self, a, a接口):
		设备.I开放最短路径优先接口.__init__(self, a, a接口)
	@staticmethod
	def f生成通告接口命令(a进程号, a区域):
		v命令 = 设备.C命令("ospf enable")
		v命令 += a进程号
		v命令 += "area " + str(a区域)
		return v命令
	@staticmethod
	def f执行通告接口命令(a接口, a肯定, a进程号, a区域):
		v命令 = Cospf接口.f生成通告接口命令(a进程号, a区域)
		v命令.f前置否定(a肯定, c不)
		a接口.f执行当前模式命令(v命令)
	def f通告接口(self, a进程号, a区域):
		f执行通告接口命令(self, True, a进程号, a区域)
	def f删除接口(self, a进程号, a区域):
		f执行通告接口命令(self, False, a进程号, a区域)
#===============================================================================
# telnet
#===============================================================================
class Ctelnet(设备.I远端登入, 设备.C同级模式):
	def __init__(self, a):
		设备.I远端登入.__init__(self, a)
	def fs端口号(self, a):
		v命令 = 设备.C命令("telnet server port")
		v命令 += a
		self.f执行当前模式命令(v命令)
	def f开关(self, a):
		v命令 = 设备.C命令("telnet server enable")
		v命令.f前置否定(a, c不)
		self.f执行当前模式命令(v命令)
#===============================================================================
# 工具
#===============================================================================
class C实用工具:
	@staticmethod
	def f加密等级(a):
		if type(a) == str:
			v补全 = 设备.C实用工具.f命令补全(a, 'cipher', 'simple')
			if v补全:
				return v补全
		if 设备.C实用工具.f参数等级(a加密等级, 1):
			return 'cipher'
		else:
			return 'simple'
class C配置内容:
	def __init__(self, a配置):
		self.m配置 = a配置.replace('\r', '')
	def __str__(self):
		return self.m配置
	def fg设备名称(self):
		return C输出分析.f从配置取设备名称(self.m配置)
class C输出分析:
	@staticmethod
	def f从配置取设备名称(a配置):
		v指定行 = a配置.find(' sysname ')
		v结束 = a配置.find('\n', v指定行)
		if v结束 == -1:
			return a配置[v指定行 + 8 :]
		else:
			return a配置[v指定行 + 8 : v结束]