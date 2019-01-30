import cflw网络设备 as 设备
import 网络设备.思科_密码 as 密码
from 网络设备.思科_常量 import *
#===============================================================================
# 用户配置
#===============================================================================
class C用户配置(设备.C同级模式, 设备.I用户配置模式):
	def __init__(self, a父模式, a用户名):
		设备.I用户配置模式.__init__(self, a父模式, a用户名)
		self.m命令前缀 = 设备.C命令("username %s " % (self.m用户名,))
	def fg删除命令(self):
		return c不 + self.m命令前缀
	#显示
	def f显示_当前模式配置(self):
		v命令 = "show running-config | section " + self.m命令前缀
		return self.m设备.f执行显示命令(v命令)
	#执行
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
