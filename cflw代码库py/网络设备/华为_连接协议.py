import cflw网络设备 as 设备
import 网络设备.通用_实用 as 通用实用
from 网络设备.华为_常量 import *
class C网络终端(设备.I网络终端, 设备.C同级模式):
	def __init__(self, a):
		设备.I网络终端.__init__(self, a)
	def fs开关(self, a操作):
		v操作 = 通用实用.f解析操作(a操作)
		v命令 = 设备.C命令("telnet server enable")
		v命令.f前置否定(通用实用.fi关操作(a操作), c不)
		self.f执行当前模式命令(v命令)
	def fs端口号(self, a):
		v命令 = 设备.C命令("telnet server port")
		v命令 += a
		self.f执行当前模式命令(v命令)
class C安全外壳(设备.I安全外壳, 设备.C同级模式):
	def __init__(self, a):
		设备.I安全外壳.__init__(self, a)
	def fs开关(self, a操作):
		v操作 = 通用实用.f解析操作(a操作)
		v命令 = 设备.C命令("stelnet server enable")
		v命令.f前置否定(通用实用.fi关操作(a操作), c不)
		self.f执行当前模式命令(v命令)
	def f生成密钥(self, a长度 = 1024, a操作 = 设备.E操作.e设置):
		v操作 = 通用实用.f解析操作(a操作)
		if 通用实用.fi关操作(v操作):
			raise 设备.X操作(v操作, "华为不支持删除密钥")
		v命令 = 设备.C命令("rsa local-key-pair create")
		self.f执行当前模式命令(v命令)
		#The key name will be: Huawei_Host
		#% RSA keys defined for Huawei_Host already exist.
		#Confirm to replace them? [y/n]:
		if "replace" in v输出:
			if v操作 in (设备.E操作.e设置, 设备.E操作.e修改):
				v输出 = self.m设置.f执行命令("y")
			else:
				v输出 = self.m设置.f执行命令("n")
				return
		#The range of public key size is (512 ~ 2048). 
		#NOTES: If the key modulus is greater than 512, 
		#       it will take a few minutes.
		#Input the bits in the modulus[default = 512]:
		if "modulus" in v输出:
			self.m设置.f执行命令(a长度)
		#Generating keys...
		#..........++++++++++++
		#.........++++++++++++
		#........................++++++++
		#..............++++++++
	def fs端口号(self, a端口号 = 22, a操作 = 设备.E操作.e设置):
		v操作 = 通用实用.f解析操作(a操作)
		v命令 = 设备.C命令("ssh server port")
		if 通用实用.fi加操作(v操作):
			v命令 += a端口号
		else:
			v命令.f前面添加(c不)
		self.f执行当前模式命令(v命令)
	def fs超时时间(self, a时间, a操作 = 设备.E操作.e设置):
		"设置认证超时时间"
		v操作 = 通用实用.f解析操作(a操作)
		v命令 = 设备.C命令("ssh server timeout")
		if 通用实用.fi加操作(v操作):
			v命令 += a时间
		else:
			v命令.f前面添加(c不)
		self.f执行当前模式命令(v命令)
