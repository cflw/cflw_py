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
import 网络设备.思科_接口 as 接口
import 网络设备.思科_访问控制列表 as 访问控制列表
import 网络设备.思科_路由信息协议 as 路由信息协议
import 网络设备.思科_增强内部网关路由协议 as 增强内部网关路由协议
import 网络设备.思科_开放最短路径优先 as 开放最短路径优先
import 网络设备.思科_边界网关协议 as 边界网关协议
import 网络设备.思科_密码 as 密码
import 网络设备.思科_动态主机配置协议 as 动态主机配置协议
import 网络设备.思科_前缀列表 as 前缀列表
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
#===============================================================================
# 设备
#===============================================================================
ca错误文本与异常类 = [
	("% Invalid input detected at '^' marker.", 设备.X命令),	#语法错误
	("% Ambiguous command:", 设备.X命令),	#无法识别的命令
	("% Duplicate sequence number", 设备.X执行),	#重复的acl规则序号
	("% Multiple ports are allowed on named ACLs only", 设备.X执行),	#多端口号只允许在命名acl使用
]
class C设备(设备.I设备):
	def __init__(self, a连接):
		设备.I设备.__init__(self)
		if isinstance(a连接, 连接.I连接):
			self.m连接 = a连接
			self.m连接.fs编码("ascii")
		else:
			raise TypeError("a连接 必须是 I连接 类型")
		self.m异常 = True	#是否抛出异常
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
		self.f检测命令异常(v输出)
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
			self.f检测命令异常(v输出)
		return v输出
	def f检测命令异常(self, a输出):
		def f返回异常(ax):
			if type(ax) == type:
				v异常 = ax(a输出)
			else:
				v异常 = ax
			if self.m异常:
				raise v异常
			return v异常
		for v文本, vt异常 in ca错误文本与异常类:
			if v文本 in a输出:
				return f返回异常(vt异常)
		return None
	#助手
	def f助手_访问控制列表(self):
		return 访问控制列表.C助手()
	def f助手_密码(self, a强密码 = True):
		if a强密码:
			return 密码.C强密码助手()
		else:
			return 密码.C弱密码助手()
#===============================================================================
# 用户模式
#===============================================================================
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
#===============================================================================
# 信息
#===============================================================================
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
#===============================================================================
# 全局配置
#===============================================================================
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
		v接口 = 接口.f创建接口(a接口)
		return 接口.C接口配置(self, v接口)
	def f模式_用户配置(self, a):
		return C用户配置(self, a)
	def f模式_时间范围(self, a):
		return C时间范围(self, a)
	def f模式_访问控制列表(self, a名称, a类型 = 设备.E访问控制列表类型.e标准):
		def f整数范围检查(aa范围: list, a错误文本: str):
			if type(a名称) == int:
				for v in aa范围:
					if a名称 in v:
						return
				raise ValueError(a错误文本)
		#创建访问控制列表对象
		if a类型 == 设备.E访问控制列表类型.ipv4标准:
			f整数范围检查([range(1, 100), range(1300, 2000)], "标准访问控制列表号码范围应为1~99,1300~1999")
			return 访问控制列表.C标准4(self, a名称)
		elif a类型 == 设备.E访问控制列表类型.ipv4扩展:
			f整数范围检查([range(100, 200), range(2000, 2700)], "扩展访问控制列表号码范围应为100~199,2000~2699")
			return 访问控制列表.C扩展4(self, a名称)
		elif a类型 == 设备.E访问控制列表类型.ipv6:
			return 访问控制列表.C六(self, a名称)
		else:
			raise ValueError("未知的访问控制列表类型")
	def f模式_前缀列表(self, a名称, a类型 = 设备.E前缀列表类型.e版本4):
		if a类型 == 设备.E前缀列表类型.e版本4:
			return 前缀列表.C前缀列表(self, a名称, 前缀列表.c版本4, 地址.S网络地址4)
		elif a类型 == 设备.E前缀列表类型.e版本6:
			return 前缀列表.C前缀列表(self, a名称, 前缀列表.c版本6, 地址.S网络地址6)
		else:
			raise ValueError("错误的 a类型")
	#路由
	def f模式_路由信息协议(self, a进程号 = 0, a版本 = 设备.E版本.e路由信息协议):	#rip
		v版本 = 设备.C路由协议.f解析_版本(a版本)
		if v版本 == 设备.E版本.e路由信息协议:	#rip
			return 路由信息协议.C当代(self)
		elif v版本 == 设备.E版本.e下一代路由信息协议:	#ripng
			v进程号 = str(a进程号)
			if not v进程号:
				raise ValueError("当版本为ripng时,必须指定进程号")
			return 路由信息协议.C下代(self, a进程号)
		else:
			raise ValueError("未知的版本")
	def f模式_开放最短路径优先(self, a进程号, a版本 = 设备.E版本.e开放最短路径优先2):
		v版本 = 设备.C路由协议.f解析_版本(a版本)
		if a版本 == 设备.E版本.e开放最短路径优先2:
			return 开放最短路径优先.C路由配置(self, a进程号)
		elif a版本 == 设备.E版本.e开放最短路径优先3:
			return 开放最短路径优先.C路由配置(self, a进程号)
		else:
			raise ValueError("未知的版本")
	def f模式_增强内部网关路由协议(self, a, a版本 = 设备.E版本.e网络协议4):	#eigrp
		v类型 = type(a)
		if v类型 == int:
			return 增强内部网关路由协议.C经典(self, a)
	def f模式_边界网关协议(self, a自治系统号):
		return 边界网关协议.C路由(self, a自治系统号)
	#服务
	def f模式_动态主机配置协议地址池(self, a名称):
		return 动态主机配置协议.C地址池4(self, a名称)
	def f模式_动态主机配置协议(self):
		return 动态主机配置协议.C服务4(self)
#===============================================================================
# 时间
#===============================================================================
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
		设备.I用户配置模式.__init__(self, a父模式)
		self.m用户名 = str(a用户名)
		self.m命令前缀 = 设备.C命令("username %s " % (self.m用户名,))
	def f执行用户命令(self, a命令):
		v命令 = self.m命令前缀 + a命令
		self.f执行当前模式命令(v命令)
	def fs密码(self, a密码):
		v类型 = type(a密码)
		if v类型 == 密码.C包装:
			self.f执行用户命令(a密码)
		else:
			self.f执行用户命令("secret %s" % (a密码,))
	def fs权限等级(self, a权限等级):
		self.f执行用户命令("privildge %d" % (a权限等级,))
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
# 路由
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
		self.m设备.f执行命令('ip route ' + C静态路由.f解析参数(a网络号, a出接口))
	def f删除路由(self, a网络号, a出接口):
		self.m设备.f执行命令('no ip route ' + C静态路由.f解析参数(a网络号, a出接口))
	def fs默认路由(self, a出接口):
		self.m设备.f执行命令('ip route ' + C静态路由.f解析参数('0.0.0.0/0', a出接口))

#===============================================================================
# 工具
#===============================================================================
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
		def f连续(p字符串: str, a范围: range):
			#返回'f0/0.1-f0/0.100'这样子的字符串
			#字符串:'f0/0.',范围:range(1,101)
			v前 = p字符串 + str(a范围.start)
			v后 = p字符串 + str(a范围.stop - 1)
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