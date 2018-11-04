import cflw网络设备 as 设备
import cflw网络地址 as 地址
ga接口名称 = 设备.fc接口名称字典({})
f创建接口 = 设备.F创建接口(ga接口名称)
ga接口缩写 = {
	"Fa": 设备.E接口.e快速以太网,
	"Gi": 设备.E接口.e吉比特以太网
}
c次 = "secondary"
c不 = "no"
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
	#显示
	def f显示_当前模式配置(self):
		self.m设备.f执行用户命令("show running-config interface " + self.fg模式参数())
	#操作
	def f开关(self, a开关):
		v命令 = 设备.C命令("shutdown")
		v命令.f前置否定(a开关, c不)
		self.f执行当前模式命令(v命令)
	def fs网络地址4(self, a地址, a次地址 = False):
		v命令 = 设备.C命令("ip address")
		v命令 += f生成地址和掩码(a地址)
		if a次地址:
			v命令 += c次
		self.f执行当前模式命令(v命令)
	def f添加网络地址4(self, a地址):
		self.fs网络地址4(a地址, True)
	def f删除网络地址4(self, a地址 = None, a次地址 = False):
		v命令 = 设备.C命令("no ip address")
		if a地址:
			v命令 = f生成地址和掩码(a地址)
		self.f执行当前模式命令(v命令)
	def f添加网络地址6(self, a地址):
		v命令 = 设备.C命令("ipv6 address")
		v命令 += f生成地址和前缀长度6(a地址)
		self.f执行当前模式命令(v命令)
	def f删除网络地址6(self, a地址):
		v命令 = 设备.C命令("no ipv6 address")
		v命令 += f生成地址和前缀长度6(a地址)
		self.f执行当前模式命令(v命令)