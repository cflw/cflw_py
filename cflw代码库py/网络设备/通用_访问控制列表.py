import ipaddress
import functools
import cflw网络设备 as 设备
import cflw网络地址 as 地址
ca访问控制列表协议到字符串4 = {
	设备.C访问控制列表规则.E协议.ip: "ip",
	设备.C访问控制列表规则.E协议.ipv4: "ip",
	设备.C访问控制列表规则.E协议.ipv6: "ipv6",
	设备.C访问控制列表规则.E协议.tcp: "tcp",
	设备.C访问控制列表规则.E协议.udp: "udp",
}
ca访问控制列表协议到字符串6 = {
	设备.C访问控制列表规则.E协议.ip: "ipv6",
	设备.C访问控制列表规则.E协议.ipv4: "ip",
	设备.C访问控制列表规则.E协议.ipv6: "ipv6",
	设备.C访问控制列表规则.E协议.tcp: "tcp",
	设备.C访问控制列表规则.E协议.udp: "udp",
}
def f生成协议(a字典: dict, a协议)->str:
	v类型 = type(a协议)
	if v类型 == int:
		return str(v类型)
	elif v类型 == 设备.C访问控制列表规则.E协议:
		return a字典[a协议]
	elif v类型 == str:
		return a协议
	else:
		raise TypeError()
f生成协议4 = functools.partial(f生成协议, ca访问控制列表协议到字符串4)
f生成协议6 = functools.partial(f生成协议, ca访问控制列表协议到字符串6)
c允许 = "permit"
c阻止 = "deny"
c允许元组 = (c允许, c阻止)
def f生成允许(a元组: tuple, a允许)->str:
	if type(a允许) == str:
		if a允许 in a元组:
			return a允许
		raise ValueError()
	if a允许:
		return a元组[0]
	else:
		return a元组[1]
def f生成端口(a转换对象: 设备.I访问控制列表端口号到字符串, a端口)->str:
	if not a端口:
		return ""
	v类型 = type(a端口)
	if v类型 == 设备.S访问控制列表端口号:
		return a端口.ft字符串(a转换对象)
	elif v类型 == int:
		return a转换对象.f等于([a端口])
	elif v类型 == range:
		return a转换对象.f范围(a端口)
	else:
		raise TypeError("无法识别的类型")
def f生成地址和通配符4(a地址)->str:
	v类型 = type(a地址)
	if v类型 == 地址.S网络地址4:
		return "%s %s" % (a地址.fg网络号s(), a地址.fg掩码s())
	elif v类型 == ipaddress.IPv4Address:
		return "%s 0.0.0.0" % (a地址,)
	elif v类型 == ipaddress.IPv4Network:
		return "%s %s" % (a地址.network_address, a地址.hostmask)
	elif v类型 == str:
		return a地址
	else:
		raise TypeError()
def f解析允许(a元组: tuple, a字符串: str)->bool:
	if a字符串 == a元组[0]:
		return True
	elif a字符串 == a元组[1]:
		return False
	else:
		raise ValueError()