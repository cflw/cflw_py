import cflw网络设备 as 设备
from 网络设备.思科_常量 import *
import 网络设备.通用_实用 as 通用实用
import 网络设备.博达_接口 as 接口
class C网络终端(设备.I网络终端, 设备.C同级模式):
	def __init__(self, a):
		设备.I网络终端.__init__(self, a)
	def fs开关(self, a操作 = E操作.e设置):
		v操作 = 通用实用.f解析操作(a操作):
		if 通用实用.fi开操作(v操作):
			self.fs连接数(a操作 = 设备.E操作.e删除)
		else:
			self.fs连接数(0)
	def fs端口号(self, a端口号, a操作 = 设备.E操作.e设置):
		v操作 = 通用实用.f解析操作(a操作)
		v命令 = 设备.C命令("ip telnet listen-port")
		v命令 += a端口号
		if 通用实用.fi减操作(v操作):
			v命令.f前面添加(c不)
		self.f执行当前模式命令(v命令)
	def fs源接口(self, a接口, a操作 = 设备.E操作.e设置):
		v操作 = 通用实用.f解析操作(a操作)
		v命令 = 设备.C命令("ip telnet source-interface")
		if 通用实用.fi加操作(v操作):
			v接口 = 接口.f创建接口(a接口)
			v命令 += v接口
		else:
			v命令.f前面添加(c不)
		self.f执行当前模式命令(v命令)
	def fs连接数(self, a数量 = 5, a操作 = 设备.E操作.e设置):
		v操作 = 通用实用.f解析操作(a操作)
		v命令 = 设备.C命令("ip telnet max-user")
		if 通用实用.fi加操作(v操作):
			v命令 += a数量
		else:
			v命令.f前面添加(c不)
		self.f执行当前模式命令(v命令)
class C安全外壳(设备.I安全外壳, 设备.C同级模式):
	def __init__(self, a):
		设备.I安全外壳.__init__(self, a)
	def fs开关(self, a操作 = E操作.e设置):
		v操作 = 通用实用.f解析操作(a操作)
		v命令 = 设备.C命令("ip sshd enable")
		if 通用实用.fi减操作(v操作):
			v命令.f前面添加(c不)
		self.f执行当前模式命令(v命令)
	def f生成密钥(self, a长度 = 1024, a操作 = E操作.e设置):
		pass	#没命令
	def fs超时时间(self, a时间, a操作 = E操作.e设置):
		v操作 = 通用实用.f解析操作(a操作)
		v命令 = 设备.C命令("ip sshd timeout")
		v命令 += a时间
		if 通用实用.fi减操作(v操作):
			v命令.f前面添加(c不)
		self.f执行当前模式命令(v命令)