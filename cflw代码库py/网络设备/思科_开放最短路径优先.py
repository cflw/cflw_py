import cflw网络设备 as 设备
import cflw网络地址 as 地址
from 网络设备.思科_常量 import *
import 网络设备.通用_实用 as 通用实用
import 网络设备.通用_路由 as 通用路由
import 网络设备.通用_接口 as 通用接口
import 网络设备.思科_实用 as 思科实用
import 网络设备.思科_接口 as 接口
def f生成通告网络命令4(a网络号, a区域号, a操作):
	v地址 = 地址.S网络地址4.fc自动(a网络号)
	v区域 = 通用路由.f解析开放最短路径优先区域(a区域号)
	v命令 = 设备.C命令("network")
	v命令.f前面添加(思科实用.ca命令前缀[a操作])
	v命令.f添加(v地址.fg网络号s(), v地址.fg反掩码s(), "area", v区域)
	return v命令
def f生成通告接口命令4(a进程号, a区域号, a操作):
	v区域 = 通用路由.f解析开放最短路径优先区域(a区域号)
	v操作 = 通用实用.f解析操作(a操作)
	v命令 = 设备.C命令("ip ospf")
	v命令.f前面添加(思科实用.ca命令前缀[a操作])
	v命令.f添加(a进程号, "area", v区域)
	return v命令
def f生成虚链路命令前缀(a区域号, a路由器号):
	v区域 = 通用路由.f解析开放最短路径优先区域(a区域号)
	v地址 = 地址.S网络地址4.fc自动(a路由器号)
	v命令 = 设备.C命令("area %s virtual-link %s" % (v区域, v地址.fg地址s()))
	return v命令
#===============================================================================
# 模式
#===============================================================================
class C路由配置(设备.I开放最短路径优先):
	def __init__(self, a, a进程号):
		设备.I开放最短路径优先.__init__(self, a, a进程号)
	#命令
	def fg进入命令(self):
		return 设备.C命令("router ospf") + self.fg模式参数()
	#模式
	def f模式_接口(self, a接口):
		v接口 = 接口.f创建接口(a接口)
		v模式 = C接口4(self.fg上级模式(), self.m进程号, v接口)
		return v模式
	def f模式_区域(self, a区域号):
		v区域 = 通用路由.f解析开放最短路径优先区域(a区域号)
		return C区域4(self, self.m进程号, v区域)
	#显示
	def f显示_路由表(self):
		return self.m设备.f执行显示命令("show ip route ospf")
	#操作
	def f重启进程(self):
		v命令 = 设备.C命令("clear ip ospf process")
		v命令.f添加(self.m进程号)
		self.m设备.f执行用户命令(v命令)
	def fs路由器号(self, a):
		if a == "default" or a == None:
			v命令 = 设备.C命令("default router-id")
		else:
			v地址 = 地址.S网络地址4(a)
			v命令 = 设备.C命令("router-id")
			v命令.f添加(v地址.fg地址s())
		self.f执行当前模式命令(v命令)
	def fs通告网络(self, a网络号, a区域号, a操作 = 设备.E操作.e设置):
		v命令 = f生成通告网络命令4(a网络号, a区域号, a操作)
		self.f执行当前模式命令(v命令)
	def fs通告接口(self, a接口, a区域号, a操作 = 设备.E操作.e设置):
		v接口 = self.f模式_接口(a接口)
		v接口.fs通告接口(a区域号, a操作)
class C区域4(设备.I开放最短路径优先区域, 设备.C同级模式):
	def __init__(self, a, a进程号, a区域号):
		设备.I开放最短路径优先区域.__init__(self, a, a进程号, a区域号)
	def fs通告网络(self, a网络号, a操作 = 设备.E操作.e设置):
		self.fg上级模式().fs通告网络(a网络号, self.fg区域号(), a操作)
	def fs通告接口(self, a接口, a操作 = 设备.E操作.e设置):
		self.fg上级模式().fs通告接口(a接口, self.fg区域号(), a操作)
