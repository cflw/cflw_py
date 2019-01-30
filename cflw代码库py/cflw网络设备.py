import re
import time
import datetime
import random
import enum
import fractions
import math
import copy
import ipaddress
import operator
import cflw时间 as 时间
import cflw字符串 as 字符串
import cflw工具_运算 as 运算
c等待 = 2
c间隔 = c等待 / 10
c网络终端退格 = "["	#telnetlib的退格标记
class I设备:
	def __init__(self):
		self.m等待 = c等待
		self.m间隔 = c间隔
		self.m自动换页文本 = ''
		self.ma模式 = []
		self.fs回显(False, False)
		self.m异常开关 = True
		self.m注释 = "#"
	def fs回显(self, a回显 = True, a等待回显 = True):
		self.m回显 = a回显
		self.m等待回显 = a等待回显
	def fs延迟(self, a间隔 = c间隔):
		self.m间隔 = a间隔
		self.m等待 = a间隔 * 10
	def fs自动换页(self, a文本):
		'设置自动换页标记'
		self.m自动换页文本 = a文本
		v长度 = len(a文本)
		v删除标记 = '[' + str(v长度) + 'D'
		self.m自动换页替换 = None
	def f关闭(self):
		self.m连接.f关闭()
	def f设备_回显(self, a内容):
		if self.m回显:
			print(a内容, end = '', flush = True)
		self.f设备_停顿()
	def f设备_停顿(self, a倍数 = 1):
		time.sleep(self.m间隔 * a倍数)
	def f退出(self, a关闭 = False):
		"""设备默认退出当前模式行为, 如果模式重写了 fg退出命令 则不调用该函数\n
		如果当前模式是用户模式, 则退出登陆"""
		raise NotImplementedError()	#实现示例: self.f执行命令("exit")
	def f输入(self, a文本):
		self.f设备_停顿()
		self.m连接.f写(a文本)
	def f输出(self, a等待 = False):
		"读取输出缓存中的内容, 清除输出缓存"
		if not a等待:
			return self.m连接.f读_最新()
		v计数 = 0
		v内容 = ""
		while True:
			v读 = self.m连接.f读_最新()
			if v读:
				v内容 += v读
				time.sleep(self.m间隔)
				continue
			else:
				v计数 += 1
				if v计数 >= 10:
					break
				else:
					time.sleep(self.m间隔)
					continue
		return v内容
	def f输入_回车(self, a数量 = 1, a等待 = 1):
		if a数量 > 0:
			for i in range(a数量):
				self.m连接.f写('\r')
				self.f设备_停顿(2)
		elif a数量 == 0:
			pass	#什么都不做
		else:	#循环,有内容或时间到时结束
			v阻塞 = 时间.C循环阻塞(a等待)
			while v阻塞.f滴答():
				self.m连接.f写('\r')
				v输出 = self.f输出()
				if v输出:
					break
	def f输入_退格(self, a数量 = 1):
		self.m连接.f写('\b' * a数量)
	def f输入_空格(self, a数量 = 1):
		self.m连接.f写(' ' * a数量)
	def f输入_任意键(self, a数量 = 1):
		v字符 = random.choice("qwertyuiopasdfghjklzxcvbnm")
		self.m连接.f写(v字符)
	def f输入_注释(self):
		self.m连接.f写(self.m注释)
	def f刷新(self, a回显 = True):
		"清除正在输入的命令, 清除输出缓存"
		self.f设备_停顿()
		v输出 = self.f输出()
		if a回显:
			self.f设备_回显(v输出)
	def f等待响应(self, a时间 = 5):
		v输出 = self.m连接.f读_直到('', a时间)
		if self.m回显 and v输出:
			print(v输出, end = '', flush = True)
			return
	def f检查命令(self, a命令):
		"判断命令能不能执行"
		raise NotImplementedError()
	def f执行命令(self, a命令):
		"输入一段字符按回车, 并返回输出结果"
		self.f刷新()
		self.f输入(str(a命令))
		self.f输入_回车()
		v输出 = self.f输出()
		self.f设备_回显(v输出)
		return v输出
	def f执行显示命令(self, a命令, a自动换页 = False):
		"有自动换页功能"
		self.f刷新()
		self.f输入(str(a命令))
		self.f输入_回车()
		v输出 = ''
		if a自动换页 and self.m自动换页文本:
			while True:
				v读 = self.f输出(a等待 = True)
				v输出 += v读
				if self.m自动换页文本 in v读:	#还有更多
					self.f输入_空格()
					if self.m等待回显:
						print('.', end = '', flush = True)
					continue
				else:
					break
			v输出 = self.f自动换页替换(v输出)
		else:
			v输出 = self.f输出(a等待 = True)
		v输出 = v输出.replace("\r\n", "\n")
		self.f设备_回显(v输出)
		return v输出
	def f自动换页替换(self, a字符串: str):
		v替换位置 = a字符串.find(self.m自动换页文本)
		if v替换位置 < 0:
			return a字符串	#找不到,不处理
		if not self.m自动换页替换:	#没有则生成
			v退格结束位置 = 字符串.f连续找最后(a字符串, c网络终端退格, c网络终端退格, "D", a开始 = v替换位置)
			if v退格结束位置 >= 0:	#telnetlib
				self.m自动换页替换 = a字符串[v替换位置 : v退格结束位置+1]
			else:	#打字机
				v回车位置 = a字符串.find(" \r", v替换位置)
				self.m自动换页替换 = a字符串[v替换位置, v回车位置 + 1]
		return a字符串.replace(self.m自动换页替换, '')
	def fg当前模式(self):
		return self.ma模式[-1]
	def f进入模式(self, a模式):
		if not isinstance(a模式, I模式):
			raise TypeError("a模式 必须是一个 I模式 对象")
		self.f执行命令(a模式.fg进入命令())
		self.ma模式.append(a模式)
	def f退出模式(self):
		v模式 = self.ma模式.pop()
		if type(v模式).fg退出命令 != I模式.fg退出命令:
			self.f执行命令(v模式.fg退出命令())
		else:
			self.f退出()
	def f切换模式(self, aa模式: tuple):
		"自动退出当前模式并进入新模式"
		v现模式长度 = len(self.ma模式)
		v新模式长度 = len(aa模式)
		v最小长度 = min(v现模式长度, v新模式长度)
		#判断模式是否一样,并退出现模式
		for i in range(v最小长度):
			#找不同模式的位置,然后退出到有相同模式的位置为止
			#如果新模式是现模式的更深一层模式,不退出,直接进入新模式
			if self.ma模式[i] != aa模式[i]:
				for i1 in range(v现模式长度 - i):
					self.f退出模式()
				v进入位置 = i
				break
			else:
				v进入位置 = i + 1
		#进入模式
		for i in range(v进入位置, v新模式长度):
			self.f进入模式(aa模式[i])
	def fg提示符(self):
		raise NotImplementedError()
	def f抛出模式异常(self):
		raise X模式(self.fg当前模式())
	def f自动适应延迟(self, a测试字符: str = '#'):
		"发送字符测试延迟,根据响应时间确定间隔"
		v和 = 0
		v秒表 = 时间.C秒表()
		for i in range(10):
			v秒表.f重置()
			self.m连接.f写(a测试字符)
			self.m连接.f读_直到(a测试字符, 2)
			v和 = v秒表.f滴答()
		self.fs延迟(v和 / 5)	#间隔设置为平均响应时间的2倍
	#模式
	def f模式_用户(self):	#要求：ma模式[0]总是用户模式，没有则创建。不能创建多个用户模式对象。
		"用户模式只能查看信息,做一些基本操作,不能配置"
		raise NotImplementedError()
	def f模式_启动(self):
		"在交换机开机阶段执行操作的模式,需要串口连接"
		raise NotImplementedError()
	#显示.当存在可以在任何模式使用的命令,直接重写这里的函数
	def f显示_当前模式配置(self):
		raise NotImplementedError()
	#助手
	def f助手_访问控制列表(self):
		raise NotImplementedError()
	def f助手_密码(self):
		raise NotImplementedError()
