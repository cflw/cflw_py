import ipaddress
import time
import math
import enum
import datetime
import re
import cflw字符串 as 字符串
import cflw网络连接 as 连接
import cflw网络设备 as 设备
import cflw网络地址 as 地址
import cflw时间 as 时间
import cflw英语 as 英语
c不 = "no "
c做 = "do "
c结束符 = '\x03'	#ctrl+c
#==============================================================================
# 工厂
#==============================================================================
class E型号(enum.IntEnum):
	c2950 = 2950
	c2960 = 2960
	c3560 = 3560
	c7200 = 7200
def f创建设备(a连接: 连接.I连接, a型号: int = 0, a版本 = 0):
	return C设备(a连接)
#==============================================================================
# 设备
#==============================================================================
class C设备(设备.I设备):
	def __init__(self, a连接):
		设备.I设备.__init__(self)
		if isinstance(a连接, 连接.I连接):
			self.m连接 = a连接
			self.m连接.fs编码("ascii")
		else:
			raise TypeError("a连接 必须是 I连接 类型")
	def f退出(self):
		self.f执行命令("exit")
	def f输入_结束符(self):	#ctrl+c
		self.f输入(c结束符)
	def f模式_用户(self):
		self.f刷新(False)
		self.f输入_结束符()
		self.f输入_回车(-1, 2)
		if not self.ma模式:
			self.ma模式.append(C用户模式(self))
		return self.ma模式[0]
	def f执行命令(self, a命令):
		v输出 = 设备.I设备.f执行命令(self, a命令)
		C设备.f检测命令异常(v输出)
		return v输出
	def f执行用户命令(self, a命令):
		v命令 = str(a命令)
		if isinstance(self.ma模式[-1], C用户模式):
			v输出 = self.f执行命令(v命令)
		else:	#在配置模式，命令前要加个do
			v输出 = self.f执行命令(c做 + v命令)
		v输出 = v输出.replace("\r\n", "\n")
		return v输出
	def f执行显示命令(self, a命令):
		v命令 = str(a命令)
		#自动去头尾行
		if isinstance(self.ma模式[-1], C用户模式):
			v输出 = 设备.I设备.f执行显示命令(self, v命令)
		else:	#在配置模式，命令前要加个do
			v输出 = 设备.I设备.f执行显示命令(self, c做 + v命令)
		v输出 = v输出.replace("\r\n", "\n")
		v输出 = 设备.C实用工具.f去头尾行(v输出)
		if v输出.count("\n") < 10:	#输出行数太少,检测是否有异常
			C设备.f检测命令异常(v输出)
		return v输出
	@staticmethod
	def f检测命令异常(a输出, a抛出 = True):
		def f返回异常(ax):
			if type(ax) == type:
				v异常 = ax(a输出)
			else:
				v异常 = ax
			if a抛出:
				raise v异常
			return v异常
		if "% Invalid input detected at '^' marker." in a输出:	#语法错误
			return f返回异常(设备.X命令)
		elif "% Ambiguous command:" in a输出:	#不明确
			return f返回异常(设备.X命令)
		elif "% Duplicate sequence number" in a输出:	#acl规则序号冲突
			return f返回异常(设备.X执行)
		return None
#==============================================================================
# 用户模式
#==============================================================================
class C用户模式(设备.I用户模式):
	def __init__(self, a设备):
		设备.I用户模式.__init__(self, a设备)
		self.m版本信息 = None
		self.m版本信息时间 = 0
	def f切换到当前模式(self):
		self.m设备.f输入_结束符()
		self.m设备.ma模式 = self.m设备.ma模式[0:1]
	def f模式_全局配置(self):
		return C全局配置(self)
	#显示
	def f显示_启动配置(self):
		v输出 = self.m设备.f执行显示命令("show startup-config")
		return v输出
	def f显示_当前配置(self):
		v输出 = self.m设备.f执行显示命令("show running-config")
		return v输出
	def f显示_时间(self):
		#由于时区名可以设置成奇怪的名字,为了避免奇怪的问题,解析时过滤掉时区
		v输出 = self.m设备.f执行显示命令("show clock")	#*09:09:36.935 UTC Thu Sep 29 2016
		v空格位置 = 字符串.f全部搜索(v输出, " ")
		v行结束 = v输出.find("\n")
		if v行结束 > 0:	#如果有换行符,截取到行结束
			v输出 = v输出[0:v空格位置[0]] + v输出[v空格位置[1]:v行结束]
		else:	#如果没有换行符,截取到字符串结束
			v输出 = v输出[0:v空格位置[0]] + v输出[v空格位置[1]:]	#*09:09:36.935 Thu Sep 29 2016
		v时间 = time.strptime(v输出, "*%H:%M:%S.%f %a %b %d %Y")
		return v时间
	def f显示_设备版本(self):
		return self.fg版本信息()
	#操作
	def f登录(self, a用户名 = "", a密码 = ""):
		self.m设备.f执行命令(a用户名)
		self.m设备.f执行命令(a密码)
	def f提升权限(self, a密码 = ""):
		v输出 = self.m设备.f执行命令("enable")
		while "Password" in v输出:
			v输出 = self.m设备.f执行命令(a密码)
		if "Error" in v输出:
			raise X执行(v输出)
	#内部
	def fg版本信息(self):
		if time.time() - self.m版本信息时间 >= 60:	#超过1分种则刷新
			v输出 = self.m设备.f执行显示命令("show version")
			self.m版本信息 = C版本信息(v输出)
		return self.m版本信息
