import enum
import time
import cflw网络地址 as 地址
import cflw网络连接 as 连接
import cflw网络设备 as 设备
import cflw字符串 as 字符串
#
from 网络设备.华为_常量 import *
import 网络设备.通用_实用 as 通用实用
import 网络设备.华为_接口 as 接口
import 网络设备.华为_基本表信息 as 基本表信息
import 网络设备.华为_登录 as 登录 
#路由
import 网络设备.通用_路由 as 通用路由
import 网络设备.华为_静态路由 as 静态路由
import 网络设备.华为_开放最短路径优先 as 开放最短路径优先
#其它
import 网络设备.通用_访问控制列表 as 通用访问列表
import 网络设备.华为_访问控制列表 as 访问控制列表
import 网络设备.华为_前缀列表 as 前缀列表
import 网络设备.华为_虚拟局域网 as 虚拟局域网
import 网络设备.华为_连接协议 as 连接协议
#===============================================================================
# 工厂
#===============================================================================
class E型号(enum.IntEnum):
	c交换机 = 0x10000000
	c路由器 = 0x20000000
	c云 = 0x01000000	#适用于: ne系列路由器, cx系列路由器, ce系列交换机
	s3700 = c交换机 + 0x3700
	s3928 = c交换机 + 0x3928
	s5700 = c交换机 + 0x5700
	s7700 = c交换机 + 0x7700
	ce6800 = c交换机 + c云 + 0x6800
	ce12800 = c交换机 + c云 + 0x12800
	ar201 = c路由器 + 0x0201
	ar1220 = c路由器 + 0x1220
	ar2220 = c路由器 + 0x2220
	ar2240 = c路由器 + 0x2240
	ar3260 = c路由器 + 0x3260
	ne40e = c路由器 + c云 + 0x4000
	ne5000e = c路由器 + c云 + 0x5000
	ne9000 = c路由器 + c云 + 0x9000
def f创建设备(a连接, a型号 = 0, a版本 = 0):
	return C设备(a连接, a型号, a版本)
#===============================================================================
# 设备
#===============================================================================
ca错误文本与异常类 = [
	("Error: Wrong parameter found at '^' position.", 设备.X命令),
	("Error:Too many parameters found at '^' position.", 设备.X命令)
]
class C设备(设备.I设备):
	def __init__(self, a连接, a型号, a版本):
		设备.I设备.__init__(self)
		if isinstance(a连接, 连接.I连接):
			self.m连接 = a连接
			self.m连接.fs编码("gb2312")
		else:
			raise TypeError("a连接 必须是 I连接 类型")
		self.m型号 = a型号
		self.m版本 = a版本
		self.fs自动换页("  ---- More ----")
		if a型号 & E型号.c云:
			self.fs自动提交(设备.E自动提交.e退出配置模式时)
	def f退出(self):
		self.f执行命令("quit")
	def f提交(self):
		self.f执行命令("commit")
	def f输入_结束符(self):
		self.f输入(c结束符 + "\r")
	def f模式_用户(self):
		return C用户视图(self)
	def f执行命令(self, a命令):
		v输出 = 设备.I设备.f执行命令(self, a命令)
		self.f检测命令异常(v输出)
		return v输出
	def f执行显示命令(self, a命令, a自动换页 = False):
		v输出 = 设备.I设备.f执行显示命令(self, a命令, a自动换页)
		v输出 = 通用实用.f去头尾行(v输出)
		if v输出.count("\n") < 10:
			self.f检测命令异常(v输出)
		return v输出
	def f显示_当前模式配置(self):
		self.fg当前模式().f切换到当前模式()
		v输出 = self.f执行显示命令("display this", a自动换页 = True)
		return v输出
	#助手
	def f助手_访问控制列表(self):
		return 访问控制列表.C助手
	#其它
	f检测命令异常 = 设备.F检测命令异常(ca错误文本与异常类)