class C命令:	#快速添加命令参数
	def __init__(self, *t):
		self.m字符串 = ""
		self.f添加(*t)
	def __add__(self, a):
		v命令 = copy.copy(self)
		v命令 += a
		return v命令
	def __iadd__(self, a):
		v类型 = type(a)
		if v类型 in (tuple, list):
			self.f添加(*a)
		else:
			self.f添加(a)
		return self
	def __radd__(self, a):
		v命令 = copy.copy(self)
		v类型 = type(a)
		if v类型 in (tuple, list):
			v命令.f前面添加(*a)
		else:
			v命令.f前面添加(a)
		return v命令
	def __str__(self):
		return self.m字符串
	def f添加(self, *a):
		for v in a:
			if self.m字符串 and self.m字符串[-1] != ' ':	#添加空格
				self.m字符串 += " "
			self.m字符串 += str(v)
		return self
	def f前面添加(self, *a):
		if not a:
			raise TypeError
		for v in a:
			v命令 = str(v)
			if v命令[-1] == ' ':
				self.m字符串 = v命令 + self.m字符串
			else:
				self.m字符串 = v命令 + " " + self.m字符串
		return self
	def f前置否定(self, a判断: bool, a命令):
		if not a判断:
			self.fs前面添加(a命令)
		return self
def F检测命令异常(a列表):
	def f检测命令异常(self, a输出):
		def f返回异常(ax):
			if type(ax) == type:
				v异常 = ax(a输出)
			else:
				v异常 = ax
			if self.m异常开关:
				raise v异常
			return v异常
		for v文本, vt异常 in a列表:
			if v文本 in a输出:
				return f返回异常(vt异常)
		return None
	return f检测命令异常
#===============================================================================
# 模式基类
#===============================================================================
class E版本(enum.IntEnum):
	e网络协议4 = 4
	e网络协议6 = 6
	e路由信息协议 = 4
	e下一代路由信息协议 = 6
	e开放最短路径优先2 = 4
	e开放最短路径优先3 = 6
class E操作(enum.IntEnum):
	e设置 = 0	#覆盖原有配置,不存在则创建
	e重置 = 1	#恢复默认配置
	e添加 = 2	#添加值
	e删除 = 3	#删除/恢复
class I模式:
	def __init__(self, a):
		if isinstance(a, I设备):	#a是设备
			self.m设备 = a
			self.m模式栈 = (self, )
		elif isinstance(a, I模式):	#a是父模式
			self.m设备 = a.m设备
			self.m模式栈 = a.m模式栈 + (self, )
		else:
			raise TypeError()
	def __eq__(self, a):	#通用的模式相等比较
		if isinstance(a, I模式):
			if self is a:
				return True
			elif self.fg进入命令 != a.fg进入命令:
				return False
			else:
				return self.fg进入命令() == a.fg进入命令()
		else:
			return False
	def fi当前模式(self):
		return self == self.m设备.fg当前模式()
	def f切换到当前模式(self):
		if not self.fi当前模式():
			self.m设备.f切换模式(self.m模式栈)
	def f执行当前模式命令(self, a命令: C命令):
		self.f切换到当前模式()
		self.m设备.f执行命令(a命令)
	def f显示_当前模式配置(self):	#当前模式的配置,在用户模式显示所有配置
		self.f切换到当前模式()
		return self.m设备.f显示_当前模式配置()
	def fg模式参数(self):
		"表示要进入该模式所使用的参数"
		raise NotImplementedError()
	def fg进入命令(self):
		"要进入该模式所使用的完整命令"
		raise NotImplementedError()
	def fg退出命令(self):
		"退出到上一级模式所使用的完整命令"
		raise NotImplementedError()
	def fg上级模式(self):
		if len(self.m模式栈) > 1:
			return self.m模式栈[-2]
		else:
			return None
	def fg删除命令(self):
		"删除当前模式所使用的完整命令,需要在上级模式执行"
		raise NotImplementedError()
class C同级模式(I模式):	#和上一层模式是同一级别的，不需要进入命令也不需要退出命令
	def fg模式参数(self):
		return ""
	def fg进入命令(self):
		return ""
	def fg退出命令(self):
		return ""
#===============================================================================
# 用户模式的操作
#===============================================================================
class I用户模式(I模式):
	c模式名 = "用户模式"
	def __init__(self, a设备):
		I模式.__init__(self, a设备)
	#模式
	def f模式_全局配置(self):
		raise NotImplementedError()
	#显示设备状态
	def f显示_版本(self):
		raise NotImplementedError()
	def f显示_时间(self)->time.struct_time:
		"返回time.struct_time对象"
		raise NotImplementedError()
	def f显示_启动配置(self):
		raise NotImplementedError()
	def f显示_当前配置(self):
		raise NotImplementedError()
	def f显示_设备名称(self)->str:
		raise NotImplementedError()
	def f显示_日志(self):
		raise NotImplementedError()
	def f显示_设备版本(self)->str:
		raise NotImplementedError()
	def f显示_cpu使用率(self):
		raise NotImplementedError()
	def f显示_内存使用率(self):
		"返回数字"
		raise NotImplementedError()
	def f显示_温度(self)->dict:
		"返回字典，键=槽位，值=温度"
		raise NotImplementedError()
	def f显示_运行时间(self)->datetime.timedelta:
		"从开机到现在所经过的时间"
		raise NotImplementedError()
	def f显示_开机日期(self)->time.struct_time:
		raise NotImplementedError()
	def f显示_序列号(self)->str:
		raise NotImplementedError()
	def f显示_出厂日期(self)->time.struct_time:
		raise NotImplementedError()
	#显示具体
	def f显示_路由表4(self):
		raise NotImplementedError()
	def f显示_默认路由4(self):
		raise NotImplementedError()
	def f显示_链路层发现协议(self):
		"返回列表，列表包含邻居字典"
		raise NotImplementedError()
	def f显示_接口表(self):
		"返回接口表,应能迭代出 S接口表项"
		raise NotImplementedError()
	def f显示_网络接口表4(self):
		"返回网络接口表,应能迭代出 S网络接口表项"
		raise NotImplementedError()
	def f显示_网络接口表6(self):
		"返回网络接口表,应能迭代出 S网络接口表项"	
		raise NotImplementedError()
	def f显示_物理地址表(self):	#mac表
		raise NotImplementedError()
	def f显示_地址解析表(self):	#arp表
		raise NotImplementedError()
	def f显示_网络地址转换表(self):	#nat表
		raise NotImplementedError()
	#动作
	def f登录(self, a用户名 = "", a密码 = ""):
		raise NotImplementedError()
	def f提升权限(self, a密码 = ""):
		raise NotImplementedError()
#===============================================================================
# 信息
#===============================================================================
class I版本信息:
	def fg版本s(self)->str:
		"完整的版本字符串"
		raise NotImplementedError()
	def fg版本号(self)->str:
		raise NotImplementedError()
	def fg编译日期(self)->time.struct_time:
		"如果找不到,返回None"
		raise NotImplementedError()
	def fg运行时间(self)->datetime.timedelta:
		raise NotImplementedError()
	def fg开机日期(self)->time.struct_time:
		raise NotImplementedError()
class E物理地址类型(enum.IntEnum):
	e动态 = 0
	e静态 = 1
	e安全 = 2
class S物理地址项:
	def __init__(self, a地址 = None, a接口 = None, a虚拟局域网 = None, a类型 = None):
		self.m地址 = a地址
		self.m接口 = a接口
		self.m虚拟局域网 = a虚拟局域网
		self.m类型 = a类型
	def __str__(self):
		return 字符串.ft字符串(self.m地址, self.m接口, self.m虚拟局域网, self.m类型)
class S网络接口表项:
	def __init__(self, a接口 = None, a地址 = None, a状态 = None, a描述 = ""):
		self.m接口 = a接口
		self.m地址 = a地址
		self.m状态 = a状态
		self.m描述 = ""
	def __str__(self):
		return 字符串.ft字符串(self.m接口, self.m地址, self.m状态, self.m描述)
