import time
from . import cflw网络连接 as 连接
import win32pipe	#pywin32
import win32file	#pywin32
class C命名管道(连接.I命令行连接):
	def __init__(self, a名称):
		self.m管道 = None
		self.m名称 = a名称
		self.f连接(a名称)
		self.m缓存 = 连接.C命令行缓存()
	def __del__(self):
		self.f关闭()
	def f连接(self, a名称):
		self.m管道 = win32file.CreateFile(
			a名称,
			win32file.GENERIC_READ | win32file.GENERIC_WRITE,
			0,
			None,
			win32file.OPEN_EXISTING,
			0,
			None
		)
		v结果 = win32pipe.SetNamedPipeHandleState(self.m管道, win32pipe.PIPE_READMODE_BYTE | win32pipe.PIPE_NOWAIT, None, None)
		if v结果 == 0:
			raise RuntimeError()
	def f读_最新(self):
		v数据 = b""
		while True:
			try:
				v结果, v读 = win32file.ReadFile(self.m管道, 65536)
				v数据 += v读
				time.sleep(0.1)
			except:	#没有数据时会抛异常,无视
				break
		v内容 = v数据.decode(self.m编码)
		if v内容:
			self.m缓存.f存入(v内容)
		return v内容
	def f读_最近(self, a数量 = 1):
		self.f读_最新()
		return self.m缓存.f取出(a数量)
	def f写(self, a文本: str):
		v长度 = len(a文本)
		for i in range(0, v长度, 8):	#分段写入
			win32file.WriteFile(self.m管道, a文本[i:i+8].encode(self.m编码))
			time.sleep(0.1)	
	def f关闭(self):
		if self.m管道:
			win32file.CloseHandle(self.m管道)
			self.m管道 = None