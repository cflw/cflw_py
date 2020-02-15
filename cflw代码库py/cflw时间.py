import time
import datetime
import math
c元 = datetime.datetime.strptime("","")	#计算机可记录的首个日期
c元年 = datetime.timedelta(days = c元.year * 365.25)	#以公元为参考
#===============================================================================
# 计算间隔的秒表
#===============================================================================
class C秒表:
	"计算开始到滴答的时间。单位：秒"
	def __init__(self):
		self.f重置()
	def f重置(self):
		"时间清零"
		self.m时间 = time.time()
	def f滴答(self):
		"返回经过的时间"
		v当前时间 = time.time()
		return v当前时间  - self.m时间
class C计时器:
	"滴答一段时间后返回true，并重新计时"
	def __init__(self, a时间 = 1, a等待 = True):
		self.f重置(a时间)
		self.fs等待(a等待)
	def f重置(self, a时间):
		self.m滴答时间 = float(a时间)
		self.m累积时间 = 0.0
		self.m上次时间 = time.time()
	def fs等待(self, a):
		if type(a) == bool:
			if a:
				self.m等待时间 = math.sqrt(self.m滴答时间) / 100.0
			else:
				self.m等待时间 = 0.0
		else:
			self.m等待时间 = float(a)
	def f滴答(self):
		v这次时间 = time.time()
		self.m累积时间 += v这次时间 - self.m上次时间
		self.m上次时间 = v这次时间
		v超过 = False
		if self.m累积时间 >= self.m滴答时间:
			if self.m累积时间 >= self.m滴答时间 * 2:
				self.m累积时间 = 0	#防止程序卡住使累积时间太大,导致计时器短时间内多次滴答
			else:
				self.m累积时间 -= self.m滴答时间
			v超过 = True
		if self.m等待时间 > 0:
			time.sleep(self.m等待时间)
		return v超过
#===============================================================================
# 阻塞
#===============================================================================
class C未来阻塞:
	'一开始确定一个时间并开始计时，滴答时阻塞，直到指定时间结束'
	def __init__(self, a时间 = 1):
		self.m秒表 = C秒表()
		self.f重置(a时间)
	def f重置(self, a时间):
		self.m等待时间 = float(a时间)
		self.m间隔 = self.m时间 / 10.0
		self.m秒表.f重置()
	def f滴答(self):
		while True:
			if self.m秒表.f滴答() < self.m等待时间:
				time.sleep(self.m间隔)
			else:
				break
class C循环阻塞:
	'用在循环语句的条件中，自动阻塞一段时间，到时间返回False跳出循环'
	def __init__(self, a时间 = 1.0, a次数 = None, a间隔 = None):	#次数只是用来计算时间间隔,实际循环次数可能比指定次数少
		self.m秒表 = C秒表()
		self.m时间 = a时间
		if a次数:
			self.m间隔 = a时间 / float(a次数)
		elif a间隔:
			self.m间隔 = a间隔
		else:
			self.m间隔 = 0.1
		self.m开始 = True
	def f滴答(self):
		if self.m开始:	#第1次总是进入循环
			self.m开始 = False
			return True
		if self.m秒表.f滴答() < self.m时间:
			time.sleep(self.m间隔)
			return True
		else:
			return False
#===============================================================================
# 格式化字符串
#===============================================================================
class C时间转字符串:
	c日期时间全数字 = '%Y%m%d%H%M%S'
	c日期时间中文 = '%Y年%m月%d日%H时%M分%S秒'
	c日期全数字 = '%Y%m%d'
	c时间全数字 = '%H%M%S'
	@staticmethod
	def f取时间(a时间):
		if a时间:
			return a时间
		else:	#空的，取现在时间
			return time.localtime()
	@staticmethod
	def f转换(a格式, a时间 = None):
		v时间 = C时间转字符串.f取时间(a时间)
		return time.strftime(a格式, v时间)
	@staticmethod
	def f日期时间全数字(a时间 = None):
		return C时间转字符串.f转换(C时间转字符串.c日期时间全数字, a时间)
	@staticmethod
	def f日期时间中文(a时间 = None):
		return C时间转字符串.f转换(C时间转字符串.c日期时间中文, a时间)
	@staticmethod
	def f日期全数字(a时间 = None):
		return C时间转字符串.f转换(C时间转字符串.c日期全数字, a时间)
	@staticmethod
	def f时间全数字(a时间 = None):
		return C时间转字符串.f转换(C时间转字符串.c时间全数字, a时间)
	@staticmethod
	def f日期分隔(a时间, a分隔符):
		pass