#==============================================================================
# 信息
#==============================================================================
class C版本信息(设备.I版本信息):
	def __init__(self, a):
		self.m字符串 = str(a)
	def fg版本s(self):
		return 字符串.f提取字符串之间(self.m字符串, "Version ", "\n", a包含开始 = True)
	def fg版本号(self):
		raise NotImplementedError()
	def fg编译日期(self):
		v字符串 = 字符串.f提取字符串之间(self.m字符串, "Compiled ", " by")
		v时间 = time.strptime(v字符串, "%a %d-%b-%y %H:%M")
		return v时间
	def fg运行时间(self):
		v字符串 = 字符串.f提取字符串之间(self.m字符串, "uptime is", "\n")
		v周 = 字符串.f提取字符串之间(v字符串, " ", " week", a反向查找 = True)
		v日 = 字符串.f提取字符串之间(v字符串, " ", " day", a反向查找 = True)
		v时 = 字符串.f提取字符串之间(v字符串, " ", " hour", a反向查找 = True)
		v分 = 字符串.f提取字符串之间(v字符串, " ", " minute", a反向查找 = True)
		return datetime.timedelta(weeks = int("0" + v周), days = int("0" + v日), hours = int("0" + v时), minutes = int("0" + v分))
	def fg开机日期(self):
		v字符串 = 字符串.f提取字符串之间(self.m字符串, "System restarted at ", "\n")
		if v字符串:	#找到时间,提取时间
			#14:22:27 beijing Sun Aug 21 2016
			v空格0 = v字符串.find(" ")
			v空格1 = v字符串.find(" ", v空格0 + 1)
			v字符串 = v字符串[:v空格0] + v字符串[v空格1:]
			v时间 = time.strptime(v字符串, "%H:%M:%S %a %b %d %Y")
			return v时间
		else:	#找不到时间,从本机时间减运行时间
			v运行时间 = self.fg运行时间()
			return time.localtime(time.time() - v运行时间.total_seconds())
	def fg序列号(self):
		return 字符串.f提取字符串之间(self.m字符串, "Processor board ID ", "\n")
	def fg版权(self):
		return 字符串.f提取字符串之间(self.m字符串, "Copyright ", "\n", a包含开始 = True)
	def fg物理地址(self):
		v地址 = 字符串.f提取字符串之间(self.m字符串, "Base ethernet MAC Address       : ", "\n")
		if v地址:
			return 地址.S物理地址.fc字符串(v地址)
		else:
			return None
ga物理地址类型 = {
	"STATIC": 设备.E物理地址类型.e静态,
	"DYNAMIC": 设备.E物理地址类型.e动态,
}
class C物理地址表:
	c虚拟局域网开始 = 0
	c物理地址开始 = 8
	c物理地址结束 = 22
	c类型开始 = 26
	c端口开始 = 38
	def __init__(self, a):
		self.m字符串 = str(a)
	def __iter__(self):
		return self.fe行()
	def fe行(self):	#把字符串转成数据
		for v行 in 字符串.fe分割(self.m字符串, '\n'):
			if "CPU" in v行:
				continue
			if not "." in v行:	#物理地址用.分隔
				continue
			v虚拟局域网s, v地址s, v类型s, v接口s = 字符串.fe按位置分割(v行, C物理地址表.c虚拟局域网开始, C物理地址表.c物理地址开始, C物理地址表.c类型开始, C物理地址表.c端口开始)
			v虚拟局域网 = int(v虚拟局域网s)
			v接口 = 设备.S接口.fc字符串(v接口s, ga接口缩写, False)
			v地址 = 地址.S物理地址.fc字符串(v地址s)
			v类型 = ga物理地址类型[str.strip(v类型s)]
			yield 设备.S物理地址项(a地址 = v地址, a接口 = v接口, a虚拟局域网 = v虚拟局域网, a类型 = v类型)
class C三层接口表:
	c接口开始 = 0
	c地址开始 = 23
	c好开始 = 39
	c方法开始 = 43
	c状态开始 = 50
	c协议开始 = 72
	def __init__(self, a):
		self.m字符串 = str(a)
	def __iter__(self):
		return self.fe行()
	def fe行(self):
		for v行 in 字符串.fe分割(self.m字符串, "\n"):
			if not "YES" in v行:
				continue
			#接口
			v接口 = 设备.S接口.fc字符串(v行[C三层接口表.c接口开始 : C三层接口表.c地址开始], ga接口名称)
			#地址
			v地址0 = v行[C三层接口表.c地址开始 : C三层接口表.c好开始]
			if "unassigned" in v地址0:
				v地址 = None
			else:
				v地址 = 地址.S网络地址4.fc地址前缀长度(v地址0, 32)
			#状态
			if "up" in v行[C三层接口表.c状态开始 : C三层接口表.c协议开始]:
				v状态 = True
			else:
				v状态 = False
			#退回
			yield 设备.S三层接口项(a接口 = v接口, a地址 = v地址, a状态 = v状态)
#==============================================================================
# 全局配置
#==============================================================================
class C全局配置(设备.I全局配置模式):
	c进入命令 = "configure terminal"
	def __init__(self, a父模式):
		设备.I全局配置模式.__init__(self, a父模式)
	#模式
	def f切换到当前模式(self):
		if self.fi当前模式():
			return
		if isinstanse(self.m设备.ma模式[-1], 设备.I用户模式):
			self.m设备.f执行命令(C全局配置.c进入命令)
		while len(self.m设备.ma模式) > 2:	#退出到第2层
			self.m设备.f退出()
		if not self.fi当前模式():
			self.m设备.f退出()
			self.m设备.f执行命令(C全局配置.c进入命令)
	def fg进入命令(self):
		return C全局配置.c进入命令
	#基本模式
	def f模式_接口配置(self, a接口):
		v接口 = f创建接口(a接口)
		return C接口配置(self, v接口)
	def f模式_用户配置(self, a):
		return C用户配置(self, a)
	def f模式_时间范围(self, a):
		return C时间范围(self, a)
	def f模式_访问控制列表(self, a名称, a类型 = 设备.E访问控制列表类型.e标准):
		v名称类型 = type(a名称)
		#创建访问控制列表对象
		if a类型 == 设备.E访问控制列表类型.ipv4标准:
			if v名称类型 == int:	#验证
				if a名称 in range(1, 100) or a名称 in range(1300, 2000):
					pass
				else:
					raise ValueError("标准访问控制列表号码范围应为1~99,1300~1999")
			return C标准访问控制列表(self, a名称)
		elif a类型 == 设备.E访问控制列表类型.ipv4扩展:
			if v名称类型 == int:	#验证
				if a名称 in range(100, 200) or a名称 in range(2000, 2700):
					pass
				else:
					raise ValueError("扩展访问控制列表号码范围应为100~199,2000~2699")
			return C扩展访问控制列表(self, a名称)
		elif a类型 == 设备.E访问控制列表类型.ipv6:
			return Cipv6访问控制列表(self, a名称)
		else:
			raise ValueError("未知的访问控制列表类型")
	#路由
	def f模式_路由信息协议(self, a进程号 = 0, a版本 = 设备.E版本.e路由信息协议):	#rip
		v版本 = 设备.C路由协议.f解析_版本(a版本)
		if v版本 == 设备.E版本.e路由信息协议:	#ripng
			return Crip(self)
		elif v版本 == 设备.E版本.e下一代路由信息协议:	#ripng
			v进程号 = str(a进程号)
			if not v进程号:
				raise ValueError("当版本为ripng时,必须指定进程号")
			return Cripng(self, a进程号)
		else:
			raise ValueError("未知的版本")
	def f模式_开放最短路径优先(self, a进程号, a版本 = 设备.E版本.e开放最短路径优先2):
		v版本 = 设备.C路由协议.f解析_版本(a版本)
		if a版本 == 设备.E版本.e开放最短路径优先2:
			return Cospf(self, a进程号)
		elif a版本 == 设备.E版本.e开放最短路径优先3:
			return Cospf(self, a进程号)
		else:
			raise ValueError("未知的版本")
	def f模式_增强内部网关路由协议(self, a, a版本 = 设备.E版本.e网络协议4):	#eigrp
		v类型 = type(a)
		if v类型 == int:
			return C经典eigrp(self, a)
	#服务
	def f模式_动态主机配置协议地址池(self, a名称):
		return Cdhca地址池(self, a名称)
	def f模式_动态主机配置协议(self):
		return Cdhcp(self)
	#助手
	def f助手_访问控制列表(self):
		return C助手_访问控制列表()
