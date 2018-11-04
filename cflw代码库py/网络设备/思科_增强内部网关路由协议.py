import cflw网络设备 as 设备
c不 = "no"
class C经典4(设备.I模式):
	def __init__(self, a, a自治系统号):
		设备.I模式.__init__(self, a)
		self.m自治系统号 = a自治系统号
	def fg进入命令(self):
		return "router eigrp " + str(self.m自治系统号)
	def fs路由器号(self, a):
		self.f切换到当前模式()
		self.m设备.f执行命令("eigrp router-id " + str(a))
	def f执行通告网络命令(self, a设置, a网络号):
		v命令 = 设备.C命令("network")
		v命令.f前置否定(a设置, c不)
		v地址 = 地址.S网络地址4(a网络号)
		v命令 += v地址.fg网络号s()
		v命令 += v地址.fg反掩码s()
		self.f执行当前模式命令(v命令)
	def f执行通告接口命令(self, a设置, a接口):
		v命令模板 = 设备.C命令("network")
		v命令模板.f前置否定(a设置, c不)
		v类型 = type(a接口)
		if v类型 == C接口配置:
			va地址 = a接口.fg地址()
		elif v类型 == str:
			v全局配置 = self.fg上级模式()
			v接口配置 = v全局配置.f模式_接口(a接口)
			va地址 = a接口.fg地址()
		else:
			raise ValueError()
		self.f切换到当前模式()
		for v in va地址:
			v命令 = v命令模板.f复制()
			v命令.f添加(v.fg网络号s(), v.fg反掩码s())
			self.m设备.f执行命令(v命令)
	def f执行被动接口命令(self, a设置, a接口):
		v命令 = 设备.C命令("passive-interface")
		v命令.f前置否定(a设置, c不)
		v类型 = type(a接口)
		if v类型 == bool:
			if a接口:
				v命令 += "default"
			else:
				raise ValueError("a接口 不能为False")
		elif v类型 == str:
			if re.match(a接口, "default", re.IGNORECASE):
				v命令 += "default"
			else:
				v接口 = f创建接口(a接口)
				v命令 += v接口
		elif v类型 == 设备.S接口:
			v命令 += a接口
		self.f执行当前模式命令(v命令)
	def f开关(self, a: bool):
		if a:
			v命令 = "no shutdown"
		else:
			v命令 = "shutdown"
		self.f执行当前模式命令(v命令)
	def f日志_邻居变化(self, a: bool):
		v命令 = 设备.C命令("eigrp log-neighbor-changes")
		v命令.f前置否定(a, c不)
		self.f执行当前模式命令(v命令)
	def f日志_邻居警告(self, a: bool):
		if a:
			v命令 = "eigrp log-neighbor-changes "
			if type(a) == int:
				v命令 += str(a)
		else:
			v命令 = "no eigrp log-neighbor-changes"
		self.f执行当前模式命令(v命令)
	def f通告网络(self, a网络号):
		self.f执行通告网络命令(True, a网络号)
	def f删除网络(self, a网络号):
		self.f执行通告网络命令(False, a网络号)
	def f通告接口(self, a接口):
		self.f执行通告接口命令(True, a接口)
	def f删除接口(self, a接口):
		self.f执行通告接口命令(False, a接口)
	def fs被动接口(self, a接口):
		self.f执行被动接口命令(True, a接口)
	def fd被动接口(self, a接口):
		self.f执行被动接口命令(False, a接口)
class C经典6(设备.I模式):
	def __init__(self, a, a自治系统号):
		设备.I模式.__init__(self, a)
		self.m自治系统号 = int(a自治系统号)
	def fg进入命令(self):
		return "ipv6 router eigrp " + str(self.m自治系统号)
	def fs路由器号(self, a):
		v命令 = 设备.C命令("eigrp router-id")
		v命令 += a
		self.f切换到当前模式()
		self.m设备.f执行命令(v命令)
	def f开关(self, a):
		self.f切换到当前模式()
		if a:
			self.m设备.f执行命令("no shutdown")
		else:
			self.m设备.f执行命令("shutdown")
	def fg通告接口命令(self):
		return "ipv6 eigrp " + str(self.m自治系统号)
	def f通告接口(self, a接口):
		raise NotImplementedError()
	def f删除接口(self, a接口):
		raise NotImplementedError()
class C命名(设备.I模式):
	def __init__(self, a):
		设备.I模式.__init__(self, a)
	def f模式_地址族(self, a名称, a自治系统号):
		raise NotImplementedError()
	def f模式_服务族(self, a名称, a自治系统号):
		raise NotImplementedError()
class C地址族(设备.I模式):
	def __init__(self, a, a自治系统号):
		设备.I模式.__init__(self, a)
		self.m自治系统号 = a自治系统号
	def fg退出命令(self):
		return "exit-address-family"
class C地址族接口(设备.I模式):
	def __init__(self, a):
		设备.I模式.__init__(self, a)
	def fg退出命令(self):
		return "exit-af-interface"