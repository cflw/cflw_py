import ipaddress
import cflw网络设备 as 设备
import cflw网络地址 as 地址
def f生成对等体字符串(a对等体):
	v类型 = type(a对等体)
	if v类型 == str:
		return a对等体
	elif v类型 == 地址.S网络地址4:
		return a对等体.fg地址s()
	elif v类型 in (ipaddress.IPv4Address, ipaddress.IPv6Address):
		return str(a对等体)
	elif v类型 in (ipaddress.IPv4Network, ipaddress.IPv4Interface, ipaddress.IPv6Network, ipaddress.IPv6Interface):
		return str(a对等体.ip)
	else:
		return str(a对等体)
class C路由(设备.I边界网关协议):
	def __init__(self, a, a自治系统号):
		设备.I边界网关协议.__init__(self, a, a自治系统号)
	#命令
	def fg进入命令(self):
		return 设备.C命令("router bgp") + self.fg模式参数()
	#模式
	def f模式_对等体(self, a对等体):
		return C对等体(self, f生成对等体字符串(a对等体))
	def f模式_对等体组(self, a对等体):
		return C对等体(self, f生成对等体字符串(a对等体), a对等体组 = True)
	def f模式_地址簇(self, *a地址簇):
		v地址簇类型 = a地址簇[0]
		if v地址簇类型 == 设备.E边界网关协议地址地址簇.e单播4:
			return C单播地址簇4(self)
	#显示
	def f显示_路由表(self):
		v命令 = "show ip route bgp"
		self.m设备.f执行显示命令(v命令)
	def f显示_邻居(self):
		v命令 = "show ip bgp summary"
		self.m设备.f执行显示命令(v命令)
#泛用模式
class C对等体(设备.I边界网关协议对等体, 设备.C同级模式):
	def __init__(self, a, a对等体, a对等体组 = False):
		设备.I边界网关协议对等体.__init__(self, a, a对等体)
		if a对等体组:
			v命令 = self.fg前置命令() + "peer-group"
			self.f执行当前模式命令(v命令)
	def fg前置命令(self):
		return 设备.C命令("neighbor " + self.m对等体)
	def f激活(self):
		v命令 = self.fg前置命令() + "activate"
		self.f执行当前模式命令(v命令)
	def f绑定对等体组(self, a对等体组):
		v命令 = self.fg前置命令() + "peer-group" + str(a对等体组)
class C地址簇(设备.I边界网关协议地址簇):
	def __init__(self, a, a地址簇):
		设备.I边界网关协议地址簇.__init__(self, a, a地址簇)
	def fg退出命令(self):
		return "exit-address-family"
#具体模式
class C单播地址簇4(C地址簇):
	def __init__(self, a, a地址簇 = ""):
		C地址簇.__init__(self, a, a地址簇)
	def fg进入命令(self):
		return "address-family ipv4 unicast"
	def f模式_对等体(self, a对等体):
		return C地址簇对等体4(self, f生成对等体字符串(a对等体))
class C地址簇对等体4(C对等体):
	def __init__(self, a, a对等体):
		C对等体.__init__(self, a, a对等体)
	def fs远端自治系统号(self, a自治系统号):
		v命令 = self.fg前置命令() + "remote-as" + a自治系统号
		self.f执行当前模式命令(v命令)
	def f通告网络(self, a网络号):
		v命令 = 设备.C命令("network")
		v地址 = 地址.S网络地址4.fc自动(a网络号)
		v命令.f添加(v地址.fg网络号s(), v地址.fg掩码s())
		self.f执行当前模式命令(v命令)