#==============================================================================
# 时间
#==============================================================================
class C时间(设备.C同级模式, 设备.I时间):
	def __init__(self, a):
		设备.I时间.__init__(self, a)
	def fs日期时间(self, a):
		v时间 = 设备.I时间.f解析日期时间(a)
		v时间文本 = time.strftime("%H:%M:%S %b %d %Y", v时间)
		v命令 = "clock set " + v时间文本
		self.m设备.f执行用户命令(v命令)
	def fs时区(self, *a):
		v时区 = 设备.I时间.f解析时区(a)
		v总秒 = v时区.utcoffset(None).total_seconds()
		if v总秒 < 0:
			v符号 = "-"
			v总秒 = -v总秒
		else:
			v符号 = "+"
		v时分秒 = 时间.C时间计算.f总秒拆成时分秒(v总秒)
		v命令 = "clock timezone %s %s%s " % (v时区.tzname(), v符号, v时分秒[0])
		if v时分秒[1] != 0:
			v命令 += str(v时分秒[1])
		self.f切换到当前模式()
		self.m设备.f执行命令(v命令)
#===============================================================================
# 用户配置
#===============================================================================
class C用户配置(设备.C同级模式, 设备.I用户配置模式):
	def __init__(self, a父模式, a用户名):
		#初始化
		设备.I用户配置模式.__init__(self, a父模式)
		self.m用户名 = str(a用户名)
		self.m命令前缀 = 'username ' + self.m用户名 + ' '
	def f执行用户命令(self, a命令):
		if not self.fi当前模式():
			raise self.m设备.f抛出模式异常()
		self.m设备.f执行命令(self.m命令前缀 + a命令)
	def fs密码(self, a密码, a加密级别 = 0):
		self.f切换到当前模式()
		self.f执行用户命令('password %d %s' % (a加密级别, a密码))
	def fs权限等级(self, a权限等级):
		self.f切换到当前模式()
		self.f执行用户命令('privildge ' + a权限等级)
	def fs服务类型(self, a服务类型 = None):
		pass
#===============================================================================
# 登陆
#===============================================================================
class C登陆配置(设备.I登陆配置模式):
	def __init__(self, a):
		设备.I登陆配置模式.__init__(self, a)
#===============================================================================
# 结构
#===============================================================================
ga日子 = {
	设备.E日子.e一: "monday",
	设备.E日子.e二: "tuesday",
	设备.E日子.e三: "wednesday",
	设备.E日子.e四: "thursday",
	设备.E日子.e五: "friday",
	设备.E日子.e六: "saturday",
	设备.E日子.e日: "sunday",
	设备.E日子.e工作日: "weekdays",
	设备.E日子.e周末: "weekend",
	设备.E日子.e每天: "daily",
}
class C时间范围(设备.I时间范围配置模式):
	def __init__(self, a, a名称):
		设备.I时间范围配置模式.__init__(self, a)
		self.m名称 = a名称
	@staticmethod
	def f解析命令(a时间范围):
		if a时间范围.m绝对:
			v命令 = 设备.C命令("absolute")
			def f绝对时间(a元组: tuple, a字符串: str):
				nonlocal v命令
				if a元组:
					v命令 += a字符串
					v命令 += "%s:%s %s %s %s" % (a元组[3], a元组[4], a元组[2], 英语.f月份(a元组[1])[:3], a元组[0])
			f绝对时间(a时间范围.m开始时间, "start")
			f绝对时间(a时间范围.m结束时间, "end")
		else:	#定期
			v命令 = 设备.C命令("periodic")
			v命令 += ga日子[a时间范围.m日子]
			def f定期时间(a元组: tuple):
				nonlocal v命令
				v命令 += "%s:%s" % (a元组[0], a元组[1])
			f定期时间(a时间范围.m开始时间)
			v命令 += "to"
			f定期时间(a时间范围.m结束时间)
		return v命令
	def fg进入命令(self):
		return "time-range " + self.m名称
	def f执行时间范围命令(self, ai: bool, a时间范围):
		v命令 = C时间范围.f解析命令(a时间范围)
		v命令.f前置否定(ai, c不)
		self.f执行当前模式命令(v命令)
	def f添加(self, a时间范围):
		self.f执行时间范围命令(True, a时间范围)
	def f删除(self, a时间范围):
		self.f执行时间范围命令(False, a时间范围)
