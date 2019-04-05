import cflw网络设备 as 设备
# 注意: 下面所有代码均未测试. 具体步骤见 http://www.ruijie.com.cn/fw/qdwd/57697/
c启动字符 = '\x03'  #ctrl+c	进入启动模式
c顶级字符 = '\x1a'	#ctrl+z	回到顶级菜单
c命令字符 = '\x11'	#ctrl+q	v11敲命令用
c命令字符1 = '\x10'	#ctrl+p	v11敲命令用
class C启动v10(设备.I启动模式):
	"""v10.4(2)之前可用"""
	def __init__(self, a):
		设备.I启动模式.__init__(self, a)
	def f等待提示符(self, a超时 = 60):
		v秒表 = 时间.C秒表()
		while True:
			v输出 = self.m设备.f输出(a等待 = False)
			if "*" in v输出:
				break
			if v秒表.f滴答() >= a超时:
				raise TimeoutError()
	def f登录(self, a密码 = "", a超时 = 60):
		v秒表 = 时间.C秒表()
		while True:
			self.m设备.f输入(c启动字符)
			time.sleep(1)
			v输出 = self.m设备.f输出(a等待 = False)
			if "*" in v输出:
				break	#不需要输密码
			#超时判断
			if v秒表.f滴答() >= a超时:
				raise TimeoutError()
	def f清除配置(self):
		self.m设备.f执行命令("4")	#4. File management utilities
		self.m设备.f执行命令("1")	#1. Remove a file.
		self.m设备.f执行命令("config.txt")
		self.f等待提示符()
	def f重新启动(self):
		self.m设备.f执行命令("2")	#2. Run Main.
class C启动v1042(设备.I启动模式):
	"""v10.4(2)之后, v11之前可用"""
	def __init__(self, a):
		设备.I启动模式.__init__(self, a)
	def f等待提示符(self, a超时 = 60):
		v秒表 = 时间.C秒表()
		while True:
			v输出 = self.m设备.f输出(a等待 = False)
			if "Ctrl>" in v输出:
				break
			if v秒表.f滴答() >= a超时:
				raise TimeoutError()
	def f登录(self, a密码 = "", a超时 = 60):
		v秒表 = 时间.C秒表()
		while True:
			self.m设备.f输入(c启动字符)
			time.sleep(1)
			v输出 = self.m设备.f输出(a等待 = False)
			if "Ctrl>" in v输出:
				break	#不需要输密码
			#超时判断
			if v秒表.f滴答() >= a超时:
				raise TimeoutError()
	def f清除配置(self):
		self.m设备.f执行命令("delete config.txt")
		self.m设备.f执行命令("y")
		self.f等待提示符()
	def f重新启动(self):
		self.m设备.f执行命令("load")
class C启动v11(设备.I启动模式):
	"""v11之后可用"""
	def __init__(self, a):
		设备.I启动模式.__init__(self, a)
	def f登录(self, a密码 = "", a超时 = 60):
		v秒表 = 时间.C秒表()
		while True:
			self.m设备.f输入(c启动字符)
			time.sleep(1)
			v输出 = self.m设备.f输出(a等待 = False)
			if "*" in v输出:
				break	#不需要输密码
			#超时判断
			if v秒表.f滴答() >= a超时:
				raise TimeoutError()
	def f清除配置(self):
		self.m设备.f输入(c命令字符)
		self.m设备.f执行命令("main_config_password_clear")	#执行命令后会加载系统
	def f重新启动(self):
		self.m设备.f执行命令("2")	#2. Run Main.