#===============================================================================
# 用户视图
#===============================================================================
class C用户视图(设备.I用户模式):
	def __init__(self, a):
		设备.I用户模式.__init__(self, a)
	def f事件_进入模式(self):
		self.m设备.f刷新()
		self.m设备.f输入_结束符()
		self.m设备.f输入_回车()
		v输出 = self.m设备.f输出()
		if "commit" in v输出:
			self.m设备.f执行命令("n")
	#模式
	def f模式_全局配置(self):
		return C系统视图(self)
	#显示
	def f显示_版本(self):
		v命令 = "display version"
		v输出 = self.m设备.f执行显示命令(v命令, a自动换页 = True)
		return v输出
	def f显示_启动配置(self):
		v命令 = "display saved-configuration"
		v输出 = self.m设备.f执行显示命令(v命令, a自动换页 = True)
		return C配置内容(v输出)
	def f显示_当前配置(self):
		v命令 = "display current-configuration"
		v输出 = self.m设备.f执行显示命令(v命令, a自动换页 = True)
		return C配置内容(v输出)
	def f显示_时间(self):
		v命令 = "display clock"
		v输出 = self.m设备.f执行显示命令(v命令)
		#2019-04-12 10:58:39-08:00	#←新版本的时间后面会带时区，去掉
		#Friday
		#Time Zone(China-Standard-Time) : UTC-08:00
		v输出 = v输出.split("\n")[0]
		v时区位置 = 字符串.f连续找最后(v输出, ":", "-")
		if v时区位置 > 0:
			v输出 = v输出[:v时区位置]
		v时间 = time.strptime(v输出, "%Y-%m-%d %H:%M:%S")
		return v时间
	def f显示_设备名称(self):
		v命令 = "display current-configuration | include sysname"
		v输出 = self.m设备.f执行显示命令(v命令)
		return C输出分析.f从配置取设备名称(v输出)
	def f显示_运行时间(self):
		"从开机到现在所经过的时间"
		raise NotImplementedError()
	def f显示_开机日期(self):
		raise NotImplementedError()
	def f显示_序列号(self):
		raise NotImplementedError()
	def f显示_出厂日期(self):
		raise NotImplementedError()
	#显示 基本表信息
	def f显示_物理地址表(self):
		v命令 = "display mac-address"
		v输出 = self.m设备.f执行显示命令(v命令)
		return 基本表信息.C物理地址表(v输出)
	def f显示_地址解析表(self):
		v命令 = "display arp"
		v输出 = self.m设备.f执行显示命令(v命令)
		return 基本表信息.C地址解析表(v输出)
	def f显示_接口表(self):
		v命令 = "display interface brief"
		v输出 = self.m设备.f执行显示命令(v命令)
		return 基本表信息.C接口表(v输出)
	def f显示_网络接口表4(self):
		v命令 = "display ip interface brief"
		v输出 = self.m设备.f执行显示命令(v命令)
		return 基本表信息.C网络接口表4(v输出)
	#动作
	def f登录(self, a用户名 = "", a密码 = ""):
		time.sleep(1)
		v输出 = self.m设备.f输出()[-100:]
		if "Username:" in v输出:
			v输出 = self.m设备.f执行命令(a用户名)
		if "Password:" in v输出:
			self.m设备.f执行命令(a密码)
		self.f切换到当前模式()
	def fs终端监视(self, a开关):
		v命令 = 设备.C命令("terminal monitor")
		v命令.f前置否定(a开关, c不)
		self.f执行当前模式命令(v命令)