class S接口表项:
	def __init__(self, a接口 = None, a状态 = None, a描述 = ""):
		self.m接口 = a接口
		self.m状态 = a状态
		self.m描述 = ""
	def __str__(self):
		return 字符串.ft字符串(self.m接口, self.m状态, self.m描述)
#===============================================================================
# 全局配置模式的操作
#===============================================================================
class I全局配置模式(I模式):
	c模式名 = "全局配置模式"
	def __init__(self, a设备):
		I模式.__init__(self, a设备)
	#模式
	def f模式_时间(self):
		raise NotImplementedError()
	def f模式_接口配置(self, a接口, a操作 = E操作.e设置):
		raise NotImplementedError()
	def f模式_用户配置(self, a用户名, a操作 = E操作.e设置):
		raise NotImplementedError()
	def f模式_登陆配置(self, a方式, a范围, a操作 = E操作.e设置):	#console,vty之类的
		raise NotImplementedError()
	def f模式_时间范围(self, a名称, a操作 = E操作.e设置):
		raise NotImplementedError()
	def f模式_虚拟局域网(self, a序号, a操作 = E操作.e设置):	#vlan
		raise NotImplementedError()
	#模式_路由
	def f模式_静态路由(self, a版本 = E版本.e网络协议4):
		raise NotImplementedError()
	def f模式_路由信息协议(self, a进程号 = 0, a版本 = E版本.e网络协议4, a操作 = E操作.e设置):	#rip
		raise NotImplementedError()
	def f模式_开放最短路径优先(self, a进程号, a版本 = E版本.e开放最短路径优先2, a操作 = E操作.e设置):	#ospf
		raise NotImplementedError()
	def f模式_增强内部网关路由协议(self, a名称, a版本 = E版本.e网络协议4, a操作 = E操作.e设置):	#eigrp
		raise NotImplementedError()
	def f模式_边界网关协议(self, a自治系统号, a操作 = E操作.e设置):	#bgp
		raise NotImplementedError()
	def f模式_中间系统到中间系统(self, a进程号, a操作 = E操作.e设置):	#isis
		raise NotImplementedError()
	def f模式_热备份路由协议(self, a组号, a操作 = E操作.e设置):	#hsrp
		raise NotImplementedError()
	def f模式_虚拟路由器冗余协议(self, a组号, a操作 = E操作.e设置):	#vrrp
		raise NotImplementedError()	
	def f模式_网关负载均衡协议(self, a组号, a操作 = E操作.e设置):	#glbp
		raise NotImplementedError()
	#模式_其它
	def f模式_访问控制列表(self, a名称, a类型, a操作 = E操作.e设置):
		raise NotImplementedError()
	def f模式_前缀列表(self, a名称, a类型, a操作 = E操作.e设置):
		raise NotImplementedError()
	def f模式_端口安全(self):
		raise NotImplementedError()
	def f模式_接口端口安全(self, a接口):
		raise NotImplementedError()
	def f模式_远端登入(self):	#telnet
		raise NotImplementedError()
	def f模式_安全外壳(self):	#ssh
		raise NotImplementedError()
	def f模式_网络协议地址池(self, a名称, a操作 = E操作.e设置):	#ip pool
		raise NotImplementedError()
	def f模式_动态主机配置协议地址池(self, a名称, a操作 = E操作.e设置):	#dhcp pool
		raise NotImplementedError()
	def f模式_动态主机配置协议(self):	#dhcp
		raise NotImplementedError()
	def f模式_域名系统(self):	#dns
		raise NotImplementedError()
	def f模式_网络时间协议服务器(self):	#ntp
		raise NotImplementedError()
	def f模式_网络时间协议客户端(self): #ntp
		raise NotImplementedError()
	def f模式_简单网络管理协议(self):	#snmp
		raise NotImplementedError()
	def f模式_以太网上的点对点协议(self):	#pppoe
		raise NotImplementedError()
	def f模式_多协议标签交换(self):	#mpls
		raise NotImplementedError()
	def f模式_第二层隧道协议(self, a名称):	#l2tp
		raise NotImplementedError()
	#配置
	def fs设备名(self, a名称):
		raise NotImplementedError()
#===============================================================================
# 时间
#===============================================================================
class I时间(I模式):
	c模式名 = "系统时间"
	def __init__(self, a):
		I模式.__init__(self, a)
	def f等于系统时间(self):
		"把设备时间设置为当前系统时间"
		v时区 = 时间.S时区.fc系统时区()
		self.fs时区(v时区)
		self.fs日期时间(time.localtime())
	def fs日期时间(self, a):
		raise NotImplementedError()
	def fs时区(self, *a):
		raise NotImplementedError()
	@staticmethod
	def f解析日期时间(a):
		if isinstance(a, time.struct_time):
			return a
		elif isinstance(a, datetime.datetime):
			return a.timetuple()
		else:
			return TypeError
	@staticmethod
	def f解析时区(a):
		"返回datetime.tzinfo对象"
		v长度 = len(a)
		if v长度 == 1:
			v0 = a[0]
			if isinstance(v0, datetime.tzinfo):
				return v0
			elif isinstance(v0, 时间.S时区):
				return v0.f转datetime点timezone()
		elif v长度 == 2:
			v0 = a[0]
			v1 = a[1]
			return datetime.timezone(时间.C字符串转时间差.f时间(v1), v0)
		else:
			raise TypeError
#===============================================================================
# 登陆
#===============================================================================
class E登陆方式(enum.IntEnum):
	e控制台 = 0	#console
	e虚拟终端 = 3	#vty
class E登陆认证方式(enum.IntEnum):
	e无 = 0,
	e密码 = 1,
	e账号 = 2
	e认证授权记账 = 3
	aaa = 3
class I登陆配置模式(I模式):
	def __init__(self, a):
		I模式.__init__(self, a)
	def fs认证方式(self, a):
		raise NotImplementedError()
	def fs登陆协议(self, a):
		raise NotImplementedError()
	def fs访问控制列表(self, a):
		raise NotImplementedError()
	def fs超时时间(self, a秒):
		raise NotImplementedError()
#===============================================================================
# 结构
#===============================================================================
class E日子(enum.IntEnum):
	e一 = 0
	e二 = 1
	e三 = 2
	e四 = 3
	e五 = 4
	e六 = 5
	e日 = 6
	e工作日 = 8
	e周末 = 9
	e每天 = 7
class S时间范围:
	def __init__(self, a开始时间, a结束时间):
		self.m绝对 = True
		self.m开始时间 = a开始时间
		self.m结束时间 = a结束时间
	@staticmethod
	def fc定期(a日子, a开始时间, a结束时间):
		"""
		a日子: E日子\n
		a开始时间: str, tuple(时, 分)\n
		a结束时间: str, tuple(时, 分)
		"""
		v = S时间范围(a开始时间, a结束时间)
		v.m绝对 = False
		v.m日子 = a日子
		return v
	@staticmethod
	def fc绝对(a开始时间, a结束时间):
		v = S时间范围(a开始时间, a结束时间)
		return v
class I时间范围配置模式(I模式):
	def __init__(self, a):
		I模式.__init__(self, a)
	def f添加(self, a时间范围):
		raise NotImplementedError()
	def f删除(self, a时间范围):
		raise NotImplementedError()
#===============================================================================
# 接口配置模式的操作
#===============================================================================
class E接口(enum.IntEnum):#为保证取接口全名有个优先级顺序，高位16位为优先级
	e空 = 0x00000000
	e环回 = 0x00000100
	e以太网 = 0x00000201
	e快速以太网 = 0x00000202
	e吉比特以太网 = 0x00000203
	e十吉以太网 = 0xffff0204
	e串行 = 0x00000300
	e虚拟局域网 = 0x00000400
	e隧道 = 0x00000500
