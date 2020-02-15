import pysnmp.hlapi as 接口	#pysnmp
import pysnmp.proto.rfc1902 as 类型
from . import cflw简单网管 as 简单网管
class C简单网管(简单网管.I简单网管):
	c连接特性 = 0x0004
	def __init__(self, a主机, a团体字 = "public", a版本 = 2, a端口号 = 161):
		self.m目标 = 接口.UdpTransportTarget((a主机, a端口号))
		self.m团体字 = 接口.CommunityData(a团体字, mpModel=0)
		self.m版本 = a版本
		self.m引擎 = 接口.SnmpEngine()
		self.m上下文 = 接口.ContextData()
	def fg获取命令(self, a对象标识符):
		v对象标识符 = 接口.ObjectType(接口.ObjectIdentity(a对象标识符))
		v命令 = 接口.getCmd(self.m引擎, self.m团体字, self.m目标, self.m上下文, v对象标识符)
		return v命令
	def fg遍历命令(self, a对象标识符):
		v对象标识符 = fc对象标识符(a对象标识符)
		v命令 = 接口.nextCmd(self.m引擎, self.m团体字, self.m目标, self.m上下文, v对象标识符)
		return v命令
	def f获取(self, a对象标识符):
		v命令 = self.fg获取命令(a对象标识符)
		v错误指示, v错误状态, v错误索引, va绑定变量 = next(v命令)
		return f取变量值(va绑定变量[0])
	def f遍历(self, a对象标识符):
		v命令 = self.fg遍历命令(a对象标识符)
		while v命令:
			v错误指示, v错误状态, v错误索引, va绑定变量 = next(v命令)
			yield f取变量值(va绑定变量[0])
def fc对象标识符(a对象标识符):
	return 接口.ObjectType(接口.ObjectIdentity(a对象标识符))
def f取变量值(a绑定变量):
	"""自动转换成python内置类型"""
	v变量 = a绑定变量[1]
	v类型 = type(a绑定变量[1])
	if v类型 in (类型.OctetString, 类型.OctetString):	#字符串
		return str(v变量)
	elif v类型 in (类型.Integer, 类型.Integer32, 类型.Counter32, 类型.Counter64, 类型.Unsigned32, 类型.Gauge32):	#整数
		return int(v变量)
	elif v类型 == 类型.Null:	#空
		return None
	else:	#默认处理
		return str(a绑定变量[1])