import cflw字符串 as 字符串
import cflw网络地址 as 地址
import cflw网络设备 as 设备
import 网络设备.华为_接口 as 接口
class C接口表:
	"""敲"display interface brief"所显示的信息"""
	c标题行 = "Interface                   PHY   Protocol InUti OutUti   inErrors  outErrors"
	c接口开始 = 0
	c物理开始 = 28
	c协议开始 = 34
	c输入率 = 43
	c输出率 = 49
	c输入错误 = 58
	c输出错误 = 68
	ca列开始 = (c接口开始, c物理开始, c协议开始, c输入率, c输出率, c输入错误, c输出错误)
	c标题行长度 = len(c标题行)
	def __init__(self, a):
		v位置 = 字符串.f连续找最后(a, C接口表.c标题行, "\n")
		self.m文本 = a[v位置+1:]
	def __iter__(self):
		return self.fe行()
	def fe行(self):
		for v行 in self.m文本.split("\n"):
			if len(v行) != C接口表.c标题行长度:
				continue	#中间可能有其它东西,跳过
			v接口s, v物理s, v协议s, v输入率s, v输出率s, v输入错误s, v输出错误s = 字符串.fe按位置分割(v行, *C接口表.ca列开始)
			v接口 = 设备.S接口.fc字符串(v接口s, 接口.ca接口名称)
			v状态 = "up" in v协议s
			yield 设备.S接口表项(a接口 = v接口, a状态 = v状态)
class C网络接口表4:
	"""敲"display ip interface brief"所显示的信息"""
	c标题行 = "Interface                         IP Address/Mask      Physical   Protocol  "
	c接口开始 = 0
	c地址开始 = 34
	c物理开始 = 55
	c协议开始 = 66
	ca列开始 = (c接口开始, c地址开始, c物理开始, c协议开始)
	c标题行长度 = len(c标题行)
	def __init__(self, a):
		v位置 = 字符串.f连续找最后(a, C网络接口表4.c标题行, "\n")
		self.m文本 = a[v位置+1:]
	def __iter__(self):
		return self.fe行()
	def fe行(self):
		for v行 in self.m文本.split("\n"):
			if len(v行) != C接口表.c标题行长度:
				continue	#中间可能有其它东西,跳过
			v接口s, v地址s, v物理s, v协议s = 字符串.fe按位置分割(v行, *C网络接口表4.ca列开始)
			v接口 = 设备.S接口.fc字符串(v接口s, 接口.ca接口名称)
			if "unassigned" in v地址s:
				v地址 = None
			else:
				v地址 = 地址.S网络地址4.fc自动(v地址s)
			v状态 = "up" in v协议s
			yield 设备.S网络接口表项(a接口 = v接口, a地址 = v地址, a状态 = v状态)