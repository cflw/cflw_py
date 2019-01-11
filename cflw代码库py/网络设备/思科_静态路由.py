import cflw网络设备 as 设备
import cflw网络地址 as 地址
def f生成静态路由命令(a网络号, a下一跳):
	#解析网络号
	v网络号 = 地址.S网络地址4.fc自动(a网络号)
class C静态路由(设备.C同级模式, 设备.I静态路由配置模式):
	def __init__(self, a):
		设备.I静态路由配置模式.__init__(self, a)
	@staticmethod
	def f解析参数(a网络号, a出接口):
		v网络号 = 地址.C因特网协议4.fc网络(a网络号, False)
		v分割 = v网络号.with_netmask.split('/')
		v接口 = 思科实用.f接口字符串(a出接口)
		s = "%s %s %s" % (*v分割, v接口)
		return s
	def fs路由4(self, a网络号, a下一跳, a操作 = 设备.E操作.e添加):

	def fs默认路由4(self, a出接口):
		self.m设备.f执行命令('ip route ' + C静态路由.f解析参数("0.0.0.0/0", a出接口))