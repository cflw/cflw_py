import cflw网络设备 as 设备
import cflw字符串 as 字符串
import cflw网络地址 as 地址
import 网络设备.华三_接口 as 接口
import 网络设备.通用_实用 as 通用实用
#===============================================================================
# 接口表
#===============================================================================
class C接口表r4:
	"""display interface brief
	适用于: 路由器"""
	c接口 = 0
	c链路 = 21
	c协议 = 26
	c地址 = 35
	c描述 = 51
	ca列开始 = (c接口, c链路, c协议, c地址, c描述)
	c标题行 = "Interface            Link Protocol Primary IP      Description"
	def __init__(self, a文本):
		v位置 = 字符串.f连续找最后(a文本, C接口表r4.c标题行, "\n")
		self.m文本 = a文本[v位置+1:]
	def __iter__(self):
		return self.fe行()
	def fe行(self):
		for v行 in self.m文本.split("\n"):
			if len(v行) < 50:
				continue
			v接口s, v链路s, v协议s, v地址s, v描述s = 字符串.fe按位置分割(v行, *C接口表r4.ca列开始)
			v接口 = 设备.S接口.fc字符串(v接口s, 接口.ca接口缩写, False)
			v状态 = v协议s == "UP"
			yield 设备.S接口表项(a接口 = v接口, a状态 = v状态, a描述 = v描述s)
class C接口表s:
	"""display interface brief
	适用于: 交换机"""
	c接口 = 0
	c链路 = 21
	c速率 = 26
	c双工 = 34
	c类型 = 41
	c虚拟局域网 = 46
	c描述 = 51
	ca列开始 = (c接口, c链路, c速率, c双工, c类型, c虚拟局域网, c描述)
	c标题行 = "Interface            Link Speed   Duplex Type PVID Description"
	def __init__(self, a文本):
		v位置 = 字符串.f连续找最后(a文本, C接口表s.c标题行, "\n")
		self.m文本 = a文本[v位置+1:]
	def __iter__(self):
		return self.fe行()
	def fe行(self):
		for v行 in self.m文本.split("\n"):
			if len(v行) < 50:
				continue
			v接口s, v链路s, v速率s, v双工s, v类型s, v虚拟局域网s, v描述s = 字符串.fe按位置分割(v行, *C接口表s.ca列开始)
			v接口 = 设备.S接口.fc字符串(v接口s, 接口.ca接口缩写, False)
			v状态 = v链路s == "UP"
			v速率 = 通用实用.f解析速率(v速率s)
			v双工 = v双工s == "F"
			v虚拟局域网 = int(v虚拟局域网s)
			yield 设备.S接口表项(a接口 = v接口, a状态 = v状态, a速率 = v速率, a双工 = v双工, a虚拟局域网 = v虚拟局域网, a描述 = v描述s)
#===============================================================================
# 网络接口表
#===============================================================================
class C网络接口表4:
	"""display ip interface brief
	适用于:msr36系列"""
	c接口 = 0
	c物理 = 25
	c协议 = 34
	c地址 = 43
	c描述 = 59
	ca列开始 = (c接口, c物理, c协议, c地址, c描述)
	c标题行 = "Interface                Physical Protocol IP Address      Description"
	def __init__(self, a文本):
		v位置 = 字符串.f连续找最后(a文本, C网络接口表4.c标题行, "\n")
		self.m文本 = a文本[v位置+1:]
	def __iter__(self):
		return self.fe行()
	def fe行(self):
		for v行 in self.m文本.split("\n"):
			if len(v行) < 50:
				continue
			v接口s, v物理s, v协议s, v地址s, v描述s = 字符串.fe按位置分割(v行, *C网络接口表4.ca列开始)
			v接口 = 设备.S接口.fc字符串(v接口s, 接口.ca接口缩写, False)
			if v地址s == "--":
				v地址 = None
			else:
				v地址 = 地址.S网络地址4.fc自动(v地址s)
			v状态 = v协议s == "UP"
			yield 设备.S网络接口表项(a接口 = v接口, a地址 = v地址, a状态 = v状态, a描述 = v描述s)