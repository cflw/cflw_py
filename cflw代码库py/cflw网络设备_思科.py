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
from 网络设备.思科_常量 import *
import 网络设备.通用_实用 as 通用实用
import 网络设备.思科_实用 as 思科实用
import 网络设备.思科_接口 as 接口
import 网络设备.思科_用户 as 用户
import 网络设备.思科_登录 as 登录
import 网络设备.思科_连接 as 连接包装
import 网络设备.思科_基本表信息 as 基本表信息
import 网络设备.思科_访问控制列表 as 访问控制列表
import 网络设备.思科_路由信息协议 as 路由信息协议
import 网络设备.思科_增强内部网关路由协议 as 增强内部网关路由协议
import 网络设备.思科_开放最短路径优先 as 开放最短路径优先
import 网络设备.思科_边界网关协议 as 边界网关协议
import 网络设备.思科_密码 as 密码
import 网络设备.思科_动态主机配置协议 as 动态主机配置协议
import 网络设备.思科_前缀列表 as 前缀列表
import 网络设备.思科_钥匙链 as 钥匙链
#===============================================================================
# 工厂
#===============================================================================
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
		self.fs自动换页("--More--")
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
		v模式 = C用户模式(self)
		# self.fs顶级模式(v模式)
		return v模式
	def f执行命令(self, a命令):
		v输出 = 设备.I设备.f执行命令(self, a命令)
		self.f检测命令异常(v输出)
		return v输出
	def f执行用户命令(self, a命令):
		v命令 = 设备.C命令(a命令)
		if not isinstance(self.fg当前模式(), C用户模式):	#在配置模式，命令前要加个do
			v命令.f前面添加(c做)
		v输出 = self.f执行命令(v命令)
		v输出 = v输出.replace("\r\n", "\n")
		return v输出
	def f执行显示命令(self, a命令, a自动换页 = True):
		v命令 = 设备.C命令(a命令)
		if not isinstance(self.fg当前模式(), C用户模式):	#在配置模式，命令前要加个do
			v命令.f前面添加(c做)
		v输出 = 设备.I设备.f执行显示命令(self, a命令 = v命令, a自动换页 = a自动换页)
		v输出 = v输出.replace("\r\n", "\n")
		v输出 = 通用实用.f去头尾行(v输出)
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
	def f事件_进入模式(self):
		self.m设备.f刷新()
		self.m设备.f输入_结束符()
		self.m设备.f输入_回车(-1, 5)
	def f模式_全局配置(self):
		self.f切换到当前模式()
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
		v命令 = "show clock"
		v输出 = self.m设备.f执行显示命令(v命令)	#*09:09:36.935 UTC Thu Sep 29 2016
		#解析
		v空格位置 = 字符串.f全部找(v输出, " ")
		v行结束 = v输出.find("\n")
		if v行结束 > 0:	#如果有换行符,截取到行结束
			v输出 = v输出[0 : v空格位置[0]] + v输出[v空格位置[1] : v行结束]
		else:	#如果没有换行符,截取到字符串结束
			v输出 = v输出[0 : v空格位置[0]] + v输出[v空格位置[1]:]	#*09:09:36.935 Thu Sep 29 2016
		v时间 = time.strptime(v输出, "*%H:%M:%S.%f %a %b %d %Y")
		return v时间
	def f显示_设备版本(self):
		return self.fg版本信息()
	#连接
	def f连接_网络终端(self, a地址, **a参数):
		return 连接包装.C网络终端(self, a地址, **a参数)
	#操作
	def f登录(self, a用户名 = "", a密码 = ""):
		self.m设备.f执行命令(a用户名)
		self.m设备.f执行命令(a密码)
	def f提升权限(self, a密码 = ""):
		v输出 = self.m设备.f执行命令("enable")
		while "Password" in v输出:
			v输出 = self.m设备.f执行命令(a密码)
		if "Error" in v输出:
			raise 设备.X执行(v输出)
	def fs终端监视(self, a开关):
		v命令 = 设备.C命令("terminal monitor")
		v命令.f前置否定(a开关, c不)
		self.m设备.f执行用户模式命令(v命令)
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
#===============================================================================
# 全局配置
#===============================================================================
class C全局配置(设备.I全局配置模式):
	c进入命令 = "configure terminal"
	def __init__(self, a父模式):
		设备.I全局配置模式.__init__(self, a父模式)
	#模式
	def fg进入命令(self):
		return C全局配置.c进入命令
	#基本模式
	def f模式_接口配置(self, a接口, a操作 = 设备.E操作.e设置):
		if isinstance(a接口, 设备.I接口配置模式):
			if not a接口.m设备 is self.m设备:
				raise ValueError("设备不匹配")
			v模式 = a接口
		else:
			v接口 = 接口.f创建接口(a接口)
			v模式 = 接口.C接口配置(self, v接口)
		思科实用.f执行模式操作命令(self, v模式, a操作)
		return v模式
	def f模式_用户配置(self, a, a操作 = 设备.E操作.e设置):
		if isinstance(a, 设备.I用户配置模式):
			if not a.m设备 is self.m设备:
				raise ValueError("设备不匹配")
			v模式 = a
		else:
			v模式 = 用户.C用户配置(self, a)
		if a操作 == 设备.E操作.e删除:
			v命令 = v模式.fg删除命令()
			self.f执行当前模式命令(v命令)
		return v模式
	def f模式_登录配置(self, a方式, a范围, a操作 = 设备.E操作.e设置):
		return 登录.C登录(self, a方式, a范围)
	def f模式_时间范围(self, a, a操作 = 设备.E操作.e设置):
		return C时间范围(self, a)
	def f模式_访问控制列表(self, a名称, a类型 = 设备.E访问控制列表类型.e标准, a操作 = 设备.E操作.e设置):
		def f整数范围检查(aa范围: list, a错误文本: str):
			if type(a名称) == int:
				for v in aa范围:
					if a名称 in v:
						return
				raise ValueError(a错误文本)
		#创建访问控制列表对象
		if a类型 == 设备.E访问控制列表类型.ipv4标准:
			f整数范围检查([range(1, 100), range(1300, 2000)], "标准访问控制列表号码范围应为1~99,1300~1999")
			v模式 = 访问控制列表.C标准4(self, a名称)
		elif a类型 == 设备.E访问控制列表类型.ipv4扩展:
			f整数范围检查([range(100, 200), range(2000, 2700)], "扩展访问控制列表号码范围应为100~199,2000~2699")
			v模式 = 访问控制列表.C扩展4(self, a名称)
		elif a类型 == 设备.E访问控制列表类型.ipv6:
			v模式 = 访问控制列表.C六(self, a名称)
		else:
			raise ValueError("未知的访问控制列表类型")
		if a操作 == 设备.E操作.e删除:
			v命令 = c不 + v模式.fg进入命令()
			self.f执行当前模式命令(v命令)
		elif a操作 == 设备.E操作.e重置:
			v命令 = c默认 + v模式.fg进入命令()
			self.f执行当前模式命令(v命令)
		return v模式
	def f模式_前缀列表(self, a名称, a类型 = 设备.E前缀列表类型.e版本4, a操作 = 设备.E操作.e设置):
		if a类型 == 设备.E前缀列表类型.e版本4:
			return 前缀列表.C前缀列表(self, a名称, 前缀列表.c版本4, 地址.S网络地址4)
		elif a类型 == 设备.E前缀列表类型.e版本6:
			return 前缀列表.C前缀列表(self, a名称, 前缀列表.c版本6, 地址.S网络地址6)
		else:
			raise ValueError("错误的 a类型")
	def f模式_钥匙链(self, a名称):
		return 钥匙链.C钥匙链(self, a名称)
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