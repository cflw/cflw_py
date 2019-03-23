import cflw网络设备 as 设备
import cflw时间 as 时间
import 网络设备.通用_登录 as 通用登录
ca登录方式 = {
	设备.E登录方式.e控制台: "aux",
	设备.E登录方式.e虚拟终端: "vty"
}
ca登录认证方式 = {
	设备.E登录认证方式.e无: "none",
	设备.E登录认证方式.e密码: "password",
	设备.E登录认证方式.e账号: "scheme",
	设备.E登录认证方式.e认证授权记账: "scheme"
}
class C登录(设备.I登录配置模式):
	def __init__(self, a, a登录, a范围 = None):
		设备.I登录配置模式.__init__(self, a)
		self.m登录 = a登录
		self.m范围 = a范围
	def fg进入命令(self):
		v命令 = 设备.C命令("user-interface")
		v命令 += self.fg模式参数()
		return v命令
	def fg模式参数(self):
		v登录 = (ca登录方式[self.m登录],)
		return v登录 + 通用登录.f生成范围元组(self.m登录, self.m范围)
	def fs认证方式(self, a认证方式):
		v命令 = 设备.C命令("authentication-mode")
		v命令 += ca登录认证方式[a认证方式]
		self.f执行当前模式命令(v命令)
	def fs访问控制列表(self, a访问列表):
		v命令 = "acl %s inbound" % (a访问列表, )
		self.f执行当前模式命令(v命令)
	def fs操作超时(self, a秒):
		v命令 = 设备.C命令("idle-timeout")
		v命令 += 时间.f总秒拆成分秒(a秒)
		self.f执行当前模式命令(v命令)
