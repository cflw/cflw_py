import enum
from . import cflw时间 as 时间
class E连接特性(enum.IntEnum):
	e命令行 = 0x0001
	e网页 = 0x0002
	c简单网管 = 0x0004
	e全部 = 0xffffffff
#===============================================================================
# 命令行连接接口
#===============================================================================
class I命令行连接:
	"连接接口"
	c连接特性 = E连接特性.e命令行
	def f连接(self):
		raise NotImplementedError()
	def fi连接(self):
		raise NotImplementedError()
	def f读_最新(self):#应该把没有读的内容都读出来
		"马上读内容，可能什么都没有"
		raise NotImplementedError()
	def f读_最近(self, a数量):
		"读最近几次内容，包括最新的"
		raise NotImplementedError()
	def f读_直到(self, a文本 = "", a时间 = 5):
		"一直读到某个文本时停止. 如果没有指定文本,直到读出任何内容时返回"
		v阻塞 = 时间.C循环阻塞(a时间)
		v内容 = ""
		while v阻塞.f滴答():
			v内容 += self.f读_最新()
			if (a文本 in v内容 if a文本 else bool(v内容)):
				return v内容
		return v内容
	def f写(self, a文本):#向设备传输文本
		raise NotImplementedError()
	def fs编码(self, a编码):#传输文本时使用的编码
		self.m编码 = a编码
	def f关闭(self):
		"断开连接"
		raise NotImplementedError()
class C命令行缓存:
	"把读到的内容临时存起来"
	def __init__(self, a大小 = 10):
		self.m大小 = a大小
		self.m缓存 = []
	def f存入(self, a内容):
		self.m缓存.append(a内容)
		if len(self.m缓存) > self.m大小:
			self.m缓存.pop(0)
	def f取出(self, a数量):
		assert(a数量 <= self.m大小)
		s = ""
		v数量 = len(self.m缓存)
		if v数量 > a数量:
			v数量 = a数量 
		for i in range(v数量):
			s += self.m缓存[i]
		return s
	def f存取(self, a存内容, a取数量):
		assert(a取数量 <= self.m大小)
		self.f存入(a存内容)
		return self.f取出(a取数量)
	def fs大小(self, a大小):
		self.m大小 = a大小
	def fg大小(self):
		return self.m大小
class C命令行回显:
	c连接特性 = I命令行连接.c连接特性
	def __init__(self, a连接, af输入回显, af输出回显):
		if not isinstance(a连接, I命令行连接):
			raise TypeError()
		self.m连接 = a连接
		self.mf输入回显 = C命令行回显.f处理回显函数(af输入回显)
		self.mf输出回显 = C命令行回显.f处理回显函数(af输出回显)
	def f读_最新(self):
		v内容 = self.m连接.f读_最新()
		self.mf输出回显(v内容)
		return v内容
	def f读_最近(self, a数量):
		v内容 =  self.m连接.f读_最近(a数量)
		self.mf输出回显(v内容)
		return v内容
	def f读_直到(self, a文本 = "", a时间 = 5):
		v内容 =  self.m连接.f读_直到(a文本, a时间)
		self.mf输出回显(v内容)
		return v内容
	def f写(self, a文本):
		self.mf输入回显(a文本)
		self.m连接.f写(a文本)
	def fs编码(self, a编码):
		self.m连接.fs编码(a编码)
	@staticmethod
	def f处理回显函数(af):
		if hasattr(af, "__call__"):
			return af
		if bool(af):
			import functools
			return functools.partial(print, end = '', flush = True)
		else:
			from . import cflw工具_运算 as 运算
			return 运算.f空
#===============================================================================
# 具体连接
#===============================================================================
class C网络终端(I命令行连接):
	"telnet"
	c命令行缓存大小 = 10	#最近读的10个文本
	def __init__(self, a主机, a端口号 = 23):
		self.m主机 = a主机
		self.m端口号 = a端口号
		self.m终端 = None
		self.m编码 = "utf-8"
		self.m缓存 = C命令行缓存(C网络终端.c命令行缓存大小)
	def f连接(self):
		assert(not self.m终端)
		import telnetlib
		self.m终端 = telnetlib.Telnet(self.m主机, self.m端口号)
	def fi连接(self):
		return bool(self.m终端)
	def f读_最新(self):
		v数据 = self.m终端.read_very_eager()
		v内容 = v数据.decode(self.m编码)
		if v内容:
			self.m缓存.f存入(v内容)
		return v内容
	def f读_最近(self, a数量 = 1):
		self.f读_最新()
		return self.m缓存.f取出(a数量)
	def f读_直到(self, a文本 = "", a时间 = 5):
		"""直到读出相应文本\n
如果没有指定文本，直到读出任何内容时返回。
		"""
		if a文本:	#直到读出相应文本
			return self.m终端.read_until(a文本.encode(self.m编码), a时间).decode(self.m编码)
		else:	#直到有内容出现
			v阻塞 = 时间.C循环阻塞(a时间)
			while v阻塞.f滴答():
				v内容 = self.f读_最新()
				if v内容:
					return v内容
			return v内容
	def f写(self, a文本: str):
		self.m终端.write(a文本.encode(self.m编码))
	def f关闭(self):
		self.m终端.close()
		self.m终端 = None
class C空连接(I命令行连接):
	"什么也不做"
	c连接特性 = 0xffffffff
	def f连接(self):
		pass
	def fi连接(self):
		return True
	def f读_最新(self):
		return ""
	def f读_最近(self, a数量):
		return ""
	def f写(self, a文本: str):#向设备传输文本
		v文本 = a文本.replace('\r', '\n')
		print(v文本, end = '')
	def fs编码(self, a编码):#传输文本时使用的编码
		pass
	def f关闭(self):
		pass
