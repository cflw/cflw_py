import cflw字符串 as 字符串
import cflw网络地址 as 地址
import cflw网络设备 as 设备
import 网络设备.中兴_接口 as 接口
#===============================================================================
# 网络接口表
#===============================================================================
class C网络接口表:
	"""show ip interface brief
	用于zxr10 m6000"""
	c接口 = 0
	c地址 = 32
	c掩码 = 48
	c管理 = 64
	c物理 = 70
	c协议 = 75
	ca列开始 = (c接口, c地址, c掩码, c管理, c物理, c协议)
	c标题行 = "Interface                       IP-Address      Mask            Admin Phy  Prot"
	def __init__(self, a):
		v开始位置 = 字符串.f连续找最后(a, C网络接口表.c标题行, "\n") + 1
		self.m字符串 = a[v开始位置:]
	def __iter__(self):
		return self.fe行()
	def fe行(self):
		for v行 in self.m字符串.split("\n"):
			if len(v行) < C网络接口表.c协议:
				continue
			elif v行[C网络接口表.c地址-1] != " ":
				continue
			elif v行[C网络接口表.c协议-1] != " ":
				continue
			v接口s, v地址s, v掩码s, v管理s, v物理s, v协议s = 字符串.fe按位置分割(v行, *C网络接口表.ca列开始)
			v接口 = 接口.f创建接口m6000(v接口s)
			if "unassigned" in v地址s:
				v地址 = None
			else:
				v地址 = 地址.S网络地址4.fc地址掩码(v地址s, v掩码s)
			v状态 = "up" in v协议s
			yield 设备.S网络接口表项(a接口 = v接口, a地址 = v地址, a状态 = v状态)
#===============================================================================
# 接口表
#===============================================================================
class C接口表:
	"""show interface brief
	用于zxr10 m6000"""
	c接口 = 0
	c光电属性 = 15
	c模式 = 26
	c速率 = 39
	c管理 = 46
	c物理 = 52
	c协议 = 58
	c描述 = 64
	ca列开始 = (c接口, c光电属性, c模式, c速率, c管理, c物理, c协议, c描述)
	c标题行 = "Interface      Portattribute  Mode  BW(Mbps)  Admin Phy   Prot  Description"
	def __init__(self, a: str):
		v开始位置 = 字符串.f连续找最后(a, C接口表.c标题行, "\n") + 1
		self.m字符串 = a[v开始位置:]
	def __iter__(self):
		return self.fe行()
	def fe行(self):
		for v行 in self.m字符串.split("\n"):
			if len(v行) < C接口表.c描述:	#太少,跳过
				continue
			elif v行[C接口表.c光电属性-1] != " ":
				continue
			elif v行[C接口表.c模式-1] != " ":
				continue
			v接口s, v光电属性s, v模式s, v速率s, v管理s, v物理s, v协议s, v描述s = 字符串.fe按位置分割(v行, *C接口表.ca列开始)
			v接口 = 接口.f创建接口m6000(v接口s)
			v状态 = "up" in v协议s
			yield 设备.S接口表项(a接口 = v接口, a状态 = v状态, a描述 = v描述s)
#===============================================================================
# 地址解析表
#===============================================================================
class C地址解析表:
	"""show arp
	用于zxr10 m6000"""
	c网络地址 = 0
	c寿命 = 16
	c物理地址 = 25
	c接口 =  40
	c外部虚拟局域网 = 53
	c内部虚拟局域网 = 60
	c子接口 = 67
	ca列开始 = (c网络地址, c寿命, c物理地址, c接口, c外部虚拟局域网, c内部虚拟局域网, c子接口)
	c标题行0 = "IP                       Hardware                    Exter  Inter  Sub"
	c标题行1 = "Address         Age      Address        Interface    VlanID VlanID Interface"
	def __init__(self, a):
		v开始位置 = 字符串.f连续找最后(a, C地址解析表.c标题行1, "-", "\n") + 1
		self.m字符串 = a[v开始位置:]
	def __iter__(self):
		return self.fe行()
	def fe行(self):
		for v行 in self.m字符串.split("\n"):
			if len(v行) < C地址解析表.c子接口:
				continue
			elif v行[C地址解析表.c寿命-1] != " ":
				continue
			elif v行[C地址解析表.c子接口-1] != " ":
				continue
			v网络地址s, v寿命s, v物理地址s, v接口s, v外部虚拟局域网s, v内部虚拟局域网s, v子接口s = 字符串.fe按位置分割(v行, *C地址解析表.ca列开始)
			if "H" in v寿命s:
				continue
			elif "N/A" in v子接口s:
				continue
			#解析
			v网络地址 = 地址.S网络地址4.fc地址前缀长度(v网络地址s, 32)
			v物理地址 = 地址.S物理地址.fc字符串(v物理地址s)
			v接口 = 接口.f创建接口m6000(v子接口s)
			v时, v分, v秒 = (int(x) for x in v寿命s.split(":"))
			v总秒 = v时 * 3600 + v分 * 60 + v秒
			yield 设备.S地址解析表项(a网络地址 = v网络地址, a物理地址 = v物理地址, a接口 = v接口, a寿命 = v总秒)