class E接口分类(enum.IntEnum):
	e空 = 0
	e环回 = 1
	e以太网 = 2
	e串行 = 3
	e虚拟局域网 = 4
	e隧道 = 5
class E方向(enum.IntEnum):
	e入 = 0
	e出 = 1
ca接口名称 = {
	E接口.e空: "Null",
	E接口.e环回: "Loopback",
	E接口.e以太网: "Ethernet",
	E接口.e快速以太网: "FastEthernet",
	E接口.e吉比特以太网: "GigabitEthernet",
	E接口.e十吉以太网: "TenGigabitEthernet",
	E接口.e串行: "Serial",
	E接口.e虚拟局域网: "Vlan",
	E接口.e隧道: "Tunnel"
}
def fc接口名称字典(a字典 = None):
	v字典 = copy.copy(ca接口名称)
	if a字典:
		v字典.update(a字典)
	return v字典
class S接口:
	"表示一个接口"
	def __init__(self, a类型: int, a名称: str, a序号: list):
		self.m类型 = int(a类型)
		self.m名称 = str(a名称)
		self.m序号 = list(a序号)
	def __str__(self):
		if self.m名称:
			return self.m名称 + self.fg序号字符串()
		else:
			self.ft字符串(ca接口名称)
	def __eq__(self, a):
		if isinstance(a, S接口):
			return (self.m类型 == a.m类型) and (self.m序号 == a.m序号)
		else:
			return False
	@staticmethod
	def fc字符串(a字符串, a全称字典 = ca接口名称, ai字典字符串在右 = True):
		if ai字典字符串在右:
			va字符串 = a全称字典.values()
			vf类型 = 运算.f字典按值找键
		else:
			va字符串 = a全称字典.keys()
			vf类型 = dict.__getitem__
		v名称 = S接口.f解析_取全称(a字符串, va字符串)
		v类型 = vf类型(a全称字典, v名称)
		v序号 = S接口.f解析_取序号(a字符串)
		return S接口(v类型, v名称, v序号)
	@staticmethod
	def fc标准(a类型, *a序号):
		"(类型,*序号,子序号)"
		return S接口(a序号, "", a序号[1:])
	def fg序号字符串(self):
		"包含子序号"
		#转成字符串列表
		v列表 = list(self.m序号)
		v子序号 = v列表.pop()
		for i in range(len(v列表)):
			v = v列表[i]
			if type(v) == range:
				v列表[i] = str(v.start) + "-" + str(v.stop - 1)
			else:
				v列表[i] = str(v)
		s = '/'.join(v列表)
		if v子序号:
			s += '.' + str(v子序号)
		return s
	@staticmethod
	def f解析_取全称(a, a参考 = ca接口名称):
		v类型 = type(a参考)
		if hasattr(a参考, "__iter__"):
			v列表 = a参考
		else:
			raise TypeError()
		v名称 = S接口.f解析_取名称(a)
		return 字符串.f找前面匹配(v列表, v名称, re.IGNORECASE)
	@staticmethod
	def f解析_取名称(a):
		return re.split(r"\d", a)[0]
	@staticmethod
	def f解析_取序号(a):
		"提取接口字符串的序号部分,返回列表,包含子序号"
		v列表 = a.split("/")
		#[0]去字符,保留数字
		v列表[0] = re.findall(r"\d+.*", v列表[0])[0]
		#[-1]判断子序号
		if "." in v列表[-1]:
			v分割 = v列表[-1].split(".")
			v列表[-1] = v分割[0]
			v子序号 = int(v分割[1])
		else:
			v子序号 = 0
		#转成int,range
		v长度 = len(v列表)
		for i in range(v长度):
			v = v列表[i]
			if "-" in v:
				if i != v长度 - 1:
					raise ValueError("只有最后一段才能使用范围")
				v分割 = v.split("-")
				v列表[i] = range(int(v分割[0]), int(v分割[1]))
			else:
				v列表[i] = int(v)
		v列表.append(v子序号)
		return v列表
	def fi范围(self):
		return type(self.m序号[-2]) == range
	def fs名称(self, a):
		v类型 = type(a)
		if v类型 == str:
			self.m名称 = a
		elif v类型 == dict:
			self.m名称 = a[self.m类型]
		else:
			raise TypeError("无法识别的参数")
	def fg名称(self, a字典 = None):
		if a字典:
			return a字典[self.m类型]
		elif self.m名称:
			return self.m名称
		else:
			return ca接口名称[self.m类型]
	def ft字符串(self, a字典 = ca接口名称):
		return self.fg名称(a字典) + self.fg序号字符串()
	def fg主序号数(self):
		return len(self.m序号) - 1
	def fg分类(self):
		#取类型的16进制的低3,4位
		return self.m类型 % 0x10000 // 0x10
	def fi属于分类(self, *a分类):
		v值 = self.fg分类()
		for v in a分类:
			v分类 = int(v)
			if v值 == v分类:
				return True
		return False
class F创建接口:
	def __init__(self, a全称字典 = ca接口名称):
		self.m全称字典 = a全称字典
	def __call__(self, a):
		v类型 = type(a)
		if v类型 == S接口:
			return a
		elif isinstance(a, I接口配置模式):
			return a.m接口
		elif v类型 == str:
			return S接口.fc字符串(a, self.m全称字典)
		else:
			raise TypeError("无法解析的类型")
class I接口配置模式(I模式):
	c模式名 = "接口配置模式"
	def __init__(self, a设备, a接口):
		I模式.__init__(self, a设备)
		if not (isinstance(a接口, S接口) or type(a接口) == str):
			raise TypeError("a接口 必须是一个 S接口 对象")
		self.m接口 = a接口
	def __eq__(self, a):
		if isinstance(a, I接口配置模式):
			return self.m接口 == a.m接口
		else:
			return False
	#通用方法
	def fg模式参数(self):	#在这里确定不同厂商的接口名称
		return (self.m接口,)
	def fg进入命令(self):
		return C命令("interface") + self.fg模式参数()
class I接口配置模式_以太网(I接口配置模式):
	c模式名 = "以太网接口配置模式"
	def __init__(self, a, a接口):
		I接口配置模式.__init__(self, a, a接口)
	#接口
	def fg地址(self):
		"返回列表"
		raise NotImplementedError()
	def f开关(self, a开关):
		raise NotImplementedError()
	def f物理_s速率(self, a速率 = 1000, a操作 = E操作.e设置):
		raise NotImplementedError()
	def f物理_s双工模式(self, a全双工 = True, a操作 = E操作.e设置):
		raise NotImplementedError()
	#三层
	def fs网络地址4(self, a地址, a操作 = E操作.e设置):
		raise NotImplementedError()
	def fe网络地址4(self):
		"返回这个接口拥有的所有地址"
		raise NotImplementedError()
	def fs网络地址6(self, a地址, a操作 = E操作.e设置):
		raise NotImplementedError()
	def fe网络地址6(self):
		raise NotImplementedError()
	#二层
	def f二层_s链路模式(self, a模式):
		raise NotImplementedError()
	def f二层中继_s通过(self, a虚拟局域网, a操作 = E操作.e设置):
		raise NotImplementedError()
	def f二层中继_s封装协议(self, a协议):
		raise NotImplementedError()
	def f二层中继_s本征(self, a虚拟局域网):
		raise NotImplementedError()
	def f二层访问_绑定(self, a虚拟局域网):
		raise NotImplementedError()
	#端口安全
	def f端口安全_开关(self, a):
		raise NotImplementedError()
	def f端口安全_绑定地址(self, a地址):
		raise NotImplementedError()
	def f端口安全_解绑地址(self, a地址):
		raise NotImplementedError()
	def f端口安全_s最大地址数(self, a数量):
		raise NotImplementedError()
	def f端口安全_s自动恢复时间(self, a时间):
		raise NotImplementedError()
	def f端口安全_s地址老化时间(self, a时间):
		raise NotImplementedError()
	def f端口安全_s端口安全动作(self, a动作):
		raise NotImplementedError()
	#流量控制
	def fs访问控制列表(self, a访问控制列表, a方向):
		raise NotImplementedError()
	def fd访问控制列表(self, a方向):
		raise NotImplementedError()
	def fs服务质量(self, a, a方向):
		raise NotImplementedError()
	def fd服务质量(self, a方向):
		raise NotImplementedError()
