import enum
import time
import cflw网络设备 as 设备
import cflw网络连接 as 连接
import cflw字符串 as 字符串
#锐捷基础
from 网络设备.思科_常量 import *
import 网络设备.通用_实用 as 通用实用
import 网络设备.思科_接口 as 接口
import 网络设备.锐捷_启动 as 启动
import 网络设备.锐捷_基本表信息 as 基本表信息
#路由
import 网络设备.思科_静态路由 as 静态路由
import 网络设备.思科_路由信息协议 as 路由信息协议
import 网络设备.思科_开放最短路径优先 as 开放最短路径优先
#其它
import 网络设备.通用_访问控制列表 as 通用访问列表
import 网络设备.思科_访问控制列表 as 访问控制列表
#===============================================================================
# 工厂
#===============================================================================
class E型号(enum.IntEnum):
	s5750 = 5750
def f创建设备(a连接, a型号, a版本 = 0):
	return C设备(a连接, a型号, a版本)
#===============================================================================
# 设备
#===============================================================================
class C设备(设备.I设备):
	"""适用于: s5750(v11.4)"""
	def __init__(self, a连接, a型号, a版本):
		设备.I设备.__init__(self)
		if isinstance(a连接, 连接.I连接):
			self.m连接 = a连接
			self.m连接.fs编码("gb2312")
		else:
			raise TypeError("a连接 必须是 I连接 类型")
		self.m型号 = a型号
		self.m版本 = a版本
		self.fs自动换页("--More--")
	def f输入_结束符(self):	#ctrl+c
		self.f输入(c结束符)
	def f执行显示命令(self, a命令, a自动换页 = True):
		v命令 = str(a命令)
		v输出 = 设备.I设备.f执行显示命令(self, a命令 = v命令, a自动换页 = a自动换页)
		v输出 = v输出.replace("\r\n", "\n")
		v输出 = 通用实用.f去头尾行(v输出)
		# if v输出.count("\n") < 10:	#输出行数太少,检测是否有异常
		# 	self.f检测命令异常(v输出)
		return v输出
	#动作
	def f退出(self):
		self.f执行命令("exit")
	#模式
	def f模式_用户(self):
		v模式 = C用户模式(self)
		return v模式
	def f模式_启动(self):
		if self.m版本 < 10.4:
			return 启动.C启动v10(self)
		elif self.m版本 < 11:
			return 启动.C启动v1042(self)
		elif self.m版本 < 12:
			return 启动.C启动v11(self)
		else:
			return NotImplementedError("不支持的版本")
#===============================================================================
# 用户模式
#===============================================================================
class C用户模式(设备.I用户模式):
	"""适用于: s5750(v11.4)"""
	def __init__(self, a):
		设备.I用户模式.__init__(self, a)
	#模式
	def f事件_进入模式(self):
		self.m设备.f刷新()
		self.m设备.f输入_结束符()
		self.m设备.f输入_回车(-1, 5)
	def f模式_全局配置(self):
		return C全局配置(self)
	#显示
	def f显示_启动配置(self):
		v输出 = self.m设备.f执行显示命令("show startup-config")
		return v输出
	def f显示_当前配置(self):
		v输出 = self.m设备.f执行显示命令("show running-config")
		return v输出
	def f显示_时间(self):
		v命令 = "show clock"
		v输出 = self.m设备.f执行显示命令(v命令)	#09:22:03 beijing Thu, Apr  4, 2019
		#解析
		v空格位置 = 字符串.f全部找(v输出, " ")
		v行结束 = v输出.find("\n")
		if v行结束 > 0:	#如果有换行符,截取到行结束
			v输出 = v输出[0 : v空格位置[0]] + v输出[v空格位置[1] : v行结束]
		else:	#如果没有换行符,截取到字符串结束
			v输出 = v输出[0 : v空格位置[0]] + v输出[v空格位置[1]:]	#09:22:03 Thu, Apr  4, 2019
		v时间 = time.strptime(v输出, "%H:%M:%S %a, %b %d, %Y")
		return v时间
	def f显示_设备名称(self):
		v命令 = "show running-config | include hostname"
		v输出 = self.m设备.f执行显示命令(v命令)
		return v输出[9:]
	#显示具体
	def f显示_接口表(self):
		v命令 = "show interface status"
		v输出 = self.m设备.f执行显示命令(v命令)
		return 基本表信息.C接口表(v输出)
	def f显示_网络接口表4(self):
		v命令 = "show ip interface brief"
		v输出 = self.m设备.f执行显示命令(v命令)
		return 基本表信息.C网络接口表4(v输出)
	#动作
	def f登录(self, a用户名 = "", a密码 = ""):
		time.sleep(1)
		v输出 = self.m设备.f输出()
		if "Username:" in v输出:
			v输出 = self.m设备.f执行命令(a用户名)
		if "Password:" in v输出:
			self.m设备.f执行命令(a密码)
	def f提升权限(self, a密码 = "", a级别 = None):
		v命令 = 设备.C命令("enable")
		if a级别:
			v命令 += a级别
		self.f执行当前模式命令(v命令)
		self.m设备.f执行命令(a密码)
	def f保存配置(self):
		self.f执行当前模式命令("write")
	def f清除配置(self):
		self.f执行当前模式命令("delete config.txt")
		self.m设备.f执行命令("y")
	def f重新启动(self):
		self.f执行当前模式命令("reload")
		self.m设备.f执行命令("y")
