import time
import cflw网络设备 as 设备
def f生成时间(a时间):
	return time.strftime("%H:%M:%S %d %b %Y", a时间)
class C钥匙链(设备.I模式):
	def __init__(self, a, a名称):
		设备.I模式.__init__(self, a)
		self.m名称 = a名称
	def fg模式参数(self):
		return self.m名称
	def fg进入命令(self):
		v命令 = 设备.C命令("key chain")
		v命令 += self.fg模式参数()
		return v命令
	def f模式_钥匙(self, a钥匙号: int):
		return C钥匙(self, a钥匙号)
	def f显示_当前模式配置():
		v命令 = 设备.C命令("show key chain")
		v命令 += self.fg模式参数()
		return self.m设备.f执行显示命令(v命令)
class C钥匙(设备.I模式):
	def __init__(self, a, a号码):
		设备.I模式.__init__(self, a)
		self.m号码 = a号码
	def fg模式参数(self):
		return self.m号码
	def fg进入命令(self):
		v命令 = 设备.C命令("key")
		v命令 += self.fg模式参数()
		return v命令
	def fs密码(self, a密码):
		v命令 = 设备.C命令("key-string")
		v命令 += a密码
		self.f执行当前模式命令(v命令)
	def f执行时间命令(self, a命令, a开始时间, a结束时间):
		v命令 = 设备.C命令(a命令)
		v命令 += f生成时间(a开始时间)
		v命令 += f生成时间(a结束时间)
		self.f执行当前模式命令(v命令)
	def fs发送时间(self, a开始时间, a结束时间):
		self.f执行时间命令("send-lifetime", a开始时间, a结束时间)
	def fs接收时间(self, a开始时间, a结束时间):
		self.f执行时间命令("accept-lifetime", a开始时间, a结束时间)
