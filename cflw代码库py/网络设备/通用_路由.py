import ipaddress
import cflw网络地址 as 地址
import cflw网络设备 as 设备
#===============================================================================
# 路由版本
#===============================================================================
ca版本字符串 = {
	"ip": 设备.E协议.e网络协议4,
	"ipv4": 设备.E协议.e网络协议4,
	"ipv6": 设备.E协议.e网络协议6,
	"rip": 设备.E协议.e路由信息协议,
	"ripng": 设备.E协议.e下一代路由信息协议,
	"ospf": 设备.E协议.e开放最短路径优先,
	"ospfv2": 设备.E协议.e开放最短路径优先2,
	"ospfv3": 设备.E协议.e开放最短路径优先3,
	"eigrp": 设备.E协议.e增强内部网关路由协议,
	"isis": 设备.E协议.e中间系统到中间系统,
	"bgp": 设备.E协议.e边界网关协议
}
ca版本整数_网络协议 = {
	4: 设备.E协议.e网络协议4,
	6: 设备.E协议.e网络协议6
}
ca版本整数_路由信息协议 = {
	1: 设备.E协议.e路由信息协议,
	2: 设备.E协议.e路由信息协议,
	3: 设备.E协议.e下一代路由信息协议
}
ca版本整数_开放最短路径优先 = {
	1: 设备.E协议.e开放最短路径优先,
	2: 设备.E协议.e开放最短路径优先2,
	3: 设备.E协议.e开放最短路径优先3
}
ca版本转换_网络协议到开放最短路径优先 = {
	设备.E协议.e网络协议4: 设备.E协议.e开放最短路径优先,
	设备.E协议.e网络协议6: 设备.E协议.e开放最短路径优先3
}
ca版本转换_增强内部网关路由协议到网络协议 = {
	设备.E协议.e增强内部网关路由协议: 设备.E协议.e网络协议4
}
def f解析版本(a, aa版本整数字典):	#返回协议
	"返回 E协议 值"
	if isinstance(a, 设备.E协议):
		return a
	v类型 = type(a)
	if v类型 == int:
		return aa版本整数字典[a]
	elif v类型 == str:
		return ca版本字符串[a]
	else:
		raise TypeError("无法解析的类型")
def f解析网络协议版本(a):
	return f解析版本(a, ca版本整数_网络协议)
def f解析路由信息协议版本(a):
	return f解析版本(a, ca版本整数_路由信息协议)
def f解析开放最短路径优先版本(a):
	return f解析版本(a, ca版本整数_开放最短路径优先)
#===============================================================================
# ospf
#===============================================================================
c开放最短路径优先区域范围 = range(0, 2 ** 32)
def f解析开放最短路径优先区域(a区域, ai地址格式 = False):
	def f整数(a区域1):
		v区域 = int(a区域1)
		if not v区域 in c开放最短路径优先区域范围:
			raise ValueError("a区域 超出范围,应该在0~4294967295之间")
		return v区域
	v类型 = type(a区域)
	if v类型 == int:
		return f整数(a区域)
	elif v类型0 in (ipaddress.IPv4Network, ipaddress.IPv4Interface):
		return f整数(a区域.ip)
	elif v类型0 == ipaddress.IPv4Address:
		return f整数(a区域)
	elif v类型0 == 地址.S网络地址4:
		return a区域.fg地址i()
	elif v类型 == str:
		if a区域.count('.') == 3:	#ipv4
			return f整数(ipaddress.IPv4Address(a区域))
		elif a区域.isdigit():
			return f整数(a区域)
		else:
			raise ValueError("无法解析的字符串")
	else:	#无法识别
		raise TypeError("无法解析的类型")
