import cflw网络设备 as 设备
import cflw字符串 as 字符串
import cflw网络地址 as 地址
import 网络设备.思科_接口 as 接口
#===============================================================================
# 物理地址表
#===============================================================================
ca物理地址类型 = {
	"STATIC": 设备.E物理地址类型.e静态,
	"DYNAMIC": 设备.E物理地址类型.e动态,
}
class C物理地址表:
	"""敲"show mac address-table"所显示的信息"""
	c虚拟局域网开始 = 0
	c物理地址开始 = 8
	c物理地址结束 = 22
	c类型开始 = 26
	c端口开始 = 38
	ca列开始 = (c虚拟局域网开始, c物理地址开始, c类型开始, c端口开始)
	def __init__(self, a):
		self.m字符串 = str(a)
	def __iter__(self):
		return self.fe行()
	def fe行(self):	#把字符串转成数据
		for v行 in 字符串.fe分割(self.m字符串, '\n'):
			if "CPU" in v行:
				continue
			if not "." in v行:	#物理地址用.分隔
				continue
			v虚拟局域网s, v地址s, v类型s, v接口s = 字符串.fe按位置分割(v行, *C物理地址表.ca列开始)
			v虚拟局域网 = int(v虚拟局域网s)
			v接口 = 设备.S接口.fc字符串(v接口s, ca接口缩写, False)
			v地址 = 地址.S物理地址.fc字符串(v地址s)
			v类型 = ca物理地址类型[str.strip(v类型s)]
			yield 设备.S物理地址表项(a地址 = v地址, a接口 = v接口, a虚拟局域网 = v虚拟局域网, a类型 = v类型)
#===============================================================================
# 网络接口表
#===============================================================================
class C网络接口表4:
	"""敲"show ip interface brief"所显示的信息"""
	c接口开始 = 0
	c地址开始 = 23
	c好开始 = 39
	c方法开始 = 43
	c状态开始 = 50
	c协议开始 = 72
	ca列开始 = (c接口开始, c地址开始, c好开始, c方法开始, c状态开始, c协议开始)
	def __init__(self, a):
		self.m字符串 = str(a)
	def __iter__(self):
		return self.fe行()
	def fe行(self):
		for v行 in 字符串.fe分割(self.m字符串, "\n"):
			if not "YES" in v行:
				continue
			#接口
			v接口s = v行[C网络接口表4.c接口开始 : C网络接口表4.c地址开始]
			v接口 = 设备.S接口.fc字符串(v接口s, 接口.ca接口名称)
			#地址
			v地址s = v行[C网络接口表4.c地址开始 : C网络接口表4.c好开始]
			if "unassigned" in v地址s:
				v地址 = None
			else:
				v地址 = 地址.S网络地址4.fc地址前缀长度(v地址s, 32)
			#状态
			v状态s = v行[C网络接口表4.c状态开始 : C网络接口表4.c协议开始]
			v状态 = "up" in v状态s
			#退回
			yield 设备.S网络接口表项(a接口 = v接口, a地址 = v地址, a状态 = v状态)
class C网络接口表6:
	"""敲"show ipv6 interface brief"所显示的信息"""
	c接口开始 = 0
	c状态开始 = 23
	c地址开始 = 4
	def __init__(self, a):
		self.m字符串 = str(a)
	def __iter__(self):
		return self.fe行()
	def fe行(self):
		v项 = None
		for v行 in 字符串.fe分割(self.m字符串, "\n"):
			if "/" in v行:	#接口行包含斜杠
				if v项:
					yield v项
				v接口s, v状态s, v协议s  = 字符串.fe按字符分割(v行, "[", "/", "]")
				v接口 = 设备.S接口.fc字符串(v接口s, 接口.ca接口名称)
				v状态 = "up" in v状态s
				v项 = 设备.S网络接口表项(a接口 = v接口, a地址 = [], a状态 = v状态)
			elif v项:	#地址行
				v地址s = v行.strip()
				if "unassigned" in v地址s:
					pass
				else:
					v地址 = 地址.S网络地址6.fc地址前缀长度(v地址s, 128)
					v项.m地址.append(v地址)
			else:
				raise RuntimeError("迷之错误")
		yield v项
