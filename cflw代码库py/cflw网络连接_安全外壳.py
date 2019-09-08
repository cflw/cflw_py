import time
import paramiko	#paramiko
#import pexpect	#pexpect
from . import cflw网络连接 as 连接
class C安全外壳2(连接.I命令行连接):	#使用paramiko
	def __init__(self, a主机, a端口号 = 22, a用户名 = "", a密码 = "", a超时 = 10):
		self.m客户端 = paramiko.SSHClient()
		self.m客户端.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
		#连接
		self.m主机 = a主机
		self.m端口号 = a端口号
		self.m用户名 = a用户名
		self.m密码 = a密码
		self.m超时 = a超时
		#其它
		self.m编码 = "ascii"
		self.m缓存 = 连接.C命令行缓存()
	def f连接(self):
		self.m客户端.connect(hostname = self.m主机, port = self.m端口号, username = self.m用户名, password = self.m密码, timeout = self.m超时)
		self.m频道 = self.m客户端.invoke_shell(width = 10000, height = 10000)
	def f读_最新(self):
		v数据 = b""
		while self.m频道.recv_ready():
			v数据 += self.m频道.recv(1024)
			time.sleep(0.1)
		v内容 = v数据.decode(self.m编码)
		self.m缓存.f存入(v内容)
		return v内容
	def f读_最近(self, a数量 = 1):
		self.f读_最新()
		return self.m缓存.f取出(a数量)
	def f写(self, a文本):
		self.m频道.send(a文本.encode(self.m编码))
	def f关闭(self):
		self.m客户端.close()