#===============================================================================
# 字符串转时间
#===============================================================================
class C字符串转时间:
	@staticmethod
	def f时间(a):
		v数量 = a.count(":")
		if v数量 == 0:	#时
			return time.strptime(a, "%H")
		if v数量 == 1:	#时:分
			return time.strptime(a, "%H:%M")
		if v数量 == 2:	#时:分:秒
			return time.strptime(a, "%H:%M:%S")
		raise ValueError
class C字符串转时间差:
	@staticmethod
	def f字符串格式(a字符串, a格式):
		v原始 = datetime.datetime.strptime(a字符串, a格式)
		v差 = v原始 - c元
		if "%Y" in a格式 or "%y" in a格式:	#格式里是否带有年
			return v差 + c元年
		else:
			return v差
	@staticmethod
	def f时间(a):
		v元组 = a.split(":")
		v数量 = len(v数量)
		v字典 = {}
		if v数量 >= 1:
			v字典["hours"] = float(v元组[0])
		if v数量 >= 2:
			v字典["minutes"] = float(v元组[1])
		if v数量 >= 3:
			v字典["seconds"] = float(v元组[2])
		if v数量 >= 4:
			raise ValueError
		return datetime.timedelta(**v字典)
def strptimedelta(str, format):
	return C字符串转时间差.f字符串格式(str, format)
#===============================================================================
# 时区
#===============================================================================
class S时区:
	def __init__(self, a名称, a秒):
		self.m名称 = a名称
		self.m秒 = a秒
	@staticmethod
	def fc系统时区():
		v时区名 = time.tzname[0].encode("latin-1").decode("gbk")
		v秒 = -time.timezone
		return S时区(v时区名, v秒)
	def fg时(self):
		return f总秒取时(self.m秒)
	def fg分(self):
		return f总秒取分(self.m秒)
	def fg秒(self):
		return f总秒取秒(self.m秒)
	def fg时分秒(self):
		return f总秒拆成时分秒(self.m秒)
	def fg标准时区缩写(self):
		return "GMT+" + str(self.fg时())
	def ft标准库时区(self):
		"转datetime.timezone"
		return datetime.timezone(datetime.timedelta(seconds = self.m秒), self.fg标准时区缩写())
	#c北京时间 = S时区("beijing", 26600)
#===============================================================================
# 时间计算
#===============================================================================
def f总秒取时(a秒):
	return math.floor(a秒 // 3600)
def f总秒取分(a秒):
	return math.floor(a秒 % 3600 // 60)
def f总秒取秒(a秒):
	return math.floor(a秒 % 60)
def f总秒拆成时分秒(a秒):
	v时 = f总秒取时(a秒)
	v分 = f总秒取分(a秒)
	v秒 = f总秒取秒(a秒)
	return (v时, v分, v秒)
def f总秒拆成分秒(a秒):
	v分 = a秒 // 60
	v秒 = a秒 % 60
	return (v分, v秒)
#===============================================================================
# 日期
#===============================================================================
c每月日数 = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
c每月日数_闰年 = (31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
def fi闰年(a年):
	v年 = int(a年)
	if v年 % 400:
		return True
	return (v年 % 4) and (not v年 % 100)
def fe全年月日(ai闰年 = False):
	"""(1,1)到(12,31)"""
	v月 = 1
	v每月日数 = c每月日数_闰年 if ai闰年 else c每月日数
	for v当月日数 in v每月日数:
		for v日 in range(1, v当月日数 + 1):
			yield v月, v日
		v月 += 1