class I接口配置模式_串行(I接口配置模式):
	def __init__(self, a, a接口):
		I接口配置模式.__init__(self, a, a接口)
	#接口
	def fs时钟频率(self, a频率):
		raise NotImplementedError()

#===============================================================================
# 用户&密码&权限
#===============================================================================
class E服务类型(enum.IntEnum):
	e无 = 0x00
	e控制台 = 0x01
	e远程连接 = 0x02
	e安全外壳 = 0x04
	e全部 = 0xff
class I用户配置模式(I模式):
	c模式名 = "用户配置模式"
	def __init__(self, a设备, a用户名):
		I模式.__init__(self, a设备)
		self.m用户名 = str(a用户名)
	def fs密码(self, a密码):
		raise NotImplementedError()
	def fs权限(self, a权限):
		raise NotImplementedError()
	def fs服务类型(self, a服务类型):
		raise NotImplementedError()
class I密码助手:
	@staticmethod
	def f生成密码(a密码, a加密级别):
		raise NotImplementedError()
	@staticmethod
	def f提取密码(a字符串):
		raise NotImplementedError()
#===============================================================================
# 路由
#===============================================================================
class E路由协议(enum.IntEnum):
	e直连 = 0
	e静态 = 1
	e路由信息协议 = 10	#ria
	e开放最短路径优先 = 11	#ospf
	e边界网关协议 = 12	#bga
	e增强内部网关路由协议 = 13	#eigra
	e中间系统到中间系统 = 14	#isis
class C路由:
	pass
class C路由协议:
	c版本字符串转数字 = {
		"ip": 4,
		"ipv4": 4,
		"ipv6": 6,
		"rip": 4,
		"ripng": 6,
	}
	@staticmethod
	def f解析_版本(a):	#返回整数
		v类型 = type(a)
		if v类型 == int or isinstance(a, enum.Enum):
			return v类型
		elif v类型 == str:
			return C路由协议.c版本字符串转数字[a]
		else:
			raise TypeError("无法解析的类型")
#静态路由	=====================================================================
class I静态路由配置模式(I模式):
	def __init__(self, a):
		I模式.__init__(self, a)
	def f显示_路由表(self):
		raise NotImplementedError()
	def fs路由4(self, a网络号, a下一跳, a操作 = E操作.e添加):
		raise NotImplementedError()
	def fs默认路由4(self, a下一跳, a操作 = E操作.e添加):
		raise NotImplementedError()
	def fs路由6(self, a网络号, a下一跳, a操作 = E操作.e添加):
		raise NotImplementedError()
	def fs默认路由6(self, a下一跳, a操作 = E操作.e添加):
		raise NotImplementedError()
#路由信息协议rip	=============================================================
class I路由信息协议(I模式):
	def __init__(self, a):
		I模式.__init__(self, a)
	def f显示_路由表(self):
		raise NotImplementedError()
	def f通告网络(self, a网络号):
		raise NotImplementedError()
	def f删除网络(self, a网络号):
		raise NotImplementedError()
	def f通告接口(self, a接口):
		raise NotImplementedError()
	def f删除接口(self, a接口):
		raise NotImplementedError()
#开放最短路径优先ospf	=========================================================
class E开放最短路径优先链路状态通告类型(enum.IntEnum):
	"OSPF LSA类型"
	e全部 = 0
	e路由器 = 1
	e网络 = 2
	e网络汇总 = 3
	e区域边界路由器汇总 = 4
	e自治系统外部 = 5
	e组成员 = 6
	e非纯末节区域外部 = 7
	e外部属性 = 8
	e本地链路不透明 = 9
	e本地区域不透明 = 10
	e自制系统不透明 = 11
	#ospfv3
	e链路 = 8
	e区域内前缀 = 9
class E开放最短路径优先邻居状态(enum.IntEnum):
	e关闭 = 0
	e尝试 = 1
	e初始 = 2
	e双向 = 3
	e预启动 = 4
	e交换 = 5
	e加载 = 6
	e完成 = 7
class E开放最短路径优先选举状态(enum.IntEnum):
	e无 = 0
	e指定 = 1
	e备用 = 2
	e非指定 = 3
class I开放最短路径优先(I模式):
	c模式名 = "开放最短路径优先配置模式"
	def __init__(self, a, a进程号):
		I模式.__init__(self, a)
		self.m进程号 = a进程号
	def fg模式参数(self):
		"返回进程号"
		return (self.m进程号,)
	def f模式_区域(self, a区域):
		raise NotImplementedError()
	def f模式_接口(self, a接口):
		raise NotImplementedError()
	def f模式_虚链路(self, a区域, a对端):
		raise NotImplementedError()
	#静态
	@staticmethod
	def f解析区域(a区域):
		v区域 = int(a区域)
		if v区域 < 0 or v区域 > 4294967295:
			raise ValueError("a区域 超出范围,应该在0~4294967295之间")
		return v区域
	#显示
	def f显示_路由表(self):
		raise NotImplementedError()
	def f显示_邻居(self):
		raise NotImplementedError()
	def f显示_数据库(self, a类型 = E开放最短路径优先链路状态通告类型.e全部):
		raise NotImplementedError()
	#操作
	def f重启进程(self):
		raise NotImplementedError()
	def fs路由器号(self, a):
		raise NotImplementedError()
	def f通告默认路由(self, a总是 = False, a开销 = 0):
		raise NotImplementedError()
	def f通告网络(self, a网络号, a区域):
		raise NotImplementedError()
	def f删除网络(self, a网络号, a区域):
		raise NotImplementedError()
	def f通告接口(self, a接口, a区域):
		raise NotImplementedError()
	def f删除接口(self, a接口, a区域):
		raise NotImplementedError()
class I开放最短路径优先区域(I模式):
	c模式名 = "开放最短路径优先区域配置模式"
	def __init__(self, a, a区域):
		I模式.__init__(self, a)
		self.m区域 = a区域
	def f通告网络(self, a网络号):
		raise NotImplementedError()
	def f删除网络(self, a网络号):
		raise NotImplementedError()
	def f通告接口(self, a接口):
		raise NotImplementedError()
	def f删除接口(self, a接口):
		raise NotImplementedError()
class I开放最短路径优先接口(I接口配置模式):
	c模式名 = "开放最短路径优先接口配置模式"
	def __init__(self, a, a接口):
		I接口配置模式.__init__(self, a, a接口)
	def f通告接口(self, a进程号, a区域):
		raise NotImplementedError()
	def f删除接口(self, a进程号, a区域):
		raise NotImplementedError()	
	def fs问候时间(self, a时间 = 10):
		raise NotImplementedError()
	def fs死亡时间(self, a时间 = 40):
		raise NotImplementedError()
	def fs重传时间(self, a时间 = 5):
		raise NotImplementedError()
	def fs传输时间(self, a时间 = 1):
		raise NotImplementedError()
	def fs开销(self, a开销):
		raise NotImplementedError()
	def fs网络类型(self, a类型):
		raise NotImplementedError()
	def fs检查最大传输单元(self, a):
		raise NotImplementedError()
	def fs接口多协议标签交换同步(self, a):
		raise NotImplementedError()
class I开放最短路径优先虚链路(I模式):
	c模式名 = "开放最短路径优先虚链路配置模式"
	def __init__(self, a, a区域, a对端):
		I模式.__init__(self, a)
		self.m区域 = a区域
		self.m对端 = a对端
	def fs问候时间(self, a时间 = 10):
		raise NotImplementedError()
	def fs死亡时间(self, a时间 = 40):
		raise NotImplementedError()
	def fs重传时间(self, a时间 = 5):
		raise NotImplementedError()
	def fs传输时间(self, a时间 = 1):
		raise NotImplementedError()
