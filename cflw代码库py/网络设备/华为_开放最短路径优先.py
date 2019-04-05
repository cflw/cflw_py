import cflw网络设备 as 设备
import cflw网络地址 as 地址
from 网络设备.华为_常量 import *
import 网络设备.通用_实用 as 通用实用
import 网络设备.通用_路由 as 通用路由
import 网络设备.通用_接口 as 通用接口
import 网络设备.华为_接口 as 接口
def f生成通告网络命令4(a网络号, a操作):
	v操作 = 通用实用.f解析操作(a操作)
	v地址 = 地址.S网络地址4.fc自动(a网络号)
	v命令 = 设备.C命令("network")
	v命令 += v地址.fg地址s(), v地址.fg反掩码s()
	if v操作 == 设备.E操作.e删除:
		v命令.f前面添加(c不)
	return v命令
def f生成通告接口命令4(a进程号, a区域, a操作):
	v区域 = 通用路由.f解析开放最短路径优先区域(a区域)
	v操作 = 通用实用.f解析操作(a操作)
	v命令 = 设备.C命令("ospf enable")
	v命令 += a进程号
	v命令 += "area " + v区域
	return v命令
class C路由4(设备.I开放最短路径优先):
	def __init__(self, a, a进程号):
		设备.I开放最短路径优先.__init__(self, a, a进程号)
		self.m路由器号 = None
	def fg模式参数(self):
		v命令 = 设备.C命令(self.m进程号)
		if self.m路由器号:
			v命令 += "router-id"
			v命令 += self.m路由器号
		return v命令
	def fg进入命令(self):
		return 设备.C命令("ospf") + self.fg模式参数()
	def f模式_区域(self, a区域):
		v区域 = 通用路由.f解析开放最短路径优先区域(a区域)
		return C区域4(self, v区域)
	def f模式_接口(self, a接口):
		v接口 = 接口.f创建接口(a接口)
		return C接口4(self, v接口)
	#显示
	def f显示_路由表(self):
		return self.m设备.f执行显示命令("display ip routing-table protocol ospf")
	#操作
	def fs路由器号(self, a):
		self.m路由器号 = a
	def fs通告网络(self, a网络号, a区域, a操作 = 设备.E操作.e设置):
		v区域 = self.f模式_区域(a区域)
		v区域.f通告网络(a网络号)
	def fs通告接口(self, a接口, a区域, a操作 = 设备.E操作.e设置):
		C接口4.f执行通告接口命令(a接口, True, self.m进程号, a区域)
class C区域4(设备.I开放最短路径优先区域):
	def __init__(self, a, a区域号):
		设备.I开放最短路径优先区域.__init__(self, a, a.fg进程号(), a区域号)
	def fg模式参数(self):
		return str(self.m区域号)
	def fg进入命令(self):
		return "area " + self.fg模式参数()
	def fs通告网络(self, a网络号, a操作 = 设备.E操作.e设置):
		v命令 = f生成通告网络命令4(a网络号, a操作)
		self.f执行当前模式命令(v命令)
	def fs通告接口(self, a接口, a操作 = 设备.E操作.e设置):
		v接口模式 = self.fg上级模式().f模式_接口()
		v接口模式.fs通告接口(self.fg进程号(), self.fg区域号(), a操作)
class C接口4(设备.I开放最短路径优先接口):
	def __init__(self, a, a进程号, a接口):
		设备.I开放最短路径优先接口.__init__(self, a, a接口)
	@通用接口.A接口自动展开
	def fs通告接口(self, a区域, a操作 = 设备.E操作.e设置):
		v命令 = f生成通告接口命令4(self.m进程号, a区域, a操作)
		self.f执行当前模式命令(v命令)