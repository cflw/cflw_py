import cflw网络设备 as 设备
import cflw网络地址 as 地址
from 网络设备.思科_常量 import *
ga接口名称 = 设备.fc接口名称字典({})
f创建接口 = 设备.F创建接口(ga接口名称)
ga接口缩写 = {
	"Fa": 设备.E接口.e快速以太网,
	"Gi": 设备.E接口.e吉比特以太网
}
c次 = "secondary"
def f生成地址和掩码4(a地址):
	v地址 = 地址.S网络地址4.fc自动(a地址)
	return "%s %s" % (v地址.fg地址s(), v地址.fg掩码s())
def f生成地址和前缀长度6(a地址):
	v地址 = 地址.S网络地址6.fc自动(a地址)
	return "%s /%d" % (v地址.fg地址s(), v地址.fg前缀长度())
class C接口配置(设备.I接口配置模式):
	def __init__(self, a父模式, a接口):
		设备.I接口配置模式.__init__(self, a父模式, a接口)
	def fg模式参数(self):
		return str(self.m接口)
	def fg删除命令(self):
		return c不 + self.fg进入命令()
	#显示
	def f显示_当前模式配置(self):
		self.m设备.f执行用户命令("show running-config interface " + self.fg模式参数())
	#操作
	def f开关(self, a开关):
		v命令 = 设备.C命令("shutdown")
		v命令.f前置否定(a开关, c不)
		self.f执行当前模式命令(v命令)
	def fs网络地址4(self, a地址, a操作 = 设备.E操作.e添加):
		v命令 = 设备.C命令("ip address")
		v命令 += f生成地址和掩码4(a地址)
		if a操作 == 设备.E操作.e设置:
			pass
		elif a操作 == 设备.E操作.e添加:
			v命令 += c次
		elif a操作 == 设备.E操作.e删除:
			v命令.f前面添加(c不)
		self.f执行当前模式命令(v命令)
	def fs网络地址6(self, a地址, a操作 = 设备.E操作.e添加):
		v命令 = 设备.C命令("ipv6 address")
		v命令 += f生成地址和前缀长度6(a地址)
		if a操作 == 设备.E操作.e删除:
			v命令.f前面添加(c不)
		self.f执行当前模式命令(v命令)