class C接口4(设备.I开放最短路径优先接口):
	def __init__(self, a, a进程号, a接口: 设备.S接口):
		设备.I开放最短路径优先接口.__init__(self, a, a进程号, a接口)
	def f执行设置时间命令(self, a命令, a时间):
		v命令 = 设备.C命令(a命令)
		if a时间:
			v命令.f添加(int(a时间))
		else:
			v命令.f前面添加(c不)
		self.f执行当前模式命令(v命令)
	def fs通告接口(self, a区域号, a操作 = 设备.E操作.e设置):
		v命令 = f生成通告接口命令4(a设置, self.fg进程号(), a区域号)
		v接口.f执行当前模式命令(v命令)
	def fs问候时间(self, a时间 = 10):
		self.f执行设置时间命令("ip ospf hello-interval", a时间)
	def fs死亡时间(self, a时间 = 40):
		self.f执行设置时间命令("ip ospf dead-interval", a时间)
	def fs重传时间(self, a时间 = 5):
		raise NotImplementedError()
	def fs传输时间(self, a时间 = 1):
		raise NotImplementedError()
	def fs开销(self, a开销):
		v命令 = 设备.C命令("ip ospf cost")
		v命令 += a开销
		self.f执行当前模式命令(v命令)
	def fs网络类型(self, a类型):
		raise NotImplementedError()
class C虚链路4(设备.I开放最短路径优先虚链路, 设备.C同级模式):
	def __init__(self, a, a进程号, a区域号, a对端):
		设备.I开放最短路径优先虚链路.__init__(self, a, a进程号, a区域号, a对端)
#===============================================================================
# 显示
#===============================================================================
ca邻居状态 = {
	"DOWN": 设备.E开放最短路径优先邻居状态.e关闭,
	"ATTEMP": 设备.E开放最短路径优先邻居状态.e尝试,
	"INIT": 设备.E开放最短路径优先邻居状态.e初始,
	"TWO-WAY": 设备.E开放最短路径优先邻居状态.e双向,
	"EXSTART": 设备.E开放最短路径优先邻居状态.e预启动,
	"EXCHANGE": 设备.E开放最短路径优先邻居状态.e交换,
	"FULL": 设备.E开放最短路径优先邻居状态.e完成
}
ca选举状态 = {
	"-": 设备.E开放最短路径优先选举状态.e无,
	"DR": 设备.E开放最短路径优先选举状态.e指定,
	"BDR": 设备.E开放最短路径优先选举状态.e备用,
	"DR other": 设备.E开放最短路径优先选举状态.e非指定
}
class C邻居表4:
	c邻居开始 = 0
	c优先级开始 = 16
	c状态开始 = 22
	c死亡时间开始 = 38
	c地址开始 = 50
	c接口开始 = 66
	ca列开始 = (c邻居开始, c优先级开始, c状态开始, c死亡时间开始, c地址开始, c接口开始)
	def __init__(self, a字符串):
		self.m字符串 = a字符串
	def __iter__(self):
		return self.fe行()
	def fe行(self):
		for v行 in 字符串.fe分割(self.m字符串, "\n"):
			if v行.count(".") != 6:	#2个地址共6个点
				continue
			v邻居s, v优先级s, v状态s, v死亡s, v地址s, v接口s = 字符串.fe按位置分割(v行, *ca列开始)
			v邻居 = 地址.S网络地址4.fc地址字符串(v邻居s)
			v优先级 = int(v优先级s)
			v状态分割 = v状态s.split("/")
			v邻居状态 = ca邻居状态[v状态分割[0]]
			v选举状态 = ca邻居状态[v状态分割[1]]
			v死亡时间分割 = v死亡s.split(":")
			v死亡时间 = datetime.timedelta(hours = int(v死亡时间分割[0]), minutes = int(v死亡时间分割[1]), seconds = int(v死亡时间分割[2]))
			v对端地址 = 地址.S网络地址4.fc地址字符串(v地址s)
			v接口 = 设备.S接口.fc字符串(v接口s, ga接口名称)
			yield 设备.S开放最短路径优先邻居表项(a邻居标识 = v邻居, a优先级 = v优先级, a邻居状态 = v邻居状态, a选举状态 = v选举状态, a死亡时间 = v死亡时间, a对端地址 = v对端地址, a接口 = v接口)
