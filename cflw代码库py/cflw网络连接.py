import telnetlib
import cflw时间 as 时间
class I连接:
	def f读_最新(self):#应该把没有读的内容都读出来
		"马上读内容，可能什么都没有"
		raise NotImplementedError()
	def f读_最近(self, a数量):
		"读最近几次内容，包括最新的"
		raise NotImplementedError()
	def f写(self, a文本):#向设备传输文本
		raise NotImplementedError()
	def fs编码(self, a编码):#传输文本时使用的编码
		self.m编码 = a编码
	def f关闭(self):
		"断开连接"
		raise NotImplementedError()
class C网络终端(I连接):
	"telnet"
	c缓存大小 = 10	#最近读的10个文本
	def __init__(self, a主机, a端口号 = 23):
		self.m终端 = telnetlib.Telnet(a主机, a端口号)
		self.m编码 = "ascii"
		self.m缓存 = []
	def f读_最新(self):
		v内容 = self.m终端.read_very_eager().decode(self.m编码)
		if v内容:
			self.m缓存.append(v内容)
			if len(self.m缓存) > C网络终端.c缓存大小:
				self.m缓存.pop(0)
		return v内容
	def f读_最近(self, a数量 = 1):
		assert(a数量 <= c缓存大小)
		self.f读_最新()
		s = ""
		v数量 = len(self.m缓存)
		if v数量 > a数量:
			v数量 = a数量 
		for i in range(v数量):
			s += self.m缓存[i]
		return s
	def f读_直到(self, a文本 = "", a时间 = 5):
		"""直到读出相应文本
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
	def f写(self, a文本):
		self.m终端.write(a文本.encode(self.m编码))
	def f关闭(self):
		self.m终端.close()
