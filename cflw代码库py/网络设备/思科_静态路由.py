import cflw网络设备 as 设备
import cflw网络地址 as 地址
from 网络设备.思科_常量 import *
import 网络设备.思科_实用 as 思科实用
import 网络设备.思科_路由表信息 as 路由表信息
def f生成静态路由命令(a网络号, a下一跳):
	v网络号 = 地址.S网络地址4.fc自动(a网络号)
	v接口 = 思科实用.f接口字符串(a出接口)
	v命令 = C命令("ip route %s %s %s" % (v网络号.fg地址s(), v网络号.fg掩码s(), v接口))
	return v命令
class C静态路由4(设备.C同级模式, 设备.I静态路由配置模式):
	def __init__(self, a):
		设备.I静态路由配置模式.__init__(self, a)
	def f显示_路由表(self):
		v命令 = 路由表信息.f生成显示路由表命令(设备.E版本.e网络协议4, 设备.E路由协议.e静态)
		v输出 = self.m设备.f执行显示命令(v命令)
		return 路由表信息.C路由表4(v输出)
	def fs路由(self, a网络号, a下一跳, a操作 = 设备.E操作.e添加):
		v命令 = f生成静态路由命令(a网络号, a下一跳)
		if a操作 == 设备.E操作.e删除:
			v命令.f前面添加(c不)
		self.f执行当前模式命令(v命令)
	def fs默认路由(self, a下一跳, a操作 = 设备.E操作.e添加):
		self.fs路由4("0.0.0.0/0", a下一跳, a操作)