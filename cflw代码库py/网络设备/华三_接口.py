import cflw网络设备 as 设备
import cflw网络地址 as 地址
from 网络设备.华三_常量 import *
import 网络设备.通用_地址 as 通用地址
ca接口名称 = 设备.fc接口名称字典({
	设备.E接口.e虚拟局域网: "Vlan-interface",
})
f创建接口 = 设备.F创建接口(ca接口名称)
ca接口缩写 = {
	"Eth": 设备.E接口.e百兆以太网,
	"GE": 设备.E接口.e吉以太网,
	"XGE": 设备.E接口.e万兆以太网,
	"FGE": 设备.E接口.e四万兆以太网,
	"InLoop": 设备.E接口.e内部,
	"Loop": 设备.E接口.e环回,
	"NULL": 设备.E接口.e空,
	"Ser": 设备.E接口.e串行,
	"REG": 设备.E接口.e注册隧道,	#Register-Tunnel
}
def f生成地址命令4(a地址, a肯定, a次):
	v地址 = 地址.S网络地址4.fc自动(a地址)
	v命令 = 设备.C命令("ip address")
	v命令 += (v地址.fg地址s(), v地址.fg掩码s())
	v命令.f前置否定(a肯定, c不)
	if a次:
		v命令 += "sub"
	return v命令
class C接口(设备.I接口配置模式):
	def __init__(self, a, a接口):
		设备.I接口配置模式.__init__(self, a, a接口)
	#三层
	def fs网络地址4(self, a地址):
		v命令 = f生成地址命令4(a地址, True, False)
		self.f执行当前模式命令(v命令)
	def f添加网络地址4(self, a地址):
		v命令 = f生成地址命令4(a地址, True, True)
		self.f执行当前模式命令(v命令)
	def f删除网络地址4(self, a地址 = None):
		v命令 = f生成地址命令4(a地址, False, True)
		self.f执行当前模式命令(v命令)
	def fe网络地址4(self):
		v输出 = self.f显示_当前模式配置()
		for v in v输出.split("\n"):
			v地址 = 通用地址.f解析地址4(v)
			if v地址:
				yield v地址
	