#===============================================================================
# 全局配置
#===============================================================================
class C全局配置(设备.I全局配置模式):
	"""适用于: s5750(v11.4)"""
	def __init__(self, a):
		设备.I全局配置模式.__init__(self, a)
	#命令
	def fg进入命令(self):
		return "configure terminal"
	#模式
	def f模式_接口配置(self, a接口, a操作 = 设备.E操作.e设置):
		v接口 = 接口.f创建接口(a接口)
		return 接口.C接口(self, v接口)
	def f模式_访问控制列表(self, a名称, a类型 = 设备.E访问控制列表类型.e标准4, a操作 = 设备.E操作.e设置):
		v名称 = 通用访问列表.f解析名称(a名称, a类型, 访问控制列表.C助手)
		#创建访问控制列表对象
		if a类型 == 设备.E访问控制列表类型.e标准4:
			访问控制列表.fi标准范围(v名称)
			v模式 = 访问控制列表.C标准4(self, v名称)
		elif a类型 == 设备.E访问控制列表类型.e扩展4:
			访问控制列表.fi扩展范围(v名称)
			v模式 = 访问控制列表.C扩展4(self, v名称)
		elif a类型 in (设备.E访问控制列表类型.e标准6, 设备.E访问控制列表类型.e扩展6):
			v模式 = 访问控制列表.C六(self, v名称)
		else:
			raise ValueError("未知的访问控制列表类型")
		if a操作 == 设备.E操作.e删除:
			v命令 = c不 + v模式.fg进入命令()
			self.f执行当前模式命令(v命令)
		elif a操作 == 设备.E操作.e重置:
			v命令 = c默认 + v模式.fg进入命令()
			self.f执行当前模式命令(v命令)
		return v模式
	#路由
	def f模式_静态路由(self, a版本 = 设备.E协议.e网络协议4, a虚拟路由转发 = None):
		v版本 = f解析网络协议版本(a版本)
		if v版本 == 设备.E协议.e网络协议4:
			return 静态路由.C静态路由4(self)
		elif v版本 == 设备.E协议.e网络协议6:
			raise NotImplementedError()
		else:
			raise ValueError("未知的版本")
	def f模式_路由信息协议(self, a进程号 = 0, a版本 = 设备.E协议.e路由信息协议, a接口 = None, a操作 = 设备.E操作.e设置):	#rip
		v版本 = 通用路由.f解析路由信息协议版本(a版本)
		if v版本 == 设备.E协议.e路由信息协议:	#rip
			return 路由信息协议.C当代(self)
		elif v版本 == 设备.E协议.e下一代路由信息协议:	#ripng
			raise NotImplementedError()
		else:
			raise ValueError("未知的版本")
	def f模式_开放最短路径优先(self, a进程号 = 1, a版本 = 设备.E协议.e开放最短路径优先, a接口 = None, a操作 = 设备.E操作.e设置):
		v版本 = 通用路由.f解析开放最短路径优先版本(a版本)
		if a接口:	#有接口
			v接口 = 接口.f创建接口(a接口)
			if a版本 == 设备.E协议.e开放最短路径优先2:
				return 开放最短路径优先.C接口(self, a进程号, v接口)
			elif a版本 == 设备.E协议.e开放最短路径优先3:
				raise NotImplementedError()
			else:
				raise ValueError("未知的版本")
		#没有接口
		if a版本 == 设备.E协议.e开放最短路径优先2:
			return 开放最短路径优先.C路由配置(self, a进程号)
		elif a版本 == 设备.E协议.e开放最短路径优先3:
			raise NotImplementedError()
		else:
			raise ValueError("未知的版本")
