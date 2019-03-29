import enum
import time
import cflw网络地址 as 地址
import cflw网络连接 as 连接
import cflw网络设备 as 设备
import cflw字符串 as 字符串
import 网络设备.通用_实用 as 通用实用
import 网络设备.华为_接口 as 接口
import 网络设备.华为_基本表信息 as 基本表信息
import 网络设备.华为_开放最短路径优先 as 开放最短路径优先
import 网络设备.华为_访问控制列表 as 访问控制列表
import 网络设备.华为_前缀列表 as 前缀列表
import 网络设备.华为_虚拟局域网 as 虚拟局域网
c不 = "undo "
c结束符 = '\x1a'	#ctrl+z
#===============================================================================
# 工厂
#===============================================================================
class E型号(enum.IntEnum):
	s3700 = 23700
	s3928 = 23928
	s5700 = 25700
	s7700 = 27700
	ar201 = 30201
	ar1220 = 31220
	ar2220 = 32220
	ar3620 = 33620
def f创建设备(a连接, a型号 = 0, a版本 = 0):
	return C设备(a连接)
#===============================================================================
# 设备
#===============================================================================
ca错误文本与异常类 = [
	("Error: Wrong parameter found at '^' position.", 设备.X命令),
	("Error:Too many parameters found at '^' position.", 设备.X命令)
]
class C设备(设备.I设备):
	def __init__(self, a连接):
		设备.I设备.__init__(self)
		if isinstance(a连接, 连接.I连接):
			self.m连接 = a连接
			self.m连接.fs编码("gb2312")
		else:
			raise TypeError("a连接 必须是 I连接 类型")
		self.fs自动换页("  ---- More ----")
	def f退出(self):
		self.f执行命令("quit")
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
		v输出 = self.f执行显示命令("display this", a自动换页 = True)
		return v输出
	#助手
	def f助手_访问控制列表(self):
		return 访问控制列表.C助手()
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
		#2017-02-19 14:09:32
		#Sunday
		#Time Zone(China-Standard-Time) : UTC-08:00
		v输出 = v输出.split("\n")[0]
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
	def fs终端监视(self, a开关):
		v命令 = 设备.C命令("terminal monitor")
		v命令.f前置否定(a开关, c不)
		self.f执行当前模式命令(v命令)
#===============================================================================
# 信息
#===============================================================================
#硬件信息
class C板属性:
	def __init__(self, a):
		self.m字符串 = 字符串.f提取字符串之间(a, "[Board Properties]\n", "\n\n")
	def fg板类型(self):
		v字符串 = 字符串.f提取字符串之间(self.m字符串, "BoardType=", "\n")
		return v字符串
	def fg板代码(self):
		v字符串 = 字符串.f提取字符串之间(self.m字符串, "BarCode=", "\n")
		return v字符串
	def fg项目(self):
		v字符串 = 字符串.f提取字符串之间(self.m字符串, "Item=", "\n")
		return v字符串
	def fg描述(self):
		v字符串 = 字符串.f提取字符串之间(self.m字符串, "Description=", "\n")
		v长度 = len(v字符串)
		try:
			if v长度 == 10:	#YYYY-MM-DD
				v日期 = time.strptime("%Y-%m-%d")
			elif v长度 == 8:	#YY-MM-DD
				v日期 = time.strptime("%y-%m-%d")
			else:
				return v字符串
			return v日期
		except:
			return v字符串
	def fg生产日期(self):
		v字符串 = 字符串.f提取字符串之间(self.m字符串, "Manufactured=", "\n")
	def fg厂商名(self):
		v字符串 = 字符串.f提取字符串之间(self.m字符串, "VendorName=", "\n")
		return v字符串
class C电子标签信息s3700:	#display elabel
	def __init__(self, a):
		self.m主板 = C板属性(a)
	def fg序列号(self):
		return self.m主板.fg板代码()

#===============================================================================
# 系统视图
#===============================================================================
class C系统视图(设备.I全局配置模式):
	def __init__(self, a):
		设备.I全局配置模式.__init__(self, a)
	def fg进入命令(self):
		return "system-view"
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
	def f模式_开放最短路径优先(self, a进程号, a版本 = 设备.E协议.e开放最短路径优先2):
		return 开放最短路径优先.C路由(self, a进程号)
	#其它
	def f模式_访问控制列表(self, a名称, a类型):
		if a类型 == 设备.E访问控制列表类型.ipv4标准:
			return 访问控制列表.C基本4(self, a名称)
		elif a类型 == 设备.E访问控制列表类型.ipv4扩展:
			return 访问控制列表.C高级4(self, a名称)
		elif a类型 == 设备.E访问控制列表类型.ipv6:
			return 访问控制列表.C高级6(self, a名称)
		else:
			raise ValueError("错误的类型")
	def f模式_前缀列表(self, a名称, a类型 = 设备.E前缀列表类型.e版本4):
		if a类型 == 设备.E前缀列表类型.e版本4:
			return 前缀列表.C前缀列表(self, a名称, 前缀列表.c版本4, 地址.S网络地址4)
		elif a类型 == 设备.E前缀列表类型.e版本6:
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
# 静态路由
#===============================================================================
class C静态路由(设备.C同级模式, 设备.I静态路由配置模式):
	def __init__(self, a):
		设备.I静态路由配置模式.__init__(self, a)
	@staticmethod
	def f解析参数(a网络号, a出接口):
		v网络号 = 地址.C因特网协议4.fc网络(a网络号, False)
		v分割 = v网络号.with_netmask.split('/')
		v接口 = C实用工具.f接口字符串(a出接口)
		s = '%s %s %s' % (*v分割, v接口)
		return s
	def f添加路由(self, a网络号, a出接口):
		self.m设备.f执行命令('ip route-static ' + C静态路由.f解析参数(a网络号, a出接口))
	def f删除路由(self, a网络号, a出接口):
		self.m设备.f执行命令('undo ip route-static ' + C静态路由.f解析参数(a网络号, a出接口))
#===============================================================================
# telnet
#===============================================================================
class Ctelnet(设备.I远端登入, 设备.C同级模式):
	def __init__(self, a):
		设备.I远端登入.__init__(self, a)
	def fs端口号(self, a):
		v命令 = 设备.C命令("telnet server port")
		v命令 += a
		self.f执行当前模式命令(v命令)
	def f开关(self, a):
		v命令 = 设备.C命令("telnet server enable")
		v命令.f前置否定(a, c不)
		self.f执行当前模式命令(v命令)
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