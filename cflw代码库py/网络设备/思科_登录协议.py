import cflw网络设备 as 设备
from 网络设备.思科_常量 import *
import 网络设备.通用_实用 as 通用实用
import 网络设备.思科_接口 as 接口
class C网络终端(设备.I网络终端, 设备.C同级模式):
	def __init__(self, a):
		设备.I网络终端.__init__(self, a)
	def fs源接口(self, a接口, a操作 = 设备.E操作.e设置):
		v操作 = 通用实用.f解析操作(a操作)
		v命令 = 设备.C命令("ip telnet source-interface")
		if 通用实用.fi加操作(v操作):
			v接口 = 接口.f创建接口(a接口)
			v命令 += v接口
		else:
			v命令.f前面添加(c不)
		self.f执行当前模式命令(v命令)
class C安全外壳(设备.I安全外壳, 设备.C同级模式):
	def __init__(self, a):
		设备.I安全外壳.__init__(self, a)
	def f生成密钥(self, a长度 = 1024, a操作 = E操作.e设置):
		v操作 = 通用实用.f解析操作()
		v命令 = "crypto key generate rsa"
		if v操作 in (设备.E操作.e删除, 设备.E操作.e关闭):
			self.f执行当前模式命令(c不 + v命令)
			return
		v输出 = self.f执行当前模式命令(v命令)
		if "% Please define a domain-name first" in v输出:
			self.fg上级模式().fs域名()
			self.f执行当前模式命令("crypto key generate rsa")
		#% You already have RSA keys defined named xxxx.xxxx.
		#% Do you really want to replace them? [yes/no]:
		if "replace" in v输出:
			if v操作 in (设备.E操作.e设置, 设备.E操作.e修改):
				v输出 = self.m设置.f执行命令("y")
			else:
				v输出 = self.m设置.f执行命令("n")
				return
		#The name for the keys will be: xxxx.xxxx
		#Choose the size of the key modulus in the range of 360 to 4096 for your
		#   General Purpose Keys. Choosing a key modulus greater than 512 may take
		#   a few minutes.

		#How many bits in the modulus [512]:
		if "modulus" in v输出:
			self.m设置.f执行命令(a长度)
		#% Generating 1024 bit RSA keys, keys will be non-exportable...
		#[OK] (elapsed time was 6 seconds)
	def fs源接口(self, a接口, a操作 = 设备.E操作.e设置):
		v操作 = 通用实用.f解析操作(a操作)
		v命令 = 设备.C命令("ip ssh source-interface")
		if 通用实用.fi加操作(v操作):
			v接口 = 接口.f创建接口(a接口)
			v命令 += v接口
		else:
			v命令.f前面添加(c不)
		self.f执行当前模式命令(v命令)
	def fs连接数(self, a数量 = 5, a操作 = 设备.E操作.e设置):
		v操作 = 通用实用.f解析操作(a操作)
		v命令 = 设备.C命令("ip ssh maxstartups")
		if 通用实用.fi加操作(v操作):
			v命令 += a数量
		else:
			v命令.f前面添加(c不)
		self.f执行当前模式命令(v命令)
	def fs超时时间(self, a时间, a操作 = E操作.e设置):
		v操作 = 通用实用.f解析操作(a操作)
		v命令 = 设备.C命令("ip ssh time-out")
		v命令 += a时间
		if 通用实用.fi减操作(v操作):
			v命令.f前面添加(c不)
		self.f执行当前模式命令(v命令)