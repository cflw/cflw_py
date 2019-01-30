import cflw网络设备 as 设备
ca接口名称 = 设备.fc接口名称字典({
	设备.E接口.e虚拟局域网: "Vlanif",
})
f创建接口 = 设备.F创建接口(ca接口名称)
#===============================================================================
# 接口
#===============================================================================
class C接口视图(设备.I接口配置模式):
	def __init__(self, a, a接口):
		设备.I接口配置模式.__init__(self, a, a接口)
	@staticmethod
	def f解析参数_网络地址(a地址, a次地址):
		v地址 = 地址.C因特网协议4.fc接口(a地址)
		v分割 = v地址.with_prefixlen.split('/')
		if a次地址:
			v次地址 = 'sub'
		else:
			v次地址 = ''
		return '%s %s %s' % (*v分割, v次地址)
	@staticmethod
	def f解析参数_虚拟局域网(a虚拟局域网):
		if type(a虚拟局域网) == range:
			return '%d to %d' % (a虚拟局域网.start, a虚拟局域网.stop - 1)
		else:
			return str(a虚拟局域网)
	@staticmethod
	def f解析参数_端口安全动作(a动作):
		v类型 = type(a动作)
		if v类型 == str:
			return a动作
		elif v类型 == int:
			return ("shutdown", "restrict", "protect")[a动作]
		elif v类型 == bool:
			if a动作:
				return "restrict"
			else:
				return "shutdown"
		return "restrict"
	#接口操作
	def f开关(self, a开关):
		self.f切换到当前模式()
		if a开关:
			self.m设备.f执行命令("undo shutdown")
		else:
			self.m设备.f执行命令("shutdown")
	def fs网络地址(self, a地址, a次地址 = False):
		"设置地址"
		self.f切换到当前模式()
		self.m设备.f执行命令("ip address " + C接口视图.f解析参数_网络地址(a地址, a次地址))
	#二层
	def f二层中继_允许通过(self, a虚拟局域网):
		self.m设备.f执行命令("port trunk allow-pass vlan " + C接口视图.f解析参数_虚拟局域网(a虚拟局域网))
	#端口安全
	def f端口安全_开关(self, a开关):
		if a开关:
			self.m设备.f执行命令("port-security enable")
		else:
			self.m设备.f执行命令("undo port-security enable")
	def f端口安全_s数量(self, a数量):
		v命令 = "port-security max-mac-num " + int(a数量)
		self.m设备.f执行命令(v命令)
	def f端口安全_s动作(self, a动作):
		v命令 = "port-security protect-action " + C接口视图.f解析参数_端口安全动作(a动作)
		self.m设备.f执行命令(v命令)
class C端口组(C接口视图):
	def __init__(self, a, a接口: 设备.S接口):
		C接口视图.__init__(self, a, a接口)
		#计算哈希
		v范围 = a接口.m序号[2]
		v字节 = struct.pack('iiiii', a接口.m名称, a接口.m序号[0], a接口.m序号[1], v范围.start, v范围.stop)
		v校验 = hashlib.md5()
		v校验.update(v字节)
		self.m哈希 = v校验.hexdigest()
	def fg模式参数(self):	#在这里确定不同厂商的接口名称
		return self.m哈希
	def fg进入命令(self):
		return 'port-group ' + self.fg模式参数()
	def f切换到当前模式(self):
		C接口视图.f切换到当前模式(self)
		#是否绑定端口,没有则绑定