#===============================================================================
# 接口配置
#===============================================================================
ga接口名称 = 设备.fc接口名称字典({})
f创建接口 = 设备.F创建接口(ga接口名称)
ga接口缩写 = {
	"Fa": 设备.E接口.e快速以太网,
	"Gi": 设备.E接口.e吉比特以太网
}
class C接口配置(设备.I接口配置模式):
	def __init__(self, a父模式, a接口):
		设备.I接口配置模式.__init__(self, a父模式, a接口)
	def fg模式参数(self):
		return str(self.m接口)
	@staticmethod
	def f网络地址参数(a地址, a次地址):
		v地址 = 地址.S网络地址4.fc自动(a地址)
		if a次地址:
			v次地址 = 'secondary'
		else:
			v次地址 = ''
		return '%s %s %s' % (v地址.fg地址s(), v地址.fg掩码s(), v次地址)
	#显示
	def f显示_当前模式配置(self):
		self.m设备.f执行用户命令('show running-config interface ' + self.fg模式参数())
	#操作
	def f开关(self, a开关):
		self.f切换到当前模式()
		if a开关:
			self.m设备.f执行命令('no shutdown')
		else:
			self.m设备.f执行命令('shutdown')
	def fs网络地址(self, a地址, a次地址 = False):
		'设置地址'
		v命令 = 'ip address ' + C接口配置.f网络地址参数(a地址, a次地址)
		self.f切换到当前模式()
		self.m设备.f执行命令(v命令)
	def fd网络地址(self, a地址 = None, a次地址 = False):
		'删除地址'
		if (bool(a地址) == False) and (bool(a次地址) == False):
			v命令 = 'no ip address'
		else:
			v命令 = 'no ip address ' + C接口配置.f网络地址参数(a地址, a次地址)
		self.f切换到当前模式()
		self.m设备.f执行命令(v命令)
	def fg网络地址(self):
		raise NotImplementedError()
#==============================================================================
# 路由
#==============================================================================
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
		self.m设备.f执行命令('ip route ' + C静态路由.f解析参数(a网络号, a出接口))
	def f删除路由(self, a网络号, a出接口):
		self.m设备.f执行命令('no ip route ' + C静态路由.f解析参数(a网络号, a出接口))
	def fs默认路由(self, a出接口):
		self.m设备.f执行命令('ip route ' + C静态路由.f解析参数('0.0.0.0/0', a出接口))
#==============================================================================
# rip
#==============================================================================
class Crip(设备.I路由信息协议):
	def __init__(self, a):
		设备.I路由信息协议.__init__(self, a)
	def fg进入命令(self):
		return "router rip"
	def f执行通告网络命令(self, a命令, a网络号):
		if not 地址.S网络地址4.fi地址格式(a网络号):
			raise ValueError
		v命令 = 设备.C命令(a命令)
		v命令.f添加(a网络号)
		self.f切换到当前模式()
		self.m设备.f执行命令(v命令)
	def f通告网络(self, a网络号):
		self.f执行通告网络命令("network", a网络号)
	def f删除网络(self, a网络号):
		self.f执行通告网络命令("no network", a网络号)
	def f通告接口(self, a接口):
		raise NotImplementedError()
	def f删除接口(self, a接口):
		raise NotImplementedError()
class Cripng(设备.I路由信息协议):
	def __init__(self, a, a名称):
		设备.I路由信息协议.__init__(self, a)
		self.m名称 = str(a名称)
	def fg进入命令(self):
		return "ipv6 router " + self.fg模式参数()
	def fg模式参数(self):
		return self.m名称
	def fg通告接口命令(self):
		return "ipv6 rip %s enable" % (self.fg模式参数(),)
	def f执行通告接口命令(self, a接口):
		if not 地址.S网络地址6.fi地址格式(a网络号):
			raise ValueError
		v上级模式 = self.fg上级模式()
		v接口配置模式 = v上级模式.f模式_接口配置(a接口)
		v接口配置模式.f执行当前模式命令(self.fg通告接口命令())
	def f通告接口(self, a接口):
		raise NotImplementedError()
	def f删除接口(self, a接口):
		raise NotImplementedError()
#==============================================================================
# eigrp
#==============================================================================
class C经典eigrp(设备.I模式):
	def __init__(self, a, a自治系统号):
		设备.I模式.__init__(self, a)
		self.m自治系统号 = a自治系统号
	def fg进入命令(self):
		return "router eigrp " + str(self.m自治系统号)
	def fs路由器号(self, a):
		self.f切换到当前模式()
		self.m设备.f执行命令("eigrp router-id " + str(a))
	def f执行通告网络命令(self, a设置, a网络号):
		v命令 = 设备.C命令("network")
		v命令.f前置否定(a设置, c不)
		v地址 = 地址.S网络地址4(a网络号)
		v命令 += v地址.fg网络号s()
		v命令 += v地址.fg反掩码s()
		self.f执行当前模式命令(v命令)
	def f执行通告接口命令(self, a设置, a接口):
		v命令模板 = 设备.C命令("network")
		v命令模板.f前置否定(a设置, c不)
		v类型 = type(a接口)
		if v类型 == C接口配置:
			va地址 = a接口.fg地址()
		elif v类型 == str:
			v全局配置 = self.fg上级模式()
			v接口配置 = v全局配置.f模式_接口(a接口)
			va地址 = a接口.fg地址()
		else:
			raise ValueError
		self.f切换到当前模式()
		for v in va地址:
			v命令 = v命令模板.f复制()
			v命令.f添加(v.fg网络号s(), v.fg反掩码s())
			self.m设备.f执行命令(v命令)
	def f执行被动接口命令(self, a设置, a接口):
		v命令 = 设备.C命令("passive-interface")
		v命令.f前置否定(a设置, c不)
		v类型 = type(a接口)
		if v类型 == bool:
			if a接口:
				v命令 += "default"
			else:
				raise ValueError("a接口 不能为False")
		elif v类型 == str:
			if re.match(a接口, "default", re.IGNORECASE):
				v命令 += "default"
			else:
				v接口 = f创建接口(a接口)
				v命令 += v接口
		elif v类型 == 设备.S接口:
			v命令 += a接口
		self.f执行当前模式命令(v命令)
	def f开关(self, a):
		if a:
			v命令 = "no shutdown"
		else:
			v命令 = "shutdown"
		self.f执行当前模式命令(v命令)
	def f日志_邻居变化(self, a):
		if a:
			v命令 = "eigrp log-neighbor-changes"
		else:
			v命令 = "no eigrp log-neighbor-changes"
		self.f执行当前模式命令(v命令)
	def f日志_邻居警告(self, a):
		if a:
			v命令 = "eigrp log-neighbor-changes "
			if type(a) == int:
				v命令 += str(a)
		else:
			v命令 = "no eigrp log-neighbor-changes"
		self.f执行当前模式命令(v命令)
	def f通告网络(self, a网络号):
		self.f执行通告网络命令(True, a网络号)
	def f删除网络(self, a网络号):
		self.f执行通告网络命令(False, a网络号)
	def f通告接口(self, a接口):
		self.f执行通告接口命令(True, a接口)
	def f删除接口(self, a接口):
		self.f执行通告接口命令(False, a接口)
	def fs被动接口(self, a接口):
		self.f执行被动接口命令(True, a接口)
	def fd被动接口(self, a接口):
		self.f执行被动接口命令(False, a接口)
