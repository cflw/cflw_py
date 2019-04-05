import cflw网络设备 as 设备
import cflw网络地址 as 地址
import cflw字符串 as 字符串
import 网络设备.思科_接口 as 思科接口
import 网络设备.思科_基本表信息 as 思科基本表信息
#===============================================================================
# 接口表
#===============================================================================
class C交换接口表:
	"""show interface switchport brief
	适用于: sm4120(v6.6.4.1.3)"""
	c接口 = 0	#1
	c状态 = 18	#意义不明的列
	c连接 = 29
	c速率 = 35
	c双工 = 46
	vsl = 57	#意义不明的列
	c类型 = 66	#意义不明的列
	c虚拟局域网 = 75
	c描述 = 81
	ca列开始 = (c接口, c状态, c连接, c速率, c双工, vsl, c类型, c虚拟局域网, c描述)
	c标题行0 = " Interface        Status     Link  ActSpeed   ActDuplex  VSL      Type     Pvid  Desc"
	c标题行1 = " -----------------------------------------------------------------------------------------"
	t项 = 设备.S接口表项
	def __init__(self, a文本):
		v位置 = 字符串.f连续找最后(a文本, C交换接口表.c标题行1, "\n")
		self.m文本 = a文本[v位置+1:]
	def __iter__(self):
		return self.fe行()
	def fe行(self):
		for v行 in self.m文本.split("\n"):
			if len(v行) < 80:
				continue
			v接口s, v状态s, v连接s, v速率s, v双工s, v列5, v类型s, v虚拟局域网s, v描述s = 字符串.fe按位置分割(v行, *C交换接口表.ca列开始)
			v虚拟局域网 = int(v虚拟局域网s)
			v接口 = 设备.S接口.fc字符串(v接口s, 思科接口.ca接口缩写, False)
			v状态 = "Up" in v连接s
			v速率 = 0 if "Unknown" in v速率s else int(v速率s)
			v双工 = "Full" in v双工s
			yield 设备.S接口表项(a接口 = v接口, a状态 = v状态, a速率 = v速率, a双工 = v双工, a虚拟局域网 = v虚拟局域网, a描述 = v描述s)
#===============================================================================
# 网络接口表
#===============================================================================
class C网络接口表4:
	"""show ip interface brief
	适用于: sm4120(v6.6.4.1.3)"""
	c接口 = 0
	c地址 = 33
	c状态 = 49
	c协议 = 71
	c描述 = 80
	ca列开始 = (c接口, c地址, c状态, c协议, c描述)
	c标题行 = "Interface                        IP-Address      Status                Protocol Description"
	t项 = 设备.S网络接口表项
	def __init__(self, a文本):
		v位置 = 字符串.f连续找最后(a文本, C网络接口表4.c标题行, "\n")
		self.m文本 = a文本[v位置+1:]
	def __iter__(self):
		return self.fe行()
	def fe行(self):
		for v行 in self.m文本.split("\n"):
			if len(v行) < 79:
				continue
			v接口s, v地址s, v状态s, v协议s, v描述s = 字符串.fe按位置分割(v行, *C网络接口表4.ca列开始)
			v接口 = 思科接口.f创建接口(v接口s)
			v地址 = None if "unassigned" in v地址s else 地址.S网络地址4.fc地址前缀长度(v地址s, 32)
			v状态 = "up" in v协议s
			yield 设备.S网络接口表项(a接口 = v接口, a地址 = v地址, a状态 = v状态, a描述 = v描述s)
#===============================================================================
# 地址解析表
#===============================================================================
class C地址解析表4:
	"""show arp
	适用于: sm4120(v6.6.4.1.3)"""
	c协议 = 0
	c网络地址 = 10
	c寿命 = 30
	c物理地址 = 40
	c类型 = 56
	c网络口 = 64
	c交换口 = 99
	ca列开始 = (c协议, c网络地址, c寿命, c物理地址, c类型, c网络口, c交换口)
	c标题行 = "Protocol  Address             Age (min) Hardware Addr   Type    Interface                          Switchport          "
	t项 = 设备.S地址解析表项
	def __init__(self, a文本):
		v位置 = 字符串.f连续找最后(a文本, C地址解析表4.c标题行, "\n")
		self.m文本 = a文本[v位置+1:]
	def __iter__(self):
		return self.fe行()
	def fe行(self):
		for v行 in self.m文本.split("\n"):
			if len(v行) < 100:
				continue
			if "-" in v行:
				continue	#自已
			if not "Internet" in v行:
				continue	#似乎协议总是"Internet"
			v协议s, v网络地址s, v寿命s, v物理地址s, v类型s, v网络口s, v交换口s = 字符串.fe按位置分割(v行, *C地址解析表4.ca列开始)
			v网络地址 = 地址.S网络地址4.fc地址字符串(v网络地址s)
			v物理地址 = 地址.S物理地址.fc字符串(v物理地址s)
			v接口 = 思科接口.f创建接口(v交换口s)
			v寿命 = int(v寿命s) * 60	#分钟->秒
			yield 设备.S地址解析表项(a网络地址 = v网络地址, a物理地址 = v物理地址, a接口 = v接口, a寿命 = v寿命)
#===============================================================================
# 物理地址表
#===============================================================================
class C物理地址表:
	"""show mac-address all
	适用于: sm4120(v6.6.4.1.3)"""
	c虚拟局域网 = 0	#1
	c物理地址 = 10
	c类型 = 28
	c接口 = 40
	c状态 = 64
	c标志 = 76
	ca列开始 = (c虚拟局域网, c物理地址, c类型, c接口, c状态, c标志)
	c标题行0 = " VLAN          MAC           TYPE          INTERFACE             STATE       FLAG "
	c标题行1 = " ----     --------------    -------     --------------------    --------    ------"
	t项 = 设备.S物理地址表项
	def __init__(self, a文本):
		v位置 = 字符串.f连续找最后(a文本, C物理地址表.c标题行1, "\n")
		self.m文本 = a文本[v位置+1:]
	def __iter__(self):
		return self.fe行()
	def fe行(self):
		for v行 in self.m文本.split("\n"):
			if len(v行) < 80:
				continue
			v虚拟局域网s, v物理地址s, v类型s, v接口s, v状态s, v标志s = 字符串.fe按位置分割(v行, *C物理地址表.ca列开始)
			v地址 = 地址.S物理地址.fc字符串(v物理地址s)
			v接口 = 设备.S接口.fc字符串(v接口s, 思科接口.ca接口缩写, False)
			v虚拟局域网 = int(v虚拟局域网s)
			v类型 = 思科基本表信息.ca物理地址类型[v类型s]
			yield 设备.S物理地址表项(a地址 = v地址, a接口 = v接口, a虚拟局域网 = v虚拟局域网, a类型 = v类型)