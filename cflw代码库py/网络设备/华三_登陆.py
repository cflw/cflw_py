import cflw网络设备 as 设备
from . import 通用_登陆 as 通用
ca登陆方式 = {
	设备.E登陆方式.e控制台: "aux",
	设备.E登陆方式.e虚拟终端: "vty"
}
ca登陆认证方式 = {
	设备.E登陆认证方式.e无: "none",
	设备.E登陆认证方式.e密码: "password",
	设备.E登陆认证方式.e账号: "scheme",
	设备.E登陆认证方式.e认证授权记账: "scheme"
}
class C登陆(设备.I登陆配置模式):
	def __init__(self, a, a登陆, a范围 = None):
		设备.I登陆配置模式.__init__(self, a)
		self.m登陆 = a登陆
		self.m范围 = a范围
	def fg进入命令(self):
		v命令 = 设备.C命令("user-interface")
		v命令 += self.fg模式参数()
		return v命令
	def fg模式参数(self):
		v登陆 = (ca登陆方式[self.m登陆],)
		return v登陆 + 通用.f生成范围元组(self.m登陆, self.m范围)
	def fs认证方式(self, a认证方式):
		v命令 = 设备.C命令("authentication-mode")
		v命令 += ca登陆认证方式[a认证方式]
		self.f执行当前模式命令(v命令)
	def fs访问控制列表(self, a访问列表):
		v命令 = "acl %s inbound" % (a访问列表, )
		self.f执行当前模式命令(v命令)
	def fs超时时间(self, a秒):
		v命令 = 设备.C命令("idle-timeout")
		v命令 += a秒 * 60
		self.f执行当前模式命令(v命令)
