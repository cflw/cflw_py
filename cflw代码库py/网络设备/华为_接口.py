import hashlib
import struct
import cflw网络设备 as 设备
from 网络设备.华为_常量 import *
import 网络设备.通用_地址 as 通用地址
import 网络设备.通用_接口 as 通用接口
import 网络设备.通用_虚拟局域网 as 通用虚拟局域网
import 网络设备.华为_实用 as 华为实用
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
	#模式
	def f模式_虚拟局域网(self):
		return C虚拟局域网(self.fg上级模式(), self.m接口)
	def f模式_开放最短路径优先(self, a进程号 = 1, a版本 = 设备.E协议.e开放最短路径优先):
		return self.fg上级模式().f模式_开放最短路径优先(a进程号 = a进程号, a版本 = a版本, a接口 = self.m接口)
	#接口操作
	@通用接口.A接口自动展开
	def fs开关(self, a操作 = 设备.E操作.e设置):
		v命令 = 通用实用.f生成开关命令("shutdown", c不, a操作)
		self.f执行当前模式命令(v命令)
	@通用接口.A接口自动展开
	def fs网络地址4(self, a地址, a操作 = 设备.E操作.e设置):
		v命令 = 设备.C命令("ip address")
		v命令 += 华为实用.f生成地址和前缀长度4(a地址)
		if a操作 == 设备.E操作.e设置:
			pass
		elif a操作 == 设备.E操作.e添加:
			v命令 += c次
		elif a操作 == 设备.E操作.e删除:
			v命令.f前面添加(c不)
		self.f执行当前模式命令(v命令)
class C端口组(C接口视图):	#需要重写!
	def __init__(self, a, a接口: 设备.S接口):
		C接口视图.__init__(self, a, a接口)
		#计算哈希
		v范围 = a接口.m序号[2]
		v字节 = struct.pack("iiiii", a接口.m名称, a接口.m序号[0], a接口.m序号[1], v范围.start, v范围.stop)
		v校验 = hashlib.md5()
		v校验.update(v字节)
		self.m哈希 = v校验.hexdigest()
	def fg模式参数(self):	#在这里确定不同厂商的接口名称
		return self.m哈希
	def fg进入命令(self):
		return 'port-group ' + self.fg模式参数()
	def f切换到当前模式(self):
		C接口视图.f切换到当前模式(self)
#虚拟局域网
class C虚拟局域网(设备.I虚拟局域网接口):
	ca链路类型 = {
		设备.E链路类型.e接入: "access",
		设备.E链路类型.e中继: "trunk",
		设备.E链路类型.e混合: "hybrid",
	}
	def __init__(self, a, a接口):
		设备.I虚拟局域网接口.__init__(self, a, a接口)
	@通用接口.A接口自动展开
	def fs链路类型(self, a类型):
		v命令 = 设备.C命令("port link-type")
		v命令 += C虚拟局域网.ca链路类型[a类型]
		self.f执行当前模式命令(v命令)
	@通用接口.A接口自动展开
	def f中继_s通过(self, a虚拟局域网, a操作 = 设备.E操作.e设置):
		v命令 = 设备.C命令("port trunk allow-pass vlan")
		v命令 += 通用虚拟局域网.f生成(a虚拟局域网)
		self.m设备.f执行命令(v命令)
	@通用接口.A接口自动展开
	def f接入_s绑定(self, a虚拟局域网, a操作 = 设备.E操作.e设置):
		v命令 = 设备.C命令("port default vlan")
		v命令 += 通用虚拟局域网.f生成一个(a虚拟局域网)
		self.f执行当前模式命令(v命令)
#端口安全
class C端口安全(设备.I端口安全接口):
	def __init__(self, a, a接口):
		设备.I端口安全接口.__init__(self, a, a接口)
	@通用接口.A接口自动展开
	def fs开关(self, a开关):
		if a开关:
			self.f执行当前模式命令("port-security enable")
		else:
			self.f执行当前模式命令("undo port-security enable")
	@通用接口.A接口自动展开
	def fs数量(self, a数量):
		v命令 = "port-security max-mac-num " + int(a数量)
		self.f执行当前模式命令(v命令)
	@通用接口.A接口自动展开
	def fs动作(self, a动作):
		v命令 = "port-security protect-action " + C端口安全.f生成动作(a动作)
		self.f执行当前模式命令(v命令)
	@staticmethod
	def f生成动作(a动作):
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
