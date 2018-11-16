import cflw网络设备 as 设备
class C用户(设备.I用户配置模式):
	def __init__(self, a, a用户名):
		设备.I用户配置模式.__init__(self, a, a用户名)
	def fg模式参数(self):
		return self.m用户名
	def fg进入命令(self):
		v命令 = 设备.C命令("local-user")
		v命令 += self.fg模式参数()
		return v命令
	def fs密码(self, a密码):
		v命令 = 设备.C命令("password cipher")
		v命令 += a密码
		self.f执行当前模式命令(v命令)
	def fs权限(self, a权限):
		raise NotImplementedError()
	def fs服务类型(self, a服务类型):
		raise NotImplementedError()
class C用户s2126(C用户):
	def __init__(self, a, a用户名):
		C用户.__init__(self, a, a用户名)
class C用户v5(C用户):
	def __init__(self, a, a用户名):
		C用户.__init__(self, a, a用户名)
	def fs权限(self, a权限):
		v命令 = 设备.C命令("authorization-attribute level")
		v命令 += a权限
		self.f执行当前模式命令(v命令)
class C用户v7(C用户):
	def __init__(self, a, a用户名):
		C用户.__init__(self, a, a用户名)
	def fs权限(self, a权限):
		v命令 = 设备.C命令("authorization-attribute user-role level")
		v命令 += a权限
		self.f执行当前模式命令(v命令)
class C用户v7_1(C用户):
	def __init__(self, a, a用户名):
		C用户.__init__(self, a, a用户名)
	def fs权限(self, a权限):
		v命令 = 设备.C命令("authorization-attribute user-role")
		v类型 = type(a权限)
		if v类型 == int:
			v命令 += "level-%d" % (a权限,)
		else:
			v命令 += a权限
		self.f执行当前模式命令(v命令)
