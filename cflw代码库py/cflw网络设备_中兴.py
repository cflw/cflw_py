import time
import enum
import cflw字符串 as 字符串
import cflw网络连接 as 连接
import cflw网络设备 as 设备
import cflw网络地址 as 地址
import cflw时间 as 时间
from 网络设备.中兴_常量 import *
import 网络设备.通用_实用 as 通用实用
import 网络设备.中兴_接口 as 接口
import 网络设备.中兴_基本表信息 as 基本表信息
#===============================================================================
# 工厂
#===============================================================================
class E型号(enum.IntEnum):
	zxr10_m6000 = 46000
def f创建设备(a连接, a型号, a版本 = 0):
	return C设备(a连接, a型号, a版本)
#===============================================================================
# 设备
#===============================================================================
class C设备(设备.I设备):
	def __init__(self, a连接, a型号, a版本):
		设备.I设备.__init__(self)
		if isinstance(a连接, 连接.I连接):
			self.m连接 = a连接
			self.m连接.fs编码("gb2312")
		else:
			raise TypeError("a连接 必须是 I连接 类型")
		self.m型号 = a型号
		self.m版本 = a版本
		self.fs自动换页("--More--")
	#输入输出
	def f输入_结束符(self):	#ctrl+c
		self.f输入(c结束符)
	def f执行显示命令(self, a命令, a自动换页 = True):
		v命令 = str(a命令)
		v输出 = 设备.I设备.f执行显示命令(self, a命令 = v命令, a自动换页 = a自动换页)
		v输出 = v输出.replace("\r\n", "\n")
		v输出 = 通用实用.f去头尾行(v输出)
		# if v输出.count("\n") < 10:	#输出行数太少,检测是否有异常
		# 	self.f检测命令异常(v输出)
		return v输出
	#动作
	def f退出(self):
		self.f执行命令("exit")
	#模式
	def f模式_用户(self):
		if self.m型号 == E型号.zxr10_m6000:
			v模式 = C用户模式m6000(self)
		else:
			raise NotImplementedError()
		return v模式
#===============================================================================
# 用户模式
#===============================================================================
class C用户模式m6000(设备.I用户模式):
	def __init__(self, a):
		设备.I用户模式.__init__(self, a)
	#模式
	def f事件_进入模式(self):
		self.m设备.f刷新()
		self.m设备.f输入_结束符()
		self.m设备.f输入_回车(-1, 5)
	def f模式_全局配置(self):
		return C全局配置m6000(self)
	#显示
	def f显示_启动配置(self):
		v输出 = self.m设备.f执行显示命令("show startup-config")
		return v输出
	def f显示_当前配置(self):
		v输出 = self.m设备.f执行显示命令("show running-config")
		return v输出
	def f显示_时间(self):
		v命令 = "show clock"
		v输出 = self.m设备.f执行显示命令(v命令)	#16:20:09 beijing Tue Mar 12 2019
		#解析
		v空格位置 = 字符串.f全部找(v输出, " ")
		v行结束 = v输出.find("\n")
		if v行结束 > 0:	#如果有换行符,截取到行结束
			v输出 = v输出[0 : v空格位置[0]] + v输出[v空格位置[1] : v行结束]
		else:	#如果没有换行符,截取到字符串结束
			v输出 = v输出[0 : v空格位置[0]] + v输出[v空格位置[1]:]	#09:09:36 Thu Sep 29 2016
		v时间 = time.strptime(v输出, "%H:%M:%S %a %b %d %Y")
		return v时间
	#显示具体
	def f显示_接口表(self):
		v命令 = "show interface brief"
		v输出 = self.m设备.f执行显示命令(v命令)
		return 基本表信息.C接口表(v输出)
	def f显示_网络接口表4(self):
		v命令 = "show ip interface brief"
		v输出 = self.m设备.f执行显示命令(v命令)
		return 基本表信息.C网络接口表4(v输出)
	#动作
	def f登录(self, a用户名 = "", a密码 = ""):
		time.sleep(1)
		v输出 = self.m设备.f输出()
		if "Username:" in v输出:
			v输出 = self.m设备.f执行命令(a用户名)
		if "Password:" in v输出:
			self.m设备.f执行命令(a密码)
	def f提升权限(self, a密码 = c提权密码, a级别 = None):
		v命令 = 设备.C命令("enable")
		if a级别:
			v命令 += a级别
		elif a密码 == c提权密码:	#使用默认的提权密码时,级别固定18
			v命令 += 18
		self.f执行当前模式命令(v命令)
		self.m设备.f执行命令(a密码)
#===============================================================================
# 全局配置
#===============================================================================
class C全局配置m6000(设备.I全局配置模式):
	def __init__(self, a):
		设备.I全局配置模式.__init__(self, a)
	#命令
	def fg进入命令(self):
		return "configure terminal"
	#模式
	def f模式_接口配置(self, a接口, a操作 = 设备.E操作.e设置):
		v接口 = 接口.f创建接口m6000(a接口)
		return 接口.C接口m6000(self, v接口)