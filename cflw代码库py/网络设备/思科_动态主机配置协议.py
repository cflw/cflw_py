import cflw网络设备 as 设备
import cflw网络地址 as 地址
c不 = "no"
#===============================================================================
# 地址池
#===============================================================================
class C地址池4(设备.I动态主机配置协议地址池):
	def __init__(self, a, a名称):
		设备.I动态主机配置协议地址池.__init__(self, a, a名称)
	def fg进入命令(self):
		return 设备.C命令("ip dhcp pool") + self.fg模式参数()
	def fg模式参数(self):
		return self.m名称
	def fs网络范围(self, a网络号):
		v网络号 = 地址.S网络地址4.fc自动(a网络号)
		v命令 = 设备.C命令("network")
		v命令 += v网络号.fg地址s()
		v命令 += "/%d" % (v网络号.fg前缀长度())
		self.f执行当前模式命令(v命令)
	def fs默认网关(self, a网关):
		v网关 = 地址.S网络地址4.fc自动(a网关)
		v命令 = 设备.C命令("default-router")
		v命令 += v网关.fg地址s()
		self.f执行当前模式命令(v命令)
	def fs租期(self, a时间):
		raise NotImplementedError()
	def fs域名服务器(self, a地址):
		v命令 = 设备.C命令("dns-server address")
		v命令.f添加(a地址)
		self.f执行当前模式命令(v命令)
class C服务4(设备.I动态主机配置协议, 设备.C同级模式):
	def __init__(self, a):
		设备.I动态主机配置协议.__init__(self, a)
	def f显示_已分配地址(self):
		return self.m设备.f执行显示命令("show ip dhcp binding")
	def f开关(self, a):
		v命令 = "service dhcp"
		if not a:
			v命令 = c不 + v命令
		self.f切换到当前模式()
		self.m设备.f执行命令(v命令)
class C地址池6(设备.I动态主机配置协议地址池):
	def __init__(self, a, a名称):
		设备.I动态主机配置协议地址池.__init__(self, a, a名称)
	def fg进入命令(self):
		return 设备.C命令("ipv6 dhcp pool") + self.fg模式参数()
	def fg模式参数(self):
		return self.m名称
	def fs网络范围(self, a网络号):
		v命令 = 设备.C命令("address prefix")
		v命令 += "%s/%d" % (a网络号.fg地址s(), a网络号.fg前缀长度())
		self.f执行当前模式命令(v命令)
	def fs默认网关(self, a网关):
		raise NotImplementedError()
	def fs租期(self, a时间):
		raise NotImplementedError()
	def fs域名服务器(self, a地址):
		v命令 = 设备.C命令("dns-server address")
		v命令.f添加(a地址)
		self.f执行当前模式命令(v命令)
class C服务6(设备.I动态主机配置协议, 设备.C同级模式):
	def __init__(self, a):
		设备.I动态主机配置协议.__init__(self, a)
	def f显示_已分配地址(self):
		return self.m设备.f执行显示命令("show ipv6 dhcp binding")
	def f开关(self, a):
		v命令 = "service dhcp"
		if not a:
			v命令 = c不 + v命令
		self.f切换到当前模式()
		self.m设备.f执行命令(v命令)
