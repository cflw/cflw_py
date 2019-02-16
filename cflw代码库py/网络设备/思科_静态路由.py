import cflw网络设备 as 设备
import cflw网络地址 as 地址
from 网络设备.思科_常量 import *
import 网络设备.思科_实用 as 思科实用 
def f生成静态路由命令(a网络号, a下一跳):
	v网络号 = 地址.S网络地址4.fc自动(a网络号)
	v接口 = 思科实用.f接口字符串(a出接口)
	v命令 = C命令("ip route %s %s %s" % (v网络号.fg地址s(), v网络号.fg掩码s(), v接口))
	return v命令
class C静态路由(设备.C同级模式, 设备.I静态路由配置模式):
	def __init__(self, a):
		设备.I静态路由配置模式.__init__(self, a)
	def fs路由4(self, a网络号, a下一跳, a操作 = 设备.E操作.e添加):
		v命令 = f生成静态路由命令(a网络号, a下一跳)
		if a操作 == 设备.E操作.e删除:
			v命令.f前面添加(c不)
		self.f执行当前模式命令(v命令)
	def fs默认路由4(self, a下一跳, a操作 = 设备.E操作.e添加):
		self.fs路由4("0.0.0.0/0", a下一跳, a操作)