class C经典eigrp6(设备.I模式):
	def __init__(self, a, a自治系统号):
		设备.I模式.__init__(self, a)
		self.m自治系统号 = int(a自治系统号)
	def fg进入命令(self):
		return "ipv6 router eigrp " + str(self.m自治系统号)
	def fs路由器号(self, a):
		v命令 = 设备.C命令("eigrp router-id")
		v命令 += a
		self.f切换到当前模式()
		self.m设备.f执行命令(v命令)
	def f开关(self, a):
		self.f切换到当前模式()
		if a:
			self.m设备.f执行命令("no shutdown")
		else:
			self.m设备.f执行命令("shutdown")
	def fg通告接口命令(self):
		return "ipv6 eigrp " + str(self.m自治系统号)
	def f通告接口(self, a接口):
		raise NotImplementedError()
	def f删除接口(self, a接口):
		raise NotImplementedError()
class C命名eigrp(设备.I模式):
	def __init__(self, a):
		设备.I模式.__init__(self, a)
	def f模式_地址族(self, a名称, a自治系统号):
		raise NotImplementedError()
	def f模式_服务族(self, a名称, a自治系统号):
		raise NotImplementedError()
class Ceigra地址族(设备.I模式):
	def __init__(self, a, a自治系统号):
		设备.I模式.__init__(self, a)
		self.m自治系统号 = a自治系统号
	def fg退出命令(self):
		return "exit-address-family"
class Ceigra地址族接口(设备.I模式):
	def __init__(self, a):
		设备.I模式.__init__(self, a)
	def fg退出命令(self):
		return "exit-af-interface"
#==============================================================================
# ospf
#==============================================================================
class Cospf(设备.I开放最短路径优先):
	def __init__(self, a, a进程号):
		设备.I开放最短路径优先.__init__(self, a, a进程号)
	#命令
	def fg进入命令(self):
		return 设备.C命令("router ospf") + self.fg模式参数()
	def f执行通告网络命令(self, a设置, a网络号, a区域):
		v命令 = Cospf.f通告网络命令(a设置, a网络号, a区域)
		self.f执行当前模式命令(v命令)
	def f执行通告接口命令(self, a设置, a接口, a区域):
		v命令 = Cospf.f通告接口命令(a设置, self.m进程号, a区域)
		v接口 = self.f模式_接口(a接口)
		v接口.f执行当前模式命令(v命令)
	@staticmethod
	def f通告网络命令(a设置, a网络号, a区域):
		v命令 = 设备.C命令("network")
		v命令.f前置否定(a设置, c不)
		v地址 = 地址.S网络地址4(a网络号)
		v区域 = 设备.I开放最短路径优先.f解析区域(a区域)
		v命令.f添加(v地址.fg网络号s(), v地址.fg反掩码s(), "area", v区域)
		return v命令
	@staticmethod
	def f通告接口命令(a设置, a进程号, a区域):
		v命令 = 设备.C命令("ip ospf")
		v命令.f前置否定(a设置, c不)
		v区域 = 设备.I开放最短路径优先.f解析区域(a区域)
		v命令.f添加(a进程号, "area", v区域)
		return v命令
	#模式
	def f模式_接口(self, a接口):
		v接口 = f创建接口(a接口)
		v模式 = Cospf接口(self.fg上级模式(), v接口)
		return v模式
	def f模式_区域(self, a区域):
		v区域 = 设备.I开放最短路径优先.f解析区域(a区域)
		return Cospf区域(self, v区域)
	#显示
	def f显示_路由表(self):
		return self.m设备.f执行显示命令("show ip route ospf")
	#操作
	def f重启进程(self):
		v命令 = 设备.C命令("clear ip ospf process")
		v命令.f添加(self.m进程号)
		self.m设备.f执行用户命令(v命令)
	def fs路由器号(self, a):
		if a == "default" or a == None:
			v命令 = 设备.C命令("default router-id")
		else:
			v地址 = 地址.S网络地址4(a)
			v命令 = 设备.C命令("router-id")
			v命令.f添加(v地址.fg地址s())
		self.f执行当前模式命令(v命令)
	def f通告网络(self, a网络号, a区域):
		self.f执行通告网络命令(True, a网络号, a区域)
	def f删除网络(self, a网络号, a区域):
		self.f执行通告网络命令(False, a网络号, a区域)
	def f通告接口(self, a接口, a区域):
		self.f执行通告接口命令(True, a接口, a区域)
	def f删除接口(self, a接口, a区域):
		self.f执行通告接口命令(False, a接口, a区域)
class Cospf区域(设备.I开放最短路径优先区域, 设备.C同级模式):
	def __init__(self, a, a区域):
		设备.I开放最短路径优先区域.__init__(self, a, a区域)
	def f通告网络(self, a网络号):
		self.fg上级模式().f执行通告网络命令(True, a网络号, self.m区域)
	def f删除网络(self, a网络号):
		self.fg上级模式().f执行通告网络命令(False, a网络号, self.m区域)
	def f通告接口(self, a接口):
		self.fg上级模式().f执行通告接口命令(True, a接口, self.m区域)
	def f删除接口(self, a接口):
		self.fg上级模式().f执行通告接口命令(False, a接口, self.m区域)
