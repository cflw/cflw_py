import ipaddress
import functools
import cflw网络设备 as 设备
import cflw网络地址 as 地址
c空序号 = -1
c空规则 = 设备.S访问控制列表规则(a允许 = False)	#拒绝所有
#名称
def f解析名称(a名称, a类型, a助手):
	v名称类型 = type(a名称)
	if v名称类型 == int:
		return a名称
	elif v名称类型 == str:
		if a名称.isdigit():
			return int(a名称)
		return a名称
	elif v名称类型 == 设备.S访问控制列表序号:
		#检查序号
		if a名称.m特定序号:
			return a名称.m特定序号
		elif a名称.m统一序号 == None:
			raise ValueError("没有序号")
		#计算特定序号
		v序号类型空 = a名称.m类型 == None
		v参数类型空 = a类型 == None
		if (not v序号类型空) and (not v参数类型空):
			raise ValueError("没有类型")
		elif v序号类型空 and v参数类型空:
			if a名称.m类型 != a类型:
				raise ValueError("类型不同")
		v类型 = a类型 if a类型 else a名称.m类型
		v特定序号 = a助手.ft特定序号(a名称.m统一序号, v类型)
		return v特定序号
	else:
		raise TypeError("无法解析的类型")
#协议
ca协议到字符串4 = {
	设备.E协议.ip: "ip",
	设备.E协议.ipv4: "ip",
	设备.E协议.ipv6: "ipv6",
	设备.E协议.tcp: "tcp",
	设备.E协议.udp: "udp",
}
ca协议到字符串6 = {
	设备.E协议.ip: "ipv6",
	设备.E协议.ipv4: "ip",
	设备.E协议.ipv6: "ipv6",
	设备.E协议.tcp: "tcp",
	设备.E协议.udp: "udp",
}
ca字符串到协议 = {
	"ip": 设备.E协议.e网络协议4,
	"ipv6": 设备.E协议.e网络协议6,
	"tcp": 设备.E协议.e传输控制协议,
	"udp": 设备.E协议.e用户数据报协议,
}
def f生成协议(a字典: dict, a协议)->str:
	v类型 = type(a协议)
	if v类型 == int:
		return str(v类型)
	elif v类型 == 设备.E协议:
		return a字典[a协议]
	elif v类型 == str:
		return a协议
	else:
		raise TypeError()
f生成协议4 = functools.partial(f生成协议, ca协议到字符串4)
f生成协议6 = functools.partial(f生成协议, ca协议到字符串6)
#动作
c允许 = "permit"
c拒绝 = "deny"
c允许元组 = (c允许, c拒绝)
def f生成允许(a元组: tuple, a允许)->str:
	if type(a允许) == str:
		if a允许 in a元组:
			return a允许
		raise ValueError()
	if a允许:
		return a元组[0]
	else:
		return a元组[1]
def f解析允许(a元组: tuple, a字符串: str)->bool:
	if a字符串 == a元组[0]:
		return True
	elif a字符串 == a元组[1]:
		return False
	else:
		raise ValueError()
#地址
def f生成地址和通配符4(a地址)->str:
	v地址 = 地址.S网络地址4.fc自动(a地址)
	return "%s %s" % (v地址.fg网络号s(), v地址.fg反掩码s())
#端口号
def f生成端口(a转换对象: 设备.I端口号到字符串, a端口)->str:
	v端口 = 设备.S端口号.fc自动(a端口)
	return v端口.ft字符串(a转换对象)
