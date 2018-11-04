import cflw网络设备 as 设备
class C当代(设备.I路由信息协议):
	def __init__(self, a):
		设备.I路由信息协议.__init__(self, a)
	def fg进入命令(self):
		return "router rip"
	def f执行通告网络命令(self, a命令, a网络号):
		if not 地址.S网络地址4.fi地址格式(a网络号):
			raise ValueError()
		v命令 = 设备.C命令(a命令)
		v命令.f添加(a网络号)
		self.f切换到当前模式()
		self.m设备.f执行命令(v命令)
	def f通告网络(self, a网络号):
		self.f执行通告网络命令("network", a网络号)
	def f删除网络(self, a网络号):
		self.f执行通告网络命令("no network", a网络号)
	def f通告接口(self, a接口):
		raise NotImplementedError()
	def f删除接口(self, a接口):
		raise NotImplementedError()
class C下代(设备.I路由信息协议):
	def __init__(self, a, a名称):
		设备.I路由信息协议.__init__(self, a)
		self.m名称 = str(a名称)
	def fg进入命令(self):
		return "ipv6 router " + self.fg模式参数()
	def fg模式参数(self):
		return self.m名称
	def fg通告接口命令(self):
		return "ipv6 rip %s enable" % (self.fg模式参数(),)
	def f执行通告接口命令(self, a接口):
		if not 地址.S网络地址6.fi地址格式(a网络号):
			raise ValueError()
		v上级模式 = self.fg上级模式()
		v接口配置模式 = v上级模式.f模式_接口配置(a接口)
		v接口配置模式.f执行当前模式命令(self.fg通告接口命令())
	def f通告接口(self, a接口):
		raise NotImplementedError()
	def f删除接口(self, a接口):
		raise NotImplementedError()