class Cospf接口(设备.I开放最短路径优先接口):
	def __init__(self, a, a接口: 设备.S接口):
		设备.I开放最短路径优先接口.__init__(self, a, a接口)
	def f执行设置时间命令(self, a命令, a时间):
		v命令 = 设备.C命令(a命令)
		if a时间:
			v命令.f添加(int(a时间))
		else:
			v命令.f前面添加(c不)
		self.f执行当前模式命令(v命令)
	def fs问候时间(self, a时间 = 10):
		self.f执行设置时间命令("ip ospf hello-interval", a时间)
	def fs死亡时间(self, a时间 = 40):
		self.f执行设置时间命令("ip ospf dead-interval", a时间)
	def fs重传时间(self, a时间 = 5):
		raise NotImplementedError()
	def fs传输时间(self, a时间 = 1):
		raise NotImplementedError()
	def fs开销(self, a开销):
		raise NotImplementedError()
	def fs网络类型(self, a类型):
		raise NotImplementedError()
class Cospf虚链路(设备.I开放最短路径优先虚链路):
	def __init__(self, a, a区域, p对端):
		设备.I开放最短路径优先虚链路.__init__(self, a, a区域, p对端)
	#命令
	def fg进入命令(self):
		return 设备.C命令("router ospf") + self.fg模式参数()
gaospf邻居状态 = {
	"DOWN": 设备.E开放最短路径优先邻居状态.e关闭,
	"ATTEMP": 设备.E开放最短路径优先邻居状态.e尝试,
	"INIT": 设备.E开放最短路径优先邻居状态.e初始,
	"TWO-WAY": 设备.E开放最短路径优先邻居状态.e双向,
	"EXSTART": 设备.E开放最短路径优先邻居状态.e预启动,
	"EXCHANGE": 设备.E开放最短路径优先邻居状态.e交换,
	"FULL": 设备.E开放最短路径优先邻居状态.e完成
}
gaospf选举状态 = {
	"-": 设备.E开放最短路径优先选举状态.e无,
	"DR": 设备.E开放最短路径优先选举状态.e指定,
	"BDR": 设备.E开放最短路径优先选举状态.e备用,
	"DR other": 设备.E开放最短路径优先选举状态.e非指定
}
class Cospf邻居表:
	c邻居开始 = 0
	c优先级开始 = 16
	c状态开始 = 22
	c死亡时间开始 = 38
	c地址开始 = 50
	c接口开始 = 66
	def __init__(self, a字符串):
		self.m字符串 = a字符串
	def __iter__(self):
		return self.fe行()
	def fe行(self):
		for v行 in 字符串.fe分割(self.m字符串, "\n"):
			if v行.count(".") != 6:	#2个地址共6个点
				continue
			v邻居s, v优先级s, v状态s, v死亡s, v地址s, v接口s = 字符串.fe按位置分割(v行, Cospf邻居表.c邻居开始, Cospf邻居表.c优先级开始, Cospf邻居表.c状态开始, Cospf邻居表.c死亡时间开始, Cospf邻居表.c地址开始, Cospf邻居表.c接口开始)
			v邻居 = 地址.S网络地址4.fc地址字符串(v邻居s)
			v优先级 = int(v优先级s)
			v状态分割 = v状态s.split("/")
			v邻居状态 = gaospf邻居状态[v状态分割[0]]
			v选举状态 = gaospf选举状态[v状态分割[1]]
			v死亡时间分割 = v死亡s.split(":")
			v死亡时间 = datetime.timedelta(hours = int(v死亡时间分割[0]), minutes = int(v死亡时间分割[1]), seconds = int(v死亡时间分割[2]))
			v对端地址 = 地址.S网络地址4.fc地址字符串(v地址s)
			v接口 = 设备.S接口.fc字符串(v接口s, ga接口名称)
			yield 设备.S开放最短路径优先邻居项(a邻居标识 = v邻居, a优先级 = v优先级, a邻居状态 = v邻居状态, a选举状态 = v选举状态, a死亡时间 = v死亡时间, a对端地址 = v对端地址, a接口 = v接口)
#==============================================================================
# bgp
#==============================================================================
class Cbgp(设备.I边界网关协议):
	def __init__(self, a, a自治系统号):
		设备.I边界网关协议.__init__(self, a, a自治系统号)
	#命令
	def fg进入命令(self):
		return 设备.C命令("router eigrp") + self.fg模式参数()
	#模式
	#显示
	def f显示_路由表(self):
		v命令 = "show ip route bgp"
		self.f执行当前模式命令(v命令)
	def f显示_邻居(self):
		v命令 = "show ip bgp summary"
		self.f执行当前模式命令(v命令)
class Cbgp对等体(设备.I边界网关协议对等体):
	def __init__(self, a, p对等体):
		设备.I边界网关协议对等体.__init__(self, a, p对等体)

#==============================================================================
# mstp
#==============================================================================
class C接口生成树(设备.I生成树接口配置模式):
	def __init__(self, a, a接口):
		设备.I生成树接口配置模式.__init__(self, a, a接口)
	def fs根保护(self, a):
		v命令 = 设备.C命令("spanning-tree guard root")
		v命令.f前置否定(a, c不)
		self.f执行当前模式命令(v命令)
	def fs环路保护(self, a):
		v命令 = 设备.C命令("spanning-tree guard loop")
		v命令.f前置否定(a, c不)
		self.f执行当前模式命令(v命令)
	def fs开销(self, a树, a开销):
		v命令 = 设备.C命令("spanning-tree vlan %d cost" % (int(a树),))
		if a:
			v命令 += int(a)
		else:
			v命令.f前面添加(c不)
		self.f执行当前模式命令(v命令)
class C接口多生成树(C接口生成树, 设备.C同级模式):
	def __init__(self, a, a接口):
		C接口多生成树.__init__(self, a, a接口)
	def fs开销(self, a树, a开销):
		v命令 = 设备.C命令("spanning-tree mst %d cost" % (int(a树),))
		if a:
			v命令 += int(a)
		else:
			v命令.f前面添加(c不)
		self.f执行当前模式命令(v命令)
class C多生成树协议(设备.I多生成树):
	def __init__(self, a):
		设备.I多生成树.__init__(self, a)
	def f模式_多生成树配置(self):
		if not hasattr(self, "m配置模式"):
			self.m配置模式 = C多生成树配置(self)
		return self.m配置模式
	def fs实例映射(self, a实例, a虚拟局域网):
		self.m配置模式.fs实例映射(a实例, a虚拟局域网)
	def fs实例优先级(self, a实例, a优先级):
		v命令 = 设备.C命令("spanning-tree mst", a实例, "priority", a虚拟局域网)
	def fs实例开销(self, a接口, a实例, a开销):
		if isinstance(a接口, 设备.I接口配置模式):
			v命令 = 设备.C命令("spanning-tree mst", a实例, "cost", a开销)
			a接口.f执行当前模式命令(v命令)
		else:
			raise TypeError()
	def fs域名(self, a名称):
		self.m配置模式.fs域名(a名称)
	def fs版本(self, a版本):
		self.m配置模式.fs版本(a版本)