class S开放最短路径优先邻居项:
	def __init__(self, a邻居标识, a优先级, a邻居状态, a选举状态, a死亡时间, a对端地址, a接口):
		self.m邻居标识 = a邻居标识
		self.m优先级 = a优先级
		self.m邻居状态 = a邻居状态
		self.m选举状态 = a选举状态
		self.m死亡时间 = a死亡时间
		self.m对端地址 = a对端地址
		self.m接口 = a接口
	def __str__(self):
		return 字符串.ft字符串(self.m邻居标识, self.m优先级, self.m邻居状态, self.m选举状态, self.m死亡时间, self.m对端地址, self.m接口)
#增强内部网关路由协议eigrp	======================================================

#边界网关协议bgp ================================================================
class E边界网关协议地址地址簇(enum.IntEnum):
	e单播4 = 0
	e虚拟路由4 = 1	#vrf
	e虚专网4 = 2	#vpn
	e单播6 = 10
	e虚拟路由6 = 11
	e虚专网6 = 12
class I边界网关协议(I模式):
	c模式名 = "边界网关协议配置模式"
	def __init__(self, a, a自治系统号):
		I模式.__init__(self, a)
		self.m自治系统号 = int(a自治系统号)
	#命令
	def fg模式参数(self):
		"返回自治系统号"
		return (self.m自治系统号,)
	#模式
	def f模式_对等体(self, a对等体):
		raise NotImplementedError()
	def f模式_地址簇(self, *a地址簇):
		raise NotImplementedError()
	#显示
	def f显示_路由表(self):
		raise NotImplementedError()
	def f显示_邻居(self):
		raise NotImplementedError()
	#操作
	def fs路由器号(self, a):
		raise NotImplementedError()
	def f删除地址簇(self, *a地址簇):
		raise NotImplementedError()
class I边界网关协议地址簇(I模式):
	c模式名 = "边界网关协议地址族配置模式"
	def __init__(self, a, a参数):
		I模式.__init__(self, a)
		self.m参数 = a参数
	def f模式_对等体(self, a名称):
		raise NotImplementedError()
	def f显示_路由表(self):
		raise NotImplementedError()
	def f通告网络(self, a网络号):
		raise NotImplementedError()
	def f删除网络(self, a网络号):
		raise NotImplementedError()
	def f通告接口(self, a接口):
		raise NotImplementedError()
	def f删除接口(self, a接口):
		raise NotImplementedError()
class I边界网关协议对等体(I模式):
	c模式名 = "边界网关协议对等体配置模式"
	def __init__(self, a, a对等体):
		I模式.__init__(self, a)
		self.m对等体 = a对等体
	def __str__(self):
		return str(self.m对等体)
	#操作
	def f激活(self):
		raise NotImplementedError()
	def fs远端自治系统号(self, a):
		raise NotImplementedError()
	def fs本端自治系统号(self, a):
		raise NotImplementedError()
	def fs更新源地址(self, a):
		raise NotImplementedError()
#中间系统到中间系统isis =========================================================
class I中间系统到中间系统(I模式):
	c模式名 = "中间系统到中间系统配置模式"
	def __init__(self, a, a进程号):
		I模式.__init__(self, a)
	def f显示_路由表(self):
		raise NotImplementedError()
	def f显示_邻居(self):
		raise NotImplementedError()
	def f通告接口(self, a接口):
		raise NotImplementedError()
	def f删除接口(self, a接口):
		raise NotImplementedError()
#===============================================================================
# 冗余路由
#===============================================================================
#虚拟路由器冗余协议vrrp =========================================================
class I虚拟路由器冗余协议(I模式):
	def __init__(self, a, a组号):
		I模式.__init__(self, a)
		self.m组号 = a组号
	def fs网络地址4(self, a地址):
		raise NotImplementedError()
	def fs网络地址6(self, a地址):
		raise NotImplementedError()
	def fs优先级(self, a优先级):
		raise NotImplementedError()
#===============================================================================
# 路由策略
#===============================================================================
class I路由策略组(I模式):
	def __init__(self, a, a名称):
		I模式.__init__(self, a)
		self.m名称 = a名称
	def f模式_策略(self, a动作, a策略号):
		raise NotImplementedError()
class I路由策略节点(I模式):
	def __init__(self, a, a节点号):
		I模式.__init__(self, a)
		self.m节点号 = a节点号
	#匹配
	def f匹配_访问列表(self, a访问列表, a操作 = E操作.e添加):
		raise NotImplementedError()
	def f匹配_前缀列表(self, a前缀列表, a操作 = E操作.e添加):
		raise NotImplementedError()
	#应用
	def f应用_下一跳4(self, a地址, a操作 = E操作.e添加):
		raise NotImplementedError()
	def f应用_默认下一跳4(self, a地址, a操作 = E操作.e添加):
		raise NotImplementedError()
	def f应用_出接口(self, a接口, a操作 = E操作.e添加):
		raise NotImplementedError()
	def f应用_默认出接口(self, a接口, a操作 = E操作.e添加):
		raise NotImplementedError()
	#应用 路由
	def f应用_度量值(self, a值, a操作 = E操作.e设置):
		raise NotImplementedError()
	def f应用_区域类型(self, a区域类型, a操作 = E操作.e设置):
		"用于: ospf, isis"
		raise NotImplementedError()
	def f应用_路由类型(self, a路由类型, a操作 = E操作.e设置):
		"用于: ospf, eigrp, isis"
		raise NotImplementedError()
#===============================================================================
# acl
#===============================================================================
class E访问控制列表类型(enum.IntEnum):
	"模式用"
	e标准 = 40
	e扩展 = 41
	ipv4标准 = 40
	ipv4扩展 = 41
	ipv6 = 60
class I访问控制列表端口号到字符串:
	def f等于(self, a序列):
		raise NotImplementedError()
	def f不等于(self, a序列):
		raise NotImplementedError()
	def f大于(self, a值):
		raise NotImplementedError()
	def f大于等于(self, a值):
		return self.f大于(a值 - 1)
	def f小于(self, a值):
		raise NotImplementedError()
	def f小于等于(self, a值):
		return self.f小于(a值 + 1)
	def f范围(self, a值):
		raise NotImplementedError()
class C访问控制列表端口号到字符串(I访问控制列表端口号到字符串):
	def f大于(self, a值):
		return ">" + str(a值)
	def f大于等于(self, a值):
		return "≥" + str(a值)
	def f小于(self, a值):
		return "<" + str(a值)
	def f小于等于(self, a值):
		return "≤" + str(a值)
	def f等于(self, a序列):
		return "=" + " ".join(字符串.ft字符串序列(a序列))
	def f不等于(self, a序列):
		return "≠" + " ".join(字符串.ft字符串序列(a序列))
	def f范围(self, a值: range):
		return "%d~%d" % (a值.start, a值.stop - 1)
c访问控制列表端口号到字符串 = C访问控制列表端口号到字符串()
class S访问控制列表端口号:
	def __init__(self, a值, a运算):
		self.m运算 = a运算
		self.m值 = a值
	def __str__(self):
		return self.ft字符串()
	@staticmethod
	def fc大于(a值):
		return S访问控制列表端口号(a值, 运算.f大于)
	@staticmethod
	def fc大于等于(a值):
		return S访问控制列表端口号(a值, 运算.f大于等于)
	@staticmethod
	def fc小于(a值):
		return S访问控制列表端口号(a值, 运算.f小于)
	@staticmethod
	def fc小于等于(a值):
		return S访问控制列表端口号(a值, 运算.f小于等于)
	@staticmethod
	def fc范围(a值):
		return S访问控制列表端口号(a值, 运算.f包含)
	@staticmethod
	def fc等于(*a值):	#慎用多值,只有思科支持多值
		return S访问控制列表端口号(a值, 运算.f包含)
	@staticmethod
	def fc不等于(*a值):	#慎用,只有思科支持不等于
		return S访问控制列表端口号(a值, 运算.f不包含)
	def fi范围内(self, a):
		return self.m运算(self.m值, a)
	def ft字符串(self, a接口 = c访问控制列表端口号到字符串):
		if self.m运算 == 运算.f大于:
			return a接口.f大于(self.m值)
		elif self.m运算 == 运算.f大于等于:
			return a接口.f大于等于(self.m值)
		elif self.m运算 == 运算.f小于:
			return a接口.f小于(self.m值)
		elif self.m运算 == 运算.f小于等于:
			return a接口.f小于等于(self.m值)
		elif self.m运算 == 运算.f包含:
			if type(self.m值) == range:
				return a接口.f范围(self.m值)
			else:
				return a接口.f等于(self.m值)
		elif self.m运算 == 运算.f不包含:
			return a接口.f不等于(self.m值)
		else:
			return ""
