import cflw网络设备 as 设备
from 网络设备.华为_常量 import *
import 网络设备.通用_实用 as 通用实用
import 网络设备.华为_实用 as 华为实用
import 网络设备.华为_接口 as 接口
class C配置(设备.I虚拟局域网):
	def __init__(self, a, a编号):
		设备.I虚拟局域网.__init__(self, a, a编号)
	#动作
	def fs描述(self, a描述 = "", a操作 = 设备.E操作.e设置):
		v命令 = 通用实用.f生成描述命令(a命令 = c命令_描述, a不 = c不, a描述 = a描述, a操作 = a操作)
		self.f执行当前模式命令(v命令)
	def fs端口(self, a接口, a操作 = 设备.E操作.e添加):
		v接口 = 接口.f创建接口(a接口)
		v命令 = 设备.C命令("port")
		if not v接口.fi范围():
			v命令 += v接口
		elif v接口.fi只有末尾序号是范围():
			v命令 += 华为实用.f生成接口范围(v接口)
		else:	#展开
			for v接口 in a接口.fe接口():
				v命令 = "port %s" % (v接口,)
				self.f执行当前模式命令(v命令)
			return
		self.f执行当前模式命令(v命令)