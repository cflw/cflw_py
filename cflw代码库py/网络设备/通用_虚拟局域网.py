c虚拟局域网范围 = range(1, 4095)	#可用范围
def f生成一个(a虚拟局域网):
	v类型 = type(a虚拟局域网)
	if v类型 == str:
		if not a虚拟局域网.isdigit():
			raise ValueError("a虚拟局域网 必须是数字")
		v数字 = int(a虚拟局域网)
		if not fi范围内(v数字):
			raise ValueError("a虚拟局域网 超出范围")
		return str(v数字)
	elif v类型 == int:
		if not fi范围内(a虚拟局域网):
			raise ValueError("a虚拟局域网 超出范围")
		return str(a虚拟局域网)
	else:
		raise TypeError("无法识别的类型")
def fi范围内(a虚拟局域网: int):
	return a虚拟局域网 in c虚拟局域网范围