class C访问控制列表规则:
	"""成员&参数:\n
	允许: bool, 决定动作是permit还是deny\n
	协议: int, 值来自E协议\n
	源地址: S网络地址4\n
	目标地址: S网络地址4\n
	源端口: S端口\n
	目标端口: S端口"""
	#类型	--------------------------------------------------------------------
	class E端(enum.IntEnum):
		e地址 = 0
		e通配符 = 1
		e掩码 = 2
		e端口符号 = 3
		e端口 = 4
	class E协议(enum.IntEnum):
		ip = 30,
		ipv4 = 31,
		ipv6 = 32,
		tcp = 40,
		udp = 41
	class E写模式(enum.IntEnum):	#添加规则的策略
		e默认 = 0	#设备自身决定怎么处理
		e新建 = 1	#如果原来已存在则抛出异常，思科默认
		e覆盖 = 2
		e修改 = 3	#华为华三默认
	class S端口:
		def __init__(self):
			self.m符号 = C访问控制列表规则.E符号.e无
			self.m端口 = []
	#方法	--------------------------------------------------------------------
	def __init__(self, **a):
		self.m规则类型 = None
		self.m序号 = -1	#添加规则时不使用该序号,解析规则时赋值
		self.m地址类型 = None
		self.m解析 = True	#是否解析参数类型
		self.m允许 = None
		self.m协议 = C访问控制列表规则.E协议.ip
		self.m源地址 = None
		self.m目的地址 = None
		self.m源端口 = None
		self.m目的端口 = None
		self.f更新(**a)
	def f更新(self, **a):
		for k, v in C访问控制列表规则.ca更新.items():
			if k in a:
				v(self, a[k])
	def __str__(self):
		v = ""
		#序号
		if self.m序号 >= 0:
			v += "序号%d, " % (self.m序号,)
		#允许
		if self.m允许:
			v += "允许, "
		else:
			v += "拒绝, "
		#协议
		v += C访问控制列表规则.ca协议到字符串[self.m协议] + ", "
		#地址
		if self.m源地址:
			v += "源地址%s, " % (self.m源地址,)
		if self.m源端口:
			v += "源端口%s, " % (self.m源端口,)
		if self.m目的地址:
			v += "目的地址%s, " % (self.m目的地址,)
		if self.m目的端口:
			v += "目的端口%s, " % (self.m目的端口,)
		return v
	#属性
	def fs允许(self, a):
		self.m允许 = bool(a)
	def fs协议(self, a协议):
		self.m协议 = a协议
	def fs源地址(self, a地址):
		self.m源地址 = a地址
	def fs目的地址(self, a地址):
		self.m目的地址 = a地址
	def fs源端口(self, a端口):
		self.m源端口 = a端口
	def fs目的端口(self, a端口):
		self.m目的端口 = a端口
	def f匹配源地址(self, a地址):
		self.m源地址.fi范围内(a地址)
	def f匹配目的地址(self, a地址):
		self.m目的地址.fi范围内(a地址)
	def f匹配源端口(self, a端口):
		self.m源端口.fi范围内(a端口)
	def f匹配目的端口(self, a端口):
		self.m目的端口.fi范围内(a端口)
	#静态函数	-----------------------------------------------------------------
	@staticmethod
	def fi地址(a地址):
		if isinstance(a地址, 地址.S网络地址4):
			return True
		if isinstance(a地址, 地址.S网络地址6):
			return True
		if hasattr(a地址, "m地址") and hasattr(a地址, "__str__"):
			return True
		return False
	@staticmethod
	def fi端口(a端口):
		if isinstance(a端口, C访问控制列表规则.S端口):
			return True
		return False
	#解析
	@staticmethod
	def f空白转斜扛(s):
		s = re.sub(r"\b+", r"/", s)
		return s
	@staticmethod
	def f解析端口(a端口):
		v类型 = type(a端口)
		if v类型 == str:
			v位置 = 0
C访问控制列表规则.ca更新 = {
	"a允许": C访问控制列表规则.fs允许,
	"a协议": C访问控制列表规则.fs协议,
	"a源地址": C访问控制列表规则.fs源地址,
	"a目的地址": C访问控制列表规则.fs目的地址,
	"a源端口": C访问控制列表规则.fs源端口,
	"a目的端口": C访问控制列表规则.fs目的端口,
}
C访问控制列表规则.ca协议到字符串 = {
	C访问控制列表规则.E协议.ip: "互联网协议第4版",
	C访问控制列表规则.E协议.ipv6: "互联网协议第6版",
	C访问控制列表规则.E协议.tcp: "传输控制协议",
	C访问控制列表规则.E协议.udp: "用户数据报协议",
}
class I访问控制列表(I模式):
	c模式名 = "访问控制列表配置模式"
	def __init__(self, a):
		I模式.__init__(self, a)
	def fs规则(self, a序号 = None, a规则 = None, a操作 = E操作.e设置):
		raise NotImplementedError()
	def fe规则(self):
		raise NotImplementedError()
	def f应用到(self, a):
		raise NotImplementedError()
class I访问控制列表助手:
	"用来计算到目标设备的访问控制列表序号, 原始参数的n从0开始, 返回时不做类型转换"
	def f计算序号_标准4(self, n):
		return n
	def f计算序号_扩展4(self, n):
		return n
	def f计算序号_标准6(self, n):
		return n
	def f计算序号_扩展6(self, n):
		return n
	def f反算序号_标准4(self, n):
		return n
	def f反算序号_扩展4(self, n):
		return n
	def f反算序号_标准6(self, n):
		return n
	def f反算序号_扩展6(self, n):
		return n
#===============================================================================
# 前缀列表
#===============================================================================
class E前缀列表类型(enum.IntEnum):
	e版本4 = 0
	ipv4 = 0
	e版本6 = 1
	ipv6 = 1
class C前缀列表规则:
	def __init__(self, **a):
		self.m序号 = None
		self.m允许 = True
		self.m网络号 = None
		self.m最小长度 = None
		self.m最大长度 = None
		self.f更新(**a)
	def f更新(self, **a):
		for k, v in C前缀列表规则.ca更新.items():
			if k in a:
				v(self, a[k])
	def fs序号(self, a):
		self.m序号 = a
	def fs允许(self, a):
		self.m允许 = a
	def fs网络号(self, a):
		self.m网络号 = a
	def fs最小长度(self, a):
		self.m最小长度 = a
	def fs最大长度(self, a):
		self.m最大长度 = a
C前缀列表规则.ca更新 = {
	"a允许": C前缀列表规则.fs允许,
	"a网络号": C前缀列表规则.fs网络号,
	"a最小长度": C前缀列表规则.fs最小长度,
	"a最大长度": C前缀列表规则.fs最大长度,
}
class I前缀列表(I模式):
	c模式名 = "前缀列表配置模式"
	def __init__(self, a):
		I模式.__init__(self, a)
	def f添加规则(self, a序号 = None, a规则 = None):
		raise NotImplementedError()
	def f删除规则(self, a序号):
		raise NotImplementedError()
	def fe规则(self):
		raise NotImplementedError()
	def f应用到(self, a):
		raise NotImplementedError()
