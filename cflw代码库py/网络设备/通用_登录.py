import cflw网络设备 as 设备
def f生成范围(a登录, a范围):
	return " ".join(f生成范围元组(a登录, a范围))
def f生成范围元组(a登录, a范围):
	if a登录 == 设备.E登录方式.e控制台:
		return (0,)
	elif a登录 == 设备.E登录方式.e虚拟终端:
		v范围类型 = type(a范围)
		if v范围类型 == int:
			return (a范围,)
		elif v范围类型 == range:
			return (a范围.start, a范围.stop - 1)
		else:
			return (0, 4)
	else:
		return (0,)
