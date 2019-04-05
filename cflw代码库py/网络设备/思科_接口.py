import cflw网络设备 as 设备
import cflw网络地址 as 地址
from 网络设备.思科_常量 import *
import 网络设备.通用_实用 as 通用实用
import 网络设备.思科_实用 as 思科实用
import 网络设备.通用_接口 as 通用接口
ca接口名称 = 设备.fc接口名称字典({})
f创建接口 = 设备.F创建接口(ca接口名称)
ca接口缩写 = {
	"Fa": 设备.E接口.e快速以太网,
	"Gi": 设备.E接口.e吉以太网
}
c次 = "secondary"
def f检查接口范围(self):
	v展开 = False
	if len(self.m接口.ma序号) > 1:
		for v序号 in self.m接口.ma序号[:-1]:
			if type(v序号) == range:
				v展开 = True
	self.mi范围 = type(self.m接口.ma序号[-1]) == range
	self.mi接口自动展开 = v展开
#===============================================================================
# 接口配置
#===============================================================================
class C接口配置(设备.I接口配置模式):
	def __init__(self, a父模式, a接口):
		设备.I接口配置模式.__init__(self, a父模式, a接口)
		f检查接口范围(self)
	#模式命令
	def fg进入命令(self):
		if self.mi范围:
			v命令 = 设备.C命令("interface range")
		else:
			v命令 = 设备.C命令("interface")
		v命令 += self.fg模式参数()
		return v命令
	def fg模式参数(self):
		return str(self.m接口)
	def fg删除命令(self):
		return c不 + self.fg进入命令()
	#模式
	def f模式_路由信息协议(self, a进程号 = 1, a版本 = 设备.E协议.e路由信息协议):
		return self.fg上级模式().f模式_路由信息协议(a进程号 = a进程号, a版本 = a版本, a接口 = self.m接口)
	def f模式_开放最短路径优先(self, a进程号 = 1, a版本 = 设备.E协议.e开放最短路径优先):
		return self.fg上级模式().f模式_开放最短路径优先(a进程号 = a进程号, a版本 = a版本, a接口 = self.m接口)
	def f模式_增强内部网关路由协议(self, a版本 = 设备.E协议.e网络协议4):
		return self.fg上级模式().f模式_增强内部网关路由协议(a版本 = a版本, a接口 = self.m接口)
	def f模式_中间系统到中间系统(self, a版本 = 设备.E协议.e网络协议4):
		return self.fg上级模式().f模式_中间系统到中间系统(a进程号 = a进程号, a版本 = a版本, a接口 = self.m接口)
	#显示
	def f显示_当前模式配置(self):
		self.m设备.f执行用户命令("show running-config interface " + self.fg模式参数())
	#操作
	@通用接口.A接口自动展开
	def fs开关(self, a操作 = 设备.E操作.e设置):
		v命令 = 通用实用.f生成开关命令("shutdown", c不, a操作)
		self.f执行当前模式命令(v命令)
	@通用接口.A接口自动展开
	def fs描述(self, a描述 = "", a操作 = 设备.E操作.e设置):
		v命令 = 设备.C命令("description")
		if a操作 == 设备.E操作.e删除:
			v命令.f前面添加(c不)
		elif a操作 == 设备.E操作.e重置:
			v命令.f前面添加(c默认)
		else:
			v命令 += a描述
		self.f执行当前模式命令(v命令)
	@通用接口.A接口自动展开
	def fs网络地址4(self, a地址, a操作 = 设备.E操作.e设置):
		v命令 = 设备.C命令("ip address")
		v命令 += 思科实用.f生成地址和掩码4(a地址)
		if a操作 == 设备.E操作.e设置:
			pass
		elif a操作 == 设备.E操作.e添加:
			v命令 += c次
		elif a操作 == 设备.E操作.e删除:
			v命令.f前面添加(c不)
		self.f执行当前模式命令(v命令)
	@通用接口.A接口自动展开
	def fs网络地址6(self, a地址, a操作 = 设备.E操作.e添加):
		v命令 = 设备.C命令("ipv6 address")
		v命令 += 思科实用.f生成地址和前缀长度6(a地址)
		if a操作 == 设备.E操作.e删除:
			v命令.f前面添加(c不)
		self.f执行当前模式命令(v命令)