import pysnmp.hlapi as 接口	#pysnmp
import pysnmp.proto.rfc1902 as 类型
import pysnmp.proto.rfc1905 as rfc1905
from . import cflw简单网管 as 简单网管
#===============================================================================
# 工具
#===============================================================================
def fc对象标识符(a标识, a值 = rfc1905.unSpecified):
	return 接口.ObjectType(接口.ObjectIdentity(str(a标识)), a值)
def fc通知标识符(a标识, aa值 = {}):
	return 接口.NotificationType(接口.objectIdentity(a标识), aa值.keys(), aa值)
def ft自动(a绑定变量1):
	"""自动转换成python内置类型"""
	v类型 = type(a绑定变量1)
	if v类型 in (类型.OctetString, 类型.OctetString):	#八进制字符串
		return str(a绑定变量1)
	elif v类型 in (类型.Integer, 类型.Integer32, 类型.Counter32, 类型.Counter64, 类型.Unsigned32, 类型.Gauge32):	#整数
		return int(a绑定变量1)
	elif v类型 == 类型.IpAddress:	#网络地址4
		return bytes(a绑定变量1)
	elif v类型 == 类型.Null:	#空
		return None
	else:	#默认处理
		return str(a绑定变量1)
def ft类型(at类型, a绑定变量1):
	if at类型:
		return at类型(a绑定变量1)
	return ft自动(a绑定变量1)
def Ft类型(at类型):
	if at类型:
		return at类型
	return ft自动
def fg对象标识符(a绑定变量0):
	return 简单网管.S对象标识符.fc字符串(str(a绑定变量0))
#===============================================================================
# 连接
#===============================================================================
class C简单网管(简单网管.I简单网管):
	c连接特性 = 0x0004
	def __init__(self, a主机, a团体字 = "public", a版本 = 2, a端口号 = 161):
		self.m目标 = 接口.UdpTransportTarget((a主机, a端口号))
		v模型 = 1 if a版本 == 2 else 0	#版本
		self.m团体字 = 接口.CommunityData(a团体字, mpModel = v模型)
		self.m版本 = a版本
		self.m引擎 = 接口.SnmpEngine()
		self.m上下文 = 接口.ContextData()
	def fc命令(self, af命令, a标识, a值 = rfc1905.unSpecified):
		v标识 = fc对象标识符(a标识, a值)
		v命令 = af命令(self.m引擎, self.m团体字, self.m目标, self.m上下文, v标识)
		return v命令
	def fc通知(self, af通知, a标识, aa值 = {}):
		v标识 = fc通知标识符(a标识, a值)
		v通知 = af通知(self.m引擎, self.m团体字, self.m目标, self.m上下文, "trap", v标识)
		return v通知
	def f获取(self, a标识, at类型 = ft自动):
		v命令 = self.fc命令(接口.getCmd, a标识)
		v错误指示, v错误状态, v错误索引, va绑定变量 = next(v命令)
		return ft类型(at类型, va绑定变量[0][1])
	def f遍历(self, a开始, a结束 = None, at类型 = ft自动):
		v开始 = 简单网管.S对象标识符.fc自动(a开始)
		v命令 = self.fc命令(接口.nextCmd, v开始)
		v结束 = 简单网管.S对象标识符.fc自动(a结束) if a结束 else v开始.f末尾加一()
		vt类型 = Ft类型(at类型)
		for v错误指示, v错误状态, v错误索引, va绑定变量 in v命令:	#下一个标识只有获取了才知道，所以结束了也要再获取一次
			v绑定变量 = va绑定变量[0]
			v当前 = fg对象标识符(v绑定变量[0])
			if v当前 >= v结束:
				break
			yield vt类型(v绑定变量[1])
	def f设置(self, a标识, a值, at类型 = ft自动):
		v命令 = self.fc命令(接口.setCmd, a标识, a值)
		v错误指示, v错误状态, v错误索引, va绑定变量 = next(v命令)
		return ft类型(at类型, va绑定变量[0][1])
	def f陷阱(self, a标识, a值, at类型 = ft自动):
		v通知 = self.fc通知(接口.sendNotification, a标识, a值)
		v错误指示, v错误状态, v错误索引, va绑定变量 = next(v通知)
		return ft类型(at类型, va绑定变量[0][1])