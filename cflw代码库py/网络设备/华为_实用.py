import cflw网络地址 as 地址
import cflw网络设备 as 设备
def f生成接口范围(a接口: 设备.S接口):
	"""如果不是范围,返回接口字符串.
	如果是范围,返回以"to"连接的接口字符串"""
	if a接口.fi范围():	#是范围
		if not a接口.fi只有末尾序号是范围():
			raise 设备.X接口格式(a接口)
		v头接口 = a接口.fg头接口()
		return "%s %s to %s" % (v头接口.fg名称(), v头接口.fg序号字符串(), a接口.fg尾接口().fg序号字符串())
	else:	#不是范围
		return str(a接口)
def f生成地址和前缀长度4(a地址):
	v地址 = 地址.S网络地址4.fc自动(a地址)
	return "%s %d" % (v地址.fg地址s(), v地址.fg前缀长度())
def f生成虚拟局域网范围(a虚拟局域网):
	if type(a虚拟局域网) == range:
		return "%d to %d" % (a虚拟局域网.start, a虚拟局域网.stop - 1)
	else:
		return str(a虚拟局域网)
