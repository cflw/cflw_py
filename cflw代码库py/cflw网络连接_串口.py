import time
import cflw网络连接 as 连接
import serial	#pyserial
import win32pipe	#pywin32
import win32file	#pywin32
class C串口(连接.I连接):
	"serial"
	def __init__(self, a端口名, a波特率 = 9600):
		self.m串口 = serial.Serial(#下面这些参数根据情况修改
			port = a端口名,
			baudrate = a波特率,
			parity = serial.PARITY_NONE,
			stopbits = serial.STOPBITS_ONE,
			bytesize = serial.EIGHTBITS,
			timeout = 1
		)
		self.m编码 = "ascii"
		self.m缓存 = 连接.C缓存()
	def f读_最新(self):
		v数据 = b""
		while self.m串口.in_waiting > 0:
			v数据 += self.m串口.read(self.m串口.in_waiting)
			time.sleep(0.1)
		v内容 = v数据.decode(self.m编码)
		if v内容:
			self.m缓存.f存入(v内容)
		return v内容
	def f读_最近(self, a数量 = 1):
		self.f读_最新()
		return self.m缓存.f取出(a数量)
	def f写(self, a文本: str):
		self.m串口.write(a文本.encode(self.m编码))
		while self.m串口.out_waiting > 0:
			time.sleep(0.1)
		time.sleep(0.1)
	def f关闭(self):
		self.m串口.close()
class C命名管道(连接.I连接):
	def __init__(self, a名称):
		self.m管道 = None
		self.m名称 = a名称
		self.f连接(a名称)
		self.m缓存 = 连接.C缓存()
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