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
#===============================================================================
# 工厂
#===============================================================================
class E型号(enum.IntEnum):
	zxr10_m6000 = 46000
def f创建设备(a连接, a型号, a版本):
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
		# self.fs自动换页("  ---- More ----")
	def f模式_用户(self):
		if a型号 == E型号.zxr10_m6000:
			return C用户模式m6000(self)
		else:
			raise NotImplementedError()
#===============================================================================
# 用户模式
#===============================================================================
class C用户模式m6000(设备.I用户模式):
	def __init__(self, a):
		设备.I用户模式.__init__(self, a)
	#模式
	def f模式_全局配置(self):
		return C全局配置m6000(self)
	#显示
	def f显示_启动配置(self):
		v输出 = self.m设备.f执行显示命令("show startup-config")
		return v输出
	def f显示_当前配置(self):
		v输出 = self.m设备.f执行显示命令("show running-config")
		return v输出
	#动作
	def f登录(self, a用户名 = "", a密码 = ""):
		raise NotImplementedError()
	def f提升权限(self, a密码 = c提权密码, a级别 = 18):
		v命令 = "enable %s" % (a级别,)
		self.f执行当前模式命令(v命令)
		self.m设备.f输入(a密码)
		self.m设备.f输入_回车()
#===============================================================================
# 全局配置
#===============================================================================
class C全局配置m6000(设备.I全局配置模式):
	def __init__(self, a):
		设备.I全局配置模式.__init__(self, a)
	#命令
	def fg进入命令(self):
		return "configure terminal"
	def fg退出命令(self):
		return "exit"
	#模式
	def f模式_接口(self, a接口, a操作 = 设备.E操作.e设置):
		v接口 = 接口.f创建接口m6000(a接口)
		return 接口.C接口m6000(self, v接口)