import time
import cflw网络设备 as 设备
import cflw字符串 as 字符串
import cflw网络地址 as 地址
import 网络设备.思科_接口 as 思科接口
import 网络设备.思科_基本表信息 as 思科基本表信息
#===============================================================================
# 接口表
#===============================================================================
class C接口表:
	"""show interface status
	适用于: s5750(v11.4)"""
	c接口 = 0
	c状态 = 41
	c虚拟局域网 = 51
	c双工 = 58
	c速率 = 67
	c类型 = 77	#铜还是光纤
	ca列开始 = (c接口, c状态, c虚拟局域网, c双工, c速率, c类型)
	c标题行0 = "Interface                                Status    Vlan   Duplex   Speed     Type  "
	c标题行1 = "---------------------------------------- --------  ----   -------  --------- ------"
	def __init__(self, a文本):
		v位置 = 字符串.f连续找最后(a文本, C接口表.c标题行1, "\n")
		self.m文本 = a文本[v位置+1:]
	def __iter__(self):
		return self.fe行()
	def fe行(self):
		for v行 in self.m文本.split("\n"):
			if len(v行) < 80:
				continue
			v接口s, v状态s, v虚拟局域网s, v双工s, v速率s, v类型s = 字符串.fe按位置分割(v行, *C接口表.ca列开始)
			v接口 = 思科接口.f创建接口(v接口s)
			v虚拟局域网 = int(v虚拟局域网s)
			v状态 = "up" in v状态s
			v双工 = None if "Unknown" in v双工s else "Full" in v双工s
			v速率 = None if "Unknown" in v速率s else int(v速率s[:-1])
			yield 设备.S接口表项(a接口 = v接口, a状态 = v状态, a速率 = v速率, a双工 = v双工, a虚拟局域网 = v虚拟局域网)
class C交换接口表:
	"""show interface switchport
	适用于: s5750(v11.4)"""
	c接口 = 0
	c交换 = 33	#是否交换口
	c模式 = 44	#链路类型
	c接入 = 54	#接入口的vlan
	c本征 = 61	#中继口的vlan
	c保护 = 68
	c虚拟局域网 = 78	#意义不明的列
	c列表 = 83	#意义不明的列
	ca列开始 = (c接口, c交换, c模式, c接入, c本征, c保护, c虚拟局域网, c列表)
	c标题行0 = "Interface                        Switchport Mode      Access Native Protected VLAN lists"
	c标题行1 = "-------------------------------- ---------- --------- ------ ------ --------- ----------------------"
	def __init__(self, a文本):
		v位置 = 字符串.f连续找最后(a文本, C交换接口表.c标题行1, "\n")
		self.m文本 = a文本[v位置+1:]
	def __iter__(self):
		return self.fe行()
	def fe行(self):
		for v行 in self.m文本.split("\n"):
			if len(v行) < 80:
				continue
			v接口s, v交换s, v模式s, v接入s, v本征s, v保护s, v虚拟局域网s, v列表s = 字符串.fe按位置分割(v行, *C交换接口表.ca列开始)
			v接口 = 思科接口.f创建接口(v接口s)
			v虚拟局域网 = int(v接入s)
			yield 设备.S接口表项(a接口 = v接口, a虚拟局域网 = v虚拟局域网)
#===============================================================================
# 网络接口表
#===============================================================================
class C网络接口表4:
	"""show ip interface brief
	适用于: s5750(v11.4)"""
	c接口 = 0
	c地址0 = 41
	c地址1 = 62
	c状态 = 83
	c协议 = 106
	ca列开始 = (c接口, c地址0, c地址1, c状态, c协议)
	c标题行 = "Interface                                IP-Address(Pri)      IP-Address(Sec)      Status                 Protocol "
	def __init__(self, a文本):
		v位置 = 字符串.f连续找最后(a文本, C网络接口表4.c标题行, "\n")
		self.m文本 = a文本[v位置+1:]
	def __iter__(self):
		return self.fe行()
	def fe行(self):
		for v行 in self.m文本.split("\n"):
			if len(v行) < 110:
				continue
			v接口s, v地址0s, v地址1s, v状态s, v协议s = 字符串.fe按位置分割(v行, *C网络接口表4.ca列开始)
			v接口 = 思科接口.f创建接口(v接口s)
			v地址 = 地址.S网络地址4.fc自动(v地址0s)
			v状态 = "up" in v协议s
			yield 设备.S网络接口表项(a接口 = v接口, a地址 = v地址, a状态 = v状态)
#===============================================================================
# 物理地址表
#===============================================================================
class C物理地址表:
	"""show mac-address-table
	适用于: s5750(v11.4)"""
	c虚拟局域网 = 0
	c物理地址 = 12
	c类型 = 33
	c接口 = 42
	c时间 = 73
	ca列开始 = (c虚拟局域网, c物理地址, c类型, c接口, c时间)
	c标题行0 = "Vlan        MAC Address          Type     Interface                      Time"
	c标题行1 = "----------  -------------------- -------- ------------------------------ --------------------"
	def __init__(self, a文本):
		v位置 = 字符串.f连续找最后(a文本, C物理地址表.c标题行1, "\n")
		self.m文本 = a文本[v位置+1:]
	def __iter__(self):
		return self.fe行()
	def fe行(self):
		for v行 in self.m文本.split("\n"):
			if len(v行) < 90:
				continue
			v虚拟局域网s, v物理地址s, v类型s, v接口s, v时间s = 字符串.fe按位置分割(v行, *C物理地址表.ca列开始)
			v虚拟局域网 = int(v虚拟局域网s)
			v物理地址 = 地址.S物理地址.fc字符串(v物理地址s)
			v接口 = 思科接口.f创建接口(v接口s)
			# v时间 = time.strptime("%Y-%m-%d %H:%M:%S", v时间s)	#不可用
			v类型 = 思科基本表信息.ca物理地址类型[v类型s]
			yield 设备.S物理地址表项(a地址 = v物理地址, a接口 = v接口, a虚拟局域网 = v虚拟局域网, a类型 = v类型)
#===============================================================================
# 地址解析表
#===============================================================================
class C地址解析表4:
	"""show arp
	适用于: s5750(v11.4)"""
	c协议 = 0
	c地址 = 10
	c寿命 = 27
	c硬件 = 37
	c类型 = 53
	c接口 = 60
	ca列开始 = (c协议, c地址, c寿命, c硬件, c类型, c接口)
	c标题行 = "Protocol  Address          Age(min)  Hardware        Type   Interface               "
	def __init__(self, a文本):
		v位置 = 字符串.f连续找最后(a文本, C地址解析表4.c标题行, "\n")
		self.m文本 = a文本[v位置+1:]
	def __iter__(self):
		return self.fe行()
	def fe行(self):
		for v行 in self.m文本.split("\n"):
			if len(v行) < 80:
				continue
			if "-" in v行:
				continue
			v协议s, v网络地址s, v寿命s, v物理地址s, v类型s, v接口s = 字符串.fe按位置分割(v行, *C地址解析表4.ca列开始)
			v网络地址 = 地址.S网络地址4.fc自动(v网络地址s)
			v寿命 = int(v寿命s) * 60
			v物理地址 = 地址.S物理地址.fc字符串(v物理地址s)
			v接口 = 思科接口.f创建接口(v接口s)
			yield 设备.S地址解析表项(a网络地址 = v网络地址, a物理地址 = v物理地址, a接口 = v接口, a寿命 = v寿命)