class C多生成树配置(设备.I模式):
	def __init__(self, a):
		设备.I模式.__init__(self, a)
	def fg进入命令(self):
		return "spanning-tree mst configuration"
	def fs实例映射(self, a实例, a虚拟局域网):
		v命令 = 设备.C命令("instance", a实例, "vlan", a虚拟局域网)
		self.f执行当前模式命令(v命令)
	def fs域名(self, a名称):
		v命令 = 设备.C命令("name", a名称)
		self.f执行当前模式命令(v命令)
	def fs版本(self, a版本):
		v命令 = 设备.C命令("version", a版本)
		self.f执行当前模式命令(v命令)
#==============================================================================
# 地址池
#==============================================================================
class Cdhca地址池(设备.I动态主机配置协议地址池):
	def __init__(self, a, a名称):
		设备.I动态主机配置协议地址池.__init__(self, a, a名称)
	def fg进入命令(self):
		return 设备.C命令("ip dhcp pool") + self.fg模式参数()
	def fg模式参数(self):
		return self.m名称
	def fs网络范围(self, a网络号, p掩码):
		v命令 = 设备.C命令("network")
		self.f执行当前模式命令(v命令)
	def fs默认网关(self, p网关):
		v命令 = 设备.C命令("default-router")
		v命令.f添加(p网关)
		self.f执行当前模式命令(v命令)
	def fs租期(self, a时间):
		raise NotImplementedError()
	def fs域名服务器(self, a地址):
		v命令 = 设备.C命令("dns-server address")
		v命令.f添加(a地址)
		self.f执行当前模式命令(v命令)
#==============================================================================
# dhcp
#==============================================================================
class Cdhcp(设备.I动态主机配置协议, 设备.C同级模式):
	def __init__(self, a):
		设备.I动态主机配置协议.__init__(self, a)
	def f显示_已分配地址(self):
		return self.m设备.f执行显示命令("show ip dhcp binding")
	def f开关(self, a):
		v命令 = "service dhcp"
		if not a:
			v命令 = c不 + v命令
		self.f切换到当前模式()
		self.m设备.f执行命令(v命令)
#==============================================================================
# acl
#==============================================================================
class I访问控制列表(设备.I访问控制列表):
	c允许 = "permit"
	c拒绝 = "deny"
	def __init__(self, a, a名字, a类型 = "", a协议 = "ip"):
		设备.I访问控制列表.__init__(self, a)
		self.m名字 = a名字
		self.m类型 = a类型
		self.m协议 = a协议
	def fg模式参数(self):
		return (self.m类型, self.m名字)
	def fg进入命令(self):
		return "%s access-list %s %s" % (self.m协议, self.m类型, self.m名字)
	def f删除规则(self, a序号: int):
		self.f执行当前模式命令(c不 + str(a序号))
	@staticmethod
	def f解析允许(a允许):
		if type(a允许) == str:
			if a允许 in (I访问控制列表.c允许, I访问控制列表.c拒绝):
				return a允许
		if a允许:
			return I访问控制列表.c允许
		else:
			return I访问控制列表.c拒绝
	@staticmethod
	def f解析地址4(a地址):
		"转成字符串"
		v地址 = 设备.C访问控制列表.f解析地址4(a地址)
		v类型 = type(v地址)
		if v类型 == ipaddress.IPv4Address:
			return "host %s" % (v地址,)
		elif v类型 == ipaddress.IPv4Network:
			return "%s %s" % (v地址.network_address, v地址.hostmask)
		elif v类型 == str:
			return v地址
		elif a地址 == None:
			return "any"
		else:
			raise TypeError("无法解析的类型")
	@staticmethod
	def f解析地址6(a地址):
		v地址 = 设备.C访问控制列表.f解析地址6(a地址)
		v类型 = type(v地址)
		if v类型 == ipaddress.IPv6Address:
			return "host %s" % (v地址,)
		elif v类型 == ipaddress.IPv6Network:
			return "%s %s" % (v地址.network_address, v地址.hostmask)
		elif v类型 == str:
			return v地址
		elif a地址 == None:
			return "any"
		else:
			raise TypeError("无法解析的类型")
	@staticmethod
	def f解析端口(a端口):
		def f多值(a符号):
			v类型 = type(a端口.m端口)
			if v类型 == list:
				s = a符号
				for v in a端口.m端口:
					s += " " + str(v)
				return s
			elif v类型 == int:
				return a符号 + " " + str(a端口.m端口)
			else:
				raise TypeError("无法解析的类型")
		def f单值(a符号, p偏移 = 0):
			return a符号 + " " + str(int(a端口.m端口) + p偏移)
		def f范围(p范围):
			return "range %d %d" % (p范围.start, p范围.stop - 1)
		if not a端口:
			return ""
		v类型 = type(a端口)
		if v类型 == 设备.C访问控制列表.S端口:
			if a端口.m符号 == 设备.C访问控制列表.E符号.e等于:
				return f多值("eq")
			elif a端口.m符号 == 设备.C访问控制列表.E符号.e不等于:
				return f多值("neq")
			elif a端口.m符号 == 设备.C访问控制列表.E符号.e大于:
				return f单值("gt")
			elif a端口.m符号 == 设备.C访问控制列表.E符号.e大于等于:
				return f单值("gt", -1)
			elif a端口.m符号 == 设备.C访问控制列表.E符号.e小于:
				return f单值("lt")
			elif a端口.m符号 == 设备.C访问控制列表.E符号.e小于等于:
				return f单值("lt", +1)
			elif a端口.m符号 == 设备.C访问控制列表.E符号.e无:
				return ""
			elif a端口.m符号 == 设备.C访问控制列表.E符号.e范围:
				return f范围(a端口.m端口)
			else:
				raise TypeError("无法解析的类型")
		elif v类型 == int:
			return "eq " + str(a端口)
		elif v类型 == range:
			return f范围(a端口)
		else:
			raise TypeError("无法解析的类型")
