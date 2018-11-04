import cflw网络设备 as 设备
class C接口生成树(设备.I生成树接口配置模式):
	def __init__(self, a, a接口):
		设备.I生成树接口配置模式.__init__(self, a, a接口)
	def fs根保护(self, a):
		v命令 = 设备.C命令("spanning-tree guard root")
		v命令.f前置否定(a, c不)
		self.f执行当前模式命令(v命令)
	def fs环路保护(self, a):
		v命令 = 设备.C命令("spanning-tree guard loop")
		v命令.f前置否定(a, c不)
		self.f执行当前模式命令(v命令)
	def fs开销(self, a树, a开销):
		v命令 = 设备.C命令("spanning-tree vlan %d cost" % (int(a树),))
		if a:
			v命令 += int(a)
		else:
			v命令.f前面添加(c不)
		self.f执行当前模式命令(v命令)
class C接口多生成树(C接口生成树, 设备.C同级模式):
	def __init__(self, a, a接口):
		C接口多生成树.__init__(self, a, a接口)
	def fs开销(self, a树, a开销):
		v命令 = 设备.C命令("spanning-tree mst %d cost" % (int(a树),))
		if a:
			v命令 += int(a)
		else:
			v命令.f前面添加(c不)
		self.f执行当前模式命令(v命令)
class C多生成树协议(设备.I多生成树):
	def __init__(self, a):
		设备.I多生成树.__init__(self, a)
		self.m配置模式 = None
	def f模式_多生成树配置(self):
		if not self.m配置模式:
			self.m配置模式 = C多生成树配置(self)
		return self.m配置模式
	def fs实例映射(self, a实例, a虚拟局域网):
		self.m配置模式.fs实例映射(a实例, a虚拟局域网)
	def fs实例优先级(self, a实例, a优先级):
		v命令 = 设备.C命令("spanning-tree mst", a实例, "priority", a虚拟局域网)
	def fs实例开销(self, a接口, a实例, a开销):
		if isinstance(a接口, 设备.I接口配置模式):
			v命令 = 设备.C命令("spanning-tree mst", a实例, "cost", a开销)
			a接口.f执行当前模式命令(v命令)
		else:
			raise TypeError()
	def fs域名(self, a名称):
		self.m配置模式.fs域名(a名称)
	def fs版本(self, a版本):
		self.m配置模式.fs版本(a版本)
class C多生成树配置(设备.I模式):
	def __init__(self, a):
		设备.I模式.__init__(self, a)
	def fg进入命令(self):
		return "spanning-tree mst configuration"
	def fs实例映射(self, a实例, a虚拟局域网):
		v命令 = 设备.C命令("instance", a实例, "vlan", a虚拟局域网)
		self.f执行当前模式命令(v命令)
	def fs域名(self, a名称):
		v命令 = 设备.C命令("name", a名称)
		self.f执行当前模式命令(v命令)
	def fs版本(self, a版本):
		v命令 = 设备.C命令("version", a版本)
		self.f执行当前模式命令(v命令)