#===============================================================================
# 生成树
#===============================================================================
class I多生成树(I模式):
	c模式名 = "多生成树配置模式"
	def __init__(self, a):
		I模式.__init__(self, a)
	def fs开关(self, a):
		raise NotImplementedError()
	def fs实例映射(self, a实例, a虚拟局域网):
		raise NotImplementedError()
	def fs实例优先级(self, a实例, a优先级):
		raise NotImplementedError()
	def fs实例开销(self, a接口, a实例, a开销):
		raise NotImplementedError()
	def fs域名(self, a名称):
		raise NotImplementedError()
	def fs版本(self, a版本):
		raise NotImplementedError()
class I生成树接口配置模式(I接口配置模式):
	c模式名 = "生成树接口配置模式"
	def __init__(self, a, a接口):
		I接口配置模式.__init__(self, a, a接口)
	def fs根保护(self, a):
		raise NotImplementedError()
	def fs环路保护(self, a):
		raise NotImplementedError()
	def fs开销(self, a树, a开销):
		raise NotImplementedError()
#===============================================================================
# 远程连接
#===============================================================================
class I远端登入(I模式):
	def __init__(self, a):
		I模式.__init__(self, a)
	def fs端口号(self, a):
		raise NotImplementedError()
	def f开关(self, a):
		raise NotImplementedError()
class I安全外壳(I模式):
	def __init__(self, a):
		I模式.__init__(self, a)
	def f开关(self, a):
		raise NotImplementedError()
	def f生成密钥(self, a长度 = 0):
		raise NotImplementedError()
	def fs版本(self, a版本):
		raise NotImplementedError()
	def fs连接数(self, a数量):
		raise NotImplementedError()
#===============================================================================
# 端口安全
#===============================================================================
class E端口安全动作(enum.IntEnum):
	e丢弃包 = 12
	e丢弃并警告 = 11
	e关闭端口 = 0
	e暂时关闭端口 = 1
class I端口安全(I模式):
	def __init__(self, a):
		I模式.__init__(self, a)
	def f开关(self, a):
		raise NotImplementedError()
	def f模式_接口(self, a接口):
		raise NotImplementedError()
	def f应用到接口(self, a接口):
		raise NotImplementedError()
	def fs自动恢复时间(self, a时间):
		raise NotImplementedError()
	def fs地址老化时间(self, a时间):
		raise NotImplementedError()
#===============================================================================
# 地址池
#===============================================================================
class I网络协议地址池(I模式):
	def __init__(self, a, a名称):
		I模式.__init__(self, a)
		self.m名称 = a名称
	def fs地址范围(self, a开始, a结束 = None):
		raise NotImplementedError()
	def fs默认网关(self, a网关):
		raise NotImplementedError()
class I动态主机配置协议地址池(I模式):
	def __init__(self, a, a名称):
		I模式.__init__(self, a)
		self.m名称 = a名称
	def fs网络范围(self, a网络号, a掩码):
		raise NotImplementedError()
	def fs默认网关(self, a网关):
		raise NotImplementedError()
	def fs租期(self, a时间):
		raise NotImplementedError()
	def fs域名服务器(self, a地址):
		raise NotImplementedError()
#===============================================================================
# dhcp
#===============================================================================
class I动态主机配置协议(I模式):
	def __init__(self, a):
		I模式.__init__(self, a)
	def f显示_已分配地址(self):
		raise NotImplementedError()
	def f模式_地址池(self, a名称):
		raise NotImplementedError()
	def f开关(self, a):
		raise NotImplementedError()
#===============================================================================
# snma
#===============================================================================
class I简单网络管理协议(I模式):
	def __init__(self, a):
		I模式.__init__(self, a)
	def fs读字符串(self, a字符串):
		raise NotImplementedError()
	def fs写字符串(self, a字符串):
		raise NotImplementedError()
#===============================================================================
# ntp
#===============================================================================
class I网络时间协议服务器(I模式):
	def __init__(self, a):
		I模式.__init__(self, a)
	def f开关(self, a):
		raise NotImplementedError()
	def fs版本(self, a版本):
		raise NotImplementedError()
	def fs源地址(self, a地址):
		raise NotImplementedError()
	def fs广播更新(self, a):
		raise NotImplementedError()
class I网络时间协议客户端(I模式):
	def __init__(self, a):
		I模式.__init__(self, a)
	def f添加服务器地址(self, a地址):
		raise NotImplementedError()
	def f删除服务器地址(self, a地址):
		raise NotImplementedError()
	def f显示_同步信息(self):
		raise NotImplementedError()
#===============================================================================
# vrf
#===============================================================================
class I虚拟路由转发(I模式):
	def __init__(self, a):
		I模式.__init__(self, a)
#===============================================================================
# mpls
#===============================================================================
class I多协议标签交换(I模式):
	def __init__(self, a):
		I模式.__init__(self, a)
#===============================================================================
# qos
#===============================================================================
class I流量类(I模式):
	def __init__(self, a):
		I模式.__init__(self, a)
class I流量行为(I模式):
	def __init__(self, a):
		I模式.__init__(self, a)
class I流量策略(I模式):
	def __init__(self, a):
		I模式.__init__(self, a)
	def fs绑定(self, a类, a行为, a操作 = E操作.e设置):
		raise NotImplementedError()
#===============================================================================
# ipsec和ike
#===============================================================================
class E网络安全性工作模式(enum.IntEnum):
	e默认 = 0
	e传输 = 1
	e隧道 = 2
class I网络密钥交换策略(I模式):
	def __init__(self, a):
		I模式.__init__(self, a)
	def fs散列方式(self, a):
		raise NotImplementedError()
	def fs加密方式(self, a):
		raise NotImplementedError()
	def fs认证方式(self, a):
		raise NotImplementedError()
class I网络密钥交换密钥链(I模式):	#思科ike keyring,华三ike keychain
	def __init__(self, a):
		I模式.__init__(self, a)	
	def fs预共享密钥(self, a地址, a密码):
		raise NotImplementedError()
	def fd预共享密钥(self, a地址):
		raise NotImplementedError()
class I网络安全性变更集(I模式):	#ipsec transform set
	def __init__(self, a):
		I模式.__init__(self, a)
	def fs加密方式(self, a):
		raise NotImplementedError()
	def fs认证方式(self, a):
		raise NotImplementedError()
	def fs变更方式(self, a):
		raise NotImplementedError()
	def fs压缩方式(self, a):
		raise NotImplementedError()
	def fs工作模式(self, a):
		raise NotImplementedError()
class I网络安全性配置(I模式):
	def __init__(self, a):
		I模式.__init__(self, a)

#===============================================================================
# 异常
#===============================================================================
class X设备(RuntimeError):
	"所有设备异常的基类"
	def __init__(self, a消息):
		self.m消息 = str(a消息)
	def __str__(self):
		return self.m消息
class X命令(X设备):
	"无法解析的命令"
	def __init__(self, a):
		X设备.__init__(self, a)
class X执行(X设备):
	"无法正确执行的命令"
	def __init__(self, a):
		X设备.__init__(self, a)
class X模式(X设备):
	"在错误的模式执行命令"
	def __init__(self, a):
		if hasattr(a, c模式名):
			X设备.__init__(self, "无法在%s执行命令" % (a.c模式名,))
		elif type(a) == str:
			X设备.__init__(self, a)
		else:
			X设备.__init__(self, "无法执行命令")
class X输出(X设备):
	"无法解析设备输出信息"
	def __init__(self, a):
		X设备.__init__(self, a)
class X操作(X设备):
	"操作无效"
	def __init__(self, a操作):
		X设备.__init__(self, "操作 %s 无效" % (a操作))
#===============================================================================
# 其它
#===============================================================================
class E邻居信息(enum.IntEnum):
	"用于：链路层发现协议"
	e邻居名称 = 1
	e邻居描述 = 2
	e更新时间 = 3
	e本端接口 = 10
	e本端接口描述 = 11
	e对端接口 = 20
	e对端接口描述 = 21
	e管理地址类型 = 30
	e管理地址 = 31
