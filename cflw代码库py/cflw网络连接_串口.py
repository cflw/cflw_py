import time
from . import cflw网络连接 as 连接
import serial	#pyserial
class C串口(连接.I命令行连接):
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
		self.m缓存 = 连接.C命令行缓存()
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