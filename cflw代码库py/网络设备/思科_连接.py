import cflw网络设备 as 设备
class C网络终端(设备.I连接包装):
	def __init__(self, a模式, a地址, **a参数):
		设备.I连接包装.__init__(self, a模式)
		v命令 = 设备.C命令("telnet")
		v命令 += a地址
		a模式.m设备.f执行用户命令(v命令)