#===============================================================================
# 系统视图
#===============================================================================
class C系统视图(设备.I全局配置模式):
	def __init__(self, a):
		设备.I全局配置模式.__init__(self, a)
	def fg进入命令(self):
		return "system-view"
	def f事件_退出模式(self):
		self.m设备.f自动提交(设备.E自动提交.e退出配置模式时)
	#模式
	def f模式_接口配置(self, a接口):
		v接口 = 接口.f创建接口(a接口)
		#检查值
		if v接口.fi属于分类(设备.E接口分类.e以太网):
			if v接口.fg主序号数() != 3:
				raise ValueError("在华为设备,接口序号有3段")
			elif v接口.fi范围():
				return C端口组(self, v接口)
		if v接口.fi属于分类(设备.E接口分类.e环回):
			if v接口.fg主序号数() != 1:
				raise ValueError("环回口的序号只有1段")
		return 接口.C接口视图(self, v接口)
	def f模式_登录(self, a方式, a范围 = 0, a操作 = 设备.E操作.e设置):
		return 登录.C登录(self, a方式, a范围)
	def f模式_虚拟局域网(self, a序号, a操作 = 设备.E操作.e设置):	#vlan
		v类型 = type(a序号)
		if v类型 == int:
			return 虚拟局域网.C配置(self, a序号)
		elif v类型 == 设备.S接口:
			return 接口.C虚拟局域网(self, a序号)
		elif isinstance(a序号, 设备.I接口配置模式基础):
			return 接口.C虚拟局域网(self, a序号.m接口)
		else:
			raise ValueError()
	#路由
	def f模式_静态路由(self, a版本 = 设备.E协议.e网络协议4, a虚拟路由转发 = None):
		v版本 = 通用路由.f解析网络协议版本(a版本)
		if v版本 == 设备.E协议.e网络协议4:
			return 静态路由.C静态路由4(self)
		elif v版本 == 设备.E协议.e网络协议6:
			raise NotImplementedError()
		else:
			raise ValueError("未知的版本")
	def f模式_开放最短路径优先(self, a进程号 = 1, a版本 = 设备.E协议.e开放最短路径优先, a接口 = None, a操作 = 设备.E操作.e设置):
		if a接口:	#有接口
			v接口 = 接口.f创建接口(a接口)
			if a版本 == 设备.E协议.e开放最短路径优先2:
				return 开放最短路径优先.C接口4(self, a进程号, a接口)
			elif a版本 == 设备.E协议.e开放最短路径优先3:
				raise NotImplementedError()
			else:
				raise ValueError()
		#没有接口
		if a版本 == 设备.E协议.e开放最短路径优先2:
			return 开放最短路径优先.C路由4(self, a进程号)
		elif a版本 == 设备.E协议.e开放最短路径优先3:
			raise NotImplementedError()
		else:
			raise ValueError()
	#其它
	def f模式_访问控制列表(self, a名称, a类型 = None, a操作 = 设备.E操作.e设置):
		v名称, v类型 = 通用访问列表.f解析名称和类型(a名称, a类型, 访问控制列表.C助手)
		if v类型 == 设备.E访问控制列表类型.e标准4:
			return 访问控制列表.C基本4(self, v名称)
		elif v类型 == 设备.E访问控制列表类型.e扩展4:
			return 访问控制列表.C高级4(self, v名称)
		elif v类型 == 设备.E访问控制列表类型.e标准6:
			return 访问控制列表.C基本6(self, v名称)
		elif v类型 == 设备.E访问控制列表类型.e扩展6:
			return 访问控制列表.C高级6(self, v名称)
		else:
			raise ValueError("错误的类型")
	def f模式_前缀列表(self, a名称, a类型 = 设备.E协议.e网络协议4):
		if a类型 == 设备.E协议.e网络协议4:
			return 前缀列表.C前缀列表(self, a名称, 前缀列表.c版本4, 地址.S网络地址4)
		elif a类型 == 设备.E协议.e网络协议6:
			return 前缀列表.C前缀列表(self, a名称, 前缀列表.c版本6, 地址.S网络地址6)
		else:
			raise ValueError("错误的类型")
	#配置
	def fs设备名(self, a名称):
		self.f执行当前模式命令("sysname " + str(a名称))
#===============================================================================
# 用户配置
#===============================================================================
class C用户配置(设备.I用户配置模式):
	def __init__(self, a, a用户名):
		设备.I用户配置模式.__init__(self, a, a用户名)
	def fs密码(self, a密码, a加密等级):
		v加密等级 = C实用工具.f加密等级(a加密等级)
		v命令 = 'username %s password %s %s' % (self.m用户名, v加密等级, a密码)
		self.m设备.f执行命令(v命令)
#===============================================================================
# 工具
#===============================================================================
class C实用工具:
	@staticmethod
	def f加密等级(a):
		if type(a) == str:
			v补全 = 设备.C实用工具.f命令补全(a, 'cipher', 'simple')
			if v补全:
				return v补全
		if 设备.C实用工具.f参数等级(a加密等级, 1):
			return 'cipher'
		else:
			return 'simple'
class C配置内容:
	def __init__(self, a配置):
		self.m配置 = a配置.replace('\r', '')
	def __str__(self):
		return self.m配置
	def fg设备名称(self):
		return C输出分析.f从配置取设备名称(self.m配置)
class C输出分析:
	@staticmethod
	def f从配置取设备名称(a配置):
		if not a配置:
			return ""
		v指定行 = a配置.find(' sysname ')
		v结束 = a配置.find('\n', v指定行)
		if v结束 == -1:
			return a配置[v指定行 + 8 :]
		else:
			return a配置[v指定行 + 8 : v结束]