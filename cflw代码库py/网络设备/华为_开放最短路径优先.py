import cflw网络设备 as 设备
c不 = "undo"
class C路由(设备.I开放最短路径优先):
	def __init__(self, a, a进程号):
		设备.I开放最短路径优先.__init__(self, a, a进程号)
		self.m区域表 = {}
		self.m路由器号 = None
	def fg模式参数(self):
		v命令 = 设备.C命令(self.m进程号)
		if self.m路由器号:
			v命令 += "router-id"
			v命令 += self.m路由器号
		return v命令
	def fg进入命令(self):
		return 设备.C命令("ospf") + self.fg模式参数()
	def f模式_区域(self, a):
		v区域 = C路由.f计算区域号(a)
		if not v区域 in self.m区域表:
			self.m区域表[v区域] = C区域(self, v区域)
		return self.m区域表[v区域]
	@staticmethod
	def f计算区域号(a区域)->int:
		v类型 = type(a区域)
		if v类型 == int:
			return a区域
		elif v类型 == ipaddress.IPv4Address:
			return int(a区域)
		elif v类型 == str:
			if a区域.count('.') == 3:	#是ia地址格式
				return int(ipaddress.IPv4Address(a区域))
			else:
				return int(a区域)
		else:	#无法识别
			raise ValueError()
	#显示
	def f显示_路由表(self):
		return self.m设备.f执行显示命令("display ip routing-table protocol ospf")
	#操作
	def fs路由器号(self, a):
		self.m路由器号 = a
	def f通告网络(self, a网络号, a区域):
		v区域 = self.f模式_区域(a区域)
		v区域.f通告网络(a网络号)
	def f删除网络(self, a网络号, a区域):
		v区域 = self.f模式_区域(a区域)
		v区域.f删除网络(a网络号)
	def f通告接口(self, a接口, a区域):
		C接口.f执行通告接口命令(a接口, True, self.m进程号, a区域)
	def f删除接口(self, a接口, a区域):
		C接口.f执行通告接口命令(a接口, False, self.m进程号, a区域)
class C区域(设备.I模式):
	def __init__(self, a, a区域号):
		设备.I模式.__init__(self, a)
		self.m区域 = int(a区域号)
	def fg模式参数(self):
		return str(self.m区域)
	def fg进入命令(self):
		return "area " + self.fg模式参数()
	def fg进程号(self):
		return self.fg上级模式().m进程号
	@staticmethod
	def f生成通告网络命令(a网络号):
		v地址 = ipaddress.IPv4Network(a网络号, False)
		v分割 = 地址.C因特网协议4.f分割地址反掩码(v地址)
		return "network %s %s" % v分割
	def f通告网络(self, a网络号):
		v命令 = C区域.f生成通告网络命令(a网络号)
		self.f执行当前模式命令(v命令)
	def f删除网络(self, a网络号):
		v命令 = c不 + C区域.f生成通告网络命令(a网络号, self.m区域)
		self.f执行当前模式命令(v命令)
	def f通告接口(self, a接口):
		C接口.f执行通告接口命令(a接口, True, self.fg进程号(), self.m区域)
	def f删除接口(self, a接口):
		C接口.f执行通告接口命令(a接口, False, self.fg进程号(), self.m区域)
class C接口(设备.I开放最短路径优先接口):
	def __init__(self, a, a接口):
		设备.I开放最短路径优先接口.__init__(self, a, a接口)
	@staticmethod
	def f生成通告接口命令(a进程号, a区域):
		v命令 = 设备.C命令("ospf enable")
		v命令 += a进程号
		v命令 += "area " + str(a区域)
		return v命令
	@staticmethod
	def f执行通告接口命令(a接口, a肯定, a进程号, a区域):
		v命令 = C接口.f生成通告接口命令(a进程号, a区域)
		v命令.f前置否定(a肯定, c不)
		a接口.f执行当前模式命令(v命令)
	def f通告接口(self, a进程号, a区域):
		f执行通告接口命令(self, True, a进程号, a区域)
	def f删除接口(self, a进程号, a区域):
		f执行通告接口命令(self, False, a进程号, a区域)