class C标准访问控制列表(I访问控制列表):
	def __init__(self, a, a名字):
		I访问控制列表.__init__(self, a, a名字, a类型 = "standard")
	def f添加规则(self, a序号 = -1, a规则 = 设备.C访问控制列表.S规则(a允许 = False)):
		if a序号 == None or a序号 < 0:
			v序号 = ""
		else:
			v序号 = a序号
		v允许 = I访问控制列表.f解析允许(a规则.m允许)
		v源地址 = I访问控制列表.f解析地址4(a规则.m源地址)
		v命令 = "%s %s %s" % (v序号, v允许, v源地址)
		self.f执行当前模式命令(v命令)
	def f删除规则(self, a序号):
		self.f执行当前模式命令(c不 + str(v序号))
class C扩展访问控制列表(I访问控制列表):
	def __init__(self, a, a名字):
		I访问控制列表.__init__(self, a, a名字, a类型 = "extended")
	def f添加规则(self, a序号 = -1, a规则 = 设备.C访问控制列表.S规则(a允许 = False)):
		v命令 = 设备.C命令()
		if a序号 == None or a序号 < 0:
			pass
		else:
			v命令 += a序号
		v命令 += I访问控制列表.f解析允许(a规则.m允许)
		#确定
		if a规则.m协议 == 设备.C访问控制列表.E协议.ipv4:
			v命令 += "ip"
			v层 = 3
		elif a规则.m协议 == 设备.C访问控制列表.E协议.tcp:
			v命令 += "tcp"
			v层 = 4
		elif a规则.m协议 == 设备.C访问控制列表.E协议.udp:
			v命令 += "udp"
			v层 = 4
		else:
			raise ValueError("无法识别的协议")
		#按层
		if v层 == 3:
			v命令 += I访问控制列表.f解析地址4(a规则.m源地址)
			v命令 += I访问控制列表.f解析地址4(a规则.m目的地址)
		elif v层 == 4:
			v命令 += I访问控制列表.f解析地址4(a规则.m源地址)
			v命令 += I访问控制列表.f解析端口(a规则.m源端口)
			v命令 += I访问控制列表.f解析地址4(a规则.m目的地址)
			v命令 += I访问控制列表.f解析端口(a规则.m目的端口)
		else:
			raise NotImplementedError("迷之逻辑")
		#执行命令
		self.f执行当前模式命令(v命令)
	def f删除规则(self, a序号):
		self.f执行当前模式命令(c不 + str(v序号))
class Cipv6访问控制列表(I访问控制列表):
	def __init__(self, a, a名字):
		I访问控制列表.__init__(self, a, a名字, a协议 = "ipv6")
	def f添加规则(self, a序号 = -1, a规则 = 设备.C访问控制列表.S规则(a允许 = False)):
		if a序号 == None or a序号 < 0:
			v序号 = ""
		else:
			v序号 = "sequence" + str(a序号)
		v允许 = I访问控制列表.f解析允许(a规则.m允许)
		v源地址 = I访问控制列表.f解析地址6(a规则.m源地址)
		v命令 = "%s %s %s" % (v序号, v允许, v源地址)
		self.f执行当前模式命令(v命令)
	def f删除规则(self, a序号):
		self.f执行当前模式命令(c不 + str(v序号))
class C助手_访问控制列表(设备.I访问控制列表助手):
	def F计算(p0, p1):
		@staticmethod
		def f(n):
			v类型 = type(n)
			if v类型 == int:
				if n in range(p0[0], p0[1]):
					return n + p0[2]
				elif n in range(p1[0], p1[1]):
					return n + p1[2]
				else:
					raise ValueError("n超出范围")
			else:
				return n
		return f
	f计算序号_标准4 = F计算((0, 99, 1), (100, 799, 1200))
	f计算序号_扩展4 = F计算((0, 99, 100), (100, 799, 1900))
	f反算序号_标准4 = F计算((1, 100, -1), (1301, 2000, -1200))
	f反算序号_扩展4 = F计算((100, 200, -100), (2000, 2700, -1900))
#==============================================================================
# 工具
#==============================================================================
class C实用工具:
	@staticmethod
	def f接口字符串(a接口: 设备.S接口)->str:
		s = g接口名称[a接口.m名称]
		for i in range(len(a接口.m序号) - 1):
			s += str(a接口.m序号[i]) + '/'
		s += a接口.m序号[-1]
		if a接口.m子序号:
			s += '.' + str(a接口.m子序号)
		return s
	@staticmethod
	def f接口字符串_复杂(a接口: 设备.S接口)->str:	#支持连续地址
		def f连续(p字符串: str, p范围: range):
			#返回'f0/0.1-f0/0.100'这样子的字符串
			#字符串:'f0/0.',范围:range(1,101)
			v前 = p字符串 + str(p范围.start)
			v后 = p字符串 + str(p范围.stop - 1)
			return v前 + '-' + v后
		#S接口
		s = g接口名称[a接口.m名称]
		for i in range(len(a接口.m序号) - 1):
			s += str(a接口.m序号[i]) + '/'
		if type(a接口.m序号[-1]) == range:	#最后一段是连续的
			return f连续(s, a接口.m序号[-1])
		else:
			s += a接口.m序号[-1]
			if a接口.m子序号:
				if type(a接口.m子序号) == range:	#子序号是连续的
					return f连续(s + '.', a接口.m子序号)
				else:
					s += '.' + str(a接口.m子序号)
			return s
	@staticmethod
	def f路由协议_执行接口命令(a路由, a接口, a命令):	#在路由模式中调用,在接口执行命令
		v命令 = str(a命令)
		v接口类型 = type(a接口)
		if v接口类型 == 设备.I接口配置模式:	#接口是一个模式对象,直接切换模式
			a接口.f切换到当前模式()
			a接口.m设备.f执行命令(v命令)
		elif v接口类型 == 设备.S接口:	#构造模式对像并切换
			v接口 = a路由.m模式栈[1].f模式_接口配置(a接口)
			a接口.f切换到当前模式()
			a接口.m设备.f执行命令(v命令)
		else:
			raise TypeError("无法识别 a接口 的类型")