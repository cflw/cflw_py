import cflw网络地址 as 地址
def f解析地址4(a行):
	v地址 = 地址.c网络地址4正则.search(a行)
	if not v地址:
		return None
	v掩码 = 地址.c网络地址4正则.search(a行, v地址.endpos)
	if not v掩码:
		return None
	return 地址.S网络地址4.fc地址掩码(v地址[0], v掩码[0])