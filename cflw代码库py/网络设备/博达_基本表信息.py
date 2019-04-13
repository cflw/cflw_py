import re
import cflw网络地址 as 地址
import cflw字符串 as 字符串
import cflw网络设备 as 设备
import 网络设备.博达_接口 as 接口
#===============================================================================
# 接口表
#===============================================================================
class C接口表:
	"""show interface brief
	适用于: s3956(v2.2.0B)"""
	c标题行 = "Port   Description    Status    Vlan        Duplex   Speed    Type"
	c接口 = 0
	c描述 = 7
	c状态 = 22
	c虚拟局域网 = 32
	c双工 = 44
	c速率 = 53
	c类型 = 62
	ca列开始 = (c接口, c描述, c状态, c虚拟局域网, c双工, c速率, c类型)
	def __init__(self, a文本):
		v位置 = 字符串.f连续找最后(a文本, C接口表.c标题行, "\n")
		self.m文本 = a文本[v位置+1:]
	def __iter__(self):
		return self.fe行()
	def fe行(self):
		for v行 in self.m文本.split("\n"):
			if len(v行) < 44:
				continue	#过短
			if v行[C接口表.c描述-1] != " ":
				continue
			if v行[C接口表.c状态-1] != " ":
				continue
			if v行[C接口表.c虚拟局域网-1] != " ":
				continue
			v接口s, v描述s, v状态s, v虚拟局域网s, v双工s, v速率s, v类型s = 字符串.fe按位置分割(v行, *C接口表.ca列开始)
			v接口 = 设备.S接口.fc字符串(v接口s, 接口.ca接口缩写, ai字典字符串在右 = False)
			v状态 = "up" in v状态s
			yield 设备.S接口表项(a接口 = v接口, a状态 = v状态, a描述 = v描述s)
#===============================================================================
# 网络接口表
#===============================================================================
class C网络接口表4:
	"""show ip interface brief
	适用于: s3956(v2.2.0B)"""
	c标题行 = "Interface                  IP-Address      Method Protocol-Status"
	c接口 = 0
	c地址 = 27
	c方法 = 43
	c协议状态 = 50
	ca列开始 = (c接口, c地址, c方法, c协议状态)
	def __init__(self, a文本):
		v位置 = 字符串.f连续找最后(a文本, C网络接口表4.c标题行, "\n")
		self.m文本 = a文本[v位置+1:]
	def __iter__(self):
		return self.fe行()
	def fe行(self):
		for v行 in self.m文本.split("\n"):
			if len(v行) < 54:
				continue	#过短
			v接口s, v地址s, v方法s, v协议s = 字符串.fe按位置分割(v行, *C网络接口表4.ca列开始)
			v接口 = 设备.S接口.fc字符串(v接口s, 接口.ca接口名称)
			if "unassigned" in v地址s:
				v地址 = None
			else:
				v地址 = 地址.S网络地址4.fc自动(v地址s)
			v状态 = "up" in v协议s
			yield 设备.S网络接口表项(a接口 = v接口, a地址 = v地址, a状态 = v状态)
#===============================================================================
# 物理地址表
#===============================================================================
ca物理地址类型 = {
	"STATIC": 设备.E物理地址类型.e静态,
	"DYNAMIC": 设备.E物理地址类型.e动态,
}
class C物理地址表:
	"""show mac address-table
	适用于: s3956(v2.2.0B)"""
	c标题行0 = "Vlan    Mac Address       Type       Ports"
	c标题行1 = "----    -----------       ----       -----"
	c虚拟局域网 = 0
	c地址 = 8
	c类型 = 26
	c端口 = 37
	ca列开始 = (c虚拟局域网, c地址, c类型, c端口)
	def __init__(self, a文本):
		v位置 = 字符串.f连续找最后(a文本, C物理地址表.c标题行0, C物理地址表.c标题行1, "\n")
		self.m文本 = a文本[v位置+1:]
	def __iter__(self):
		return self.fe行()
	def fe行(self):
		for v行 in self.m文本.split("\n"):
			if len(v行) < 41:
				continue	#过短
			v虚拟局域网s, v地址s, v类型s, v端口s = 字符串.fe按位置分割(v行, *C物理地址表.ca列开始)
			v虚拟局域网 = int(v虚拟局域网s)
			v地址 = 地址.S物理地址.fc字符串(v地址s)
			v接口 = 设备.S接口.fc字符串(v端口s, 接口.ca接口缩写, ai字典字符串在右 = False)
			v类型 = ca物理地址类型[str.strip(v类型s)]
			yield 设备.S物理地址表项(a地址 = v地址, a接口 = v接口, a虚拟局域网 = v虚拟局域网, a类型 = v类型)
#===============================================================================
# 地址解析表
#===============================================================================
class C地址解析表:
	"""show arp
	适用于: s3956(v2.2.0B)"""
	c标题行 = "Protocol  Address         Age(min)  Hardware  Address  Type   Interface"
	c协议 = 0
	c网络地址 = 10
	c寿命 = 26
	c物理地址 = 36
	c类型 = 55
	c接口 = 62
	ca列开始 = (c协议, c网络地址, c寿命, c物理地址, c类型, c接口)
	c接口正则 = re.compile(r"\((.+)\)")
	def __init__(self, a文本):
		v位置 = 字符串.f连续找最后(a文本, C地址解析表.c标题行, "\n")
		self.m文本 = a文本[v位置+1:]
	def __iter__(self):
		return self.fe行()
	def fe行(self):
		for v行 in self.m文本.split("\n"):
			if len(v行) < 66:
				continue	#过短
			if "-" in v行:
				continue	#没有寿命,本机地址,跳过
			if v行[C地址解析表.c网络地址-1] != " ":
				continue
			if v行[C地址解析表.c寿命-1] != " ":
				continue
			if v行[C地址解析表.c物理地址-1] != " ":
				continue
			v协议s, v网络地址s, v寿命s, v物理地址s, v类型s, v接口0 = 字符串.fe按位置分割(v行, *C地址解析表.ca列开始)
			v网络地址 = 地址.S网络地址4.fc自动(v网络地址s)
			v物理地址 = 地址.S物理地址.fc字符串(v物理地址s)
			v接口1 = C地址解析表.c接口正则.search(v接口0)[1]
			v接口 = 设备.S接口.fc字符串(v接口1, 接口.ca接口缩写, ai字典字符串在右 = False)
			v寿命 = int(v寿命s) * 60
			yield 设备.S地址解析表项(a网络地址 = v网络地址, a物理地址 = v物理地址, a接口 = v接口, a寿命 = v寿命)