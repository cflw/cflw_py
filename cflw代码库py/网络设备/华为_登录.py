import cflw网络设备 as 设备
import cflw工具_运算 as 运算
import cflw字符串 as 字符串
import cflw时间 as 时间
from 网络设备.华为_常量 import *
import 网络设备.通用_登录 as 通用登录
#===============================================================================
# 常量
#===============================================================================
c命令_登录配置 = "user-interface "
c命令_访问控制列表 = "acl "
c命令_登录协议 = "protocol inbound "
ca登录方式 = {
	设备.E登录方式.e控制台: "con",
	设备.E登录方式.e虚拟终端: "vty"
}
ca登录认证方式 = {
	设备.E登录认证方式.e无: "none",
	设备.E登录认证方式.e密码: "password",
	设备.E登录认证方式.e账号: "aaa",
	设备.E登录认证方式.e认证授权记账: "aaa"
}
#===============================================================================
# 解析
#===============================================================================
class S登录配置:
	def __init__(self, a文本):
		self.m文本 = a文本
		v头行尾 = self.m文本.find("\n")
		v头行 = self.m文本[:v头行尾]
		v分割 = v头行.split(" ")
		self.m方式 = 运算.f字典按值找键(ca登录方式, v分割[1])
		if len(v分割) == 4:	#是范围
			self.m范围 = range(int(v分割[2]), int(v分割[3])+1)
		else:	#不是范围
			self.m范围 = int(v分割[2])
	def __str__(self):
		return self.m文本
	def fg登录方式(self):
		return self.m方式
	def fg范围(self):
		return self.m范围
	def fg认证方式(self):
		v方式s = 字符串.f提取字符串周围(self.m文本, "\n", "login", "\n").strip()
		return 运算.f字典按值找键(ca登录认证方式, v方式s)
	def fg访问控制列表(self):
		v名称 = 字符串.f提取字符串之间(self.m文本, c命令_访问控制列表, " ")
		if v名称:
			return v名称
		else:
			return None
	def fg登录协议(self):
		v协议s = 字符串.f提取字符串之间(self.m文本, c命令_登录协议, "\n")
		if not v协议s:
			return 设备.E登录协议.e全部
		v值 = 0
		for v in v协议s.split(" "):
			k = 运算.f字典按值找键(v)
			if k:
				v值 |= k
		return v值
	def fi范围内(self, a值):
		v类型 = type(self.m范围)
		if v类型 == int:
			return self.m范围 == a值
		else:
			return a值 in self.m范围
class C登录配置表:
	def __init__(self, a文本):
		self.m文本 = a文本
	def __iter__(self):
		return self.fe节()
	def fe节(self):
		v位置0 = 0
		for v位置1 in 字符串.f重复找(self.m文本, c命令_登录配置):
			if v位置0 != v位置1:
				v文本 = self.m文本[v位置0 : v位置1]
				v位置0 = v位置1
				if not c命令_登录配置 in v文本:
					continue
				yield S登录配置(v文本)
		yield S登录配置(self.m文本[v位置1:])
#===============================================================================
# 模式
#===============================================================================
class C登录(设备.I登录配置模式):
	def __init__(self, a, a方式, a范围 = None):
		设备.I登录配置模式.__init__(self, a)
		self.m方式 = a方式
		self.m范围 = a范围
		self.m配置 = None
	#命令
	def fg进入命令(self):
		v命令 = 设备.C命令(c命令_登录配置)
		v命令 += self.fg模式参数()
		return v命令
	def fg模式参数(self):
		v登录 = (ca登录方式[self.m方式],)
		return v登录 + 通用登录.f生成范围元组(self.m方式, self.m范围)
	def f显示_当前模式配置(self):
		if self.m配置:
			return self.m配置
		self.f切换到当前模式()
		v输出 = self.m设备.f执行显示命令("display this")
		v表 = C登录配置表(v输出)
		for v in v表:
			if v.fg登录方式() != self.m方式:
				continue
			if not v.fi范围内(self.fg范围开始()):
				continue
			self.m配置 = v
			break
		return self.m配置
	#操作
	def fs认证方式(self, a认证方式):
		v命令 = 设备.C命令("authentication-mode")
		v命令 += ca登录认证方式[a认证方式]
		self.f执行当前模式命令(v命令)
	def fs访问控制列表(self, a访问列表):
		v命令 = "acl %s inbound" % (a访问列表, )
		self.f执行当前模式命令(v命令)
	def fs操作超时(self, a秒 = 600):
		v命令 = 设备.C命令("idle-timeout")
		v命令 += 时间.f总秒拆成分秒(a秒)
		self.f执行当前模式命令(v命令)
	#取
	def fg范围开始(self):
		if type(self.m范围) == range:
			return self.m范围.start
		else:	#int
			return self.m范围
	def fg认证方式(self):
		v配置 = self.f显示_当前模式配置()
		return v配置.fg认证方式()
	def fg登录协议(self):
		v配置 = self.f显示_当前模式配置()
		return v配置.fg登录协议()
	def fg访问控制列表(self):
		v配置 = self.f显示_当前模式配置()
		return v配置.fg访问控制列表()