import cflw网络设备 as 设备
import cflw英语 as 英语
ca日子 = {
	设备.E日子.e一: "monday",
	设备.E日子.e二: "tuesday",
	设备.E日子.e三: "wednesday",
	设备.E日子.e四: "thursday",
	设备.E日子.e五: "friday",
	设备.E日子.e六: "saturday",
	设备.E日子.e日: "sunday",
	设备.E日子.e工作日: "weekdays",
	设备.E日子.e周末: "weekend",
	设备.E日子.e每天: "daily",
}
class C时间范围(设备.I时间范围配置模式):
	def __init__(self, a, a名称):
		设备.I时间范围配置模式.__init__(self, a)
		self.m名称 = a名称
	@staticmethod
	def f解析命令(a时间范围):
		if a时间范围.m绝对:
			v命令 = 设备.C命令("absolute")
			def f绝对时间(a元组: tuple, a字符串: str):
				nonlocal v命令
				if a元组:
					v命令 += a字符串
					v命令 += "%s:%s %s %s %s" % (a元组[3], a元组[4], a元组[2], 英语.f月份(a元组[1])[:3], a元组[0])	#时:分 日 月 年
			f绝对时间(a时间范围.m开始时间, "start")
			f绝对时间(a时间范围.m结束时间, "end")
		else:	#定期
			v命令 = 设备.C命令("periodic")
			v命令 += ca日子[a时间范围.m日子]
			def f定期时间(a元组: tuple):
				nonlocal v命令
				v命令 += "%s:%s" % (a元组[0], a元组[1])	#时:分
			f定期时间(a时间范围.m开始时间)
			v命令 += "to"
			f定期时间(a时间范围.m结束时间)
		return v命令
	def fg进入命令(self):
		return "time-range " + self.m名称
	def f执行时间范围命令(self, ai: bool, a时间范围):
		v命令 = C时间范围.f解析命令(a时间范围)
		v命令.f前置否定(ai, c不)
		self.f执行当前模式命令(v命令)
	def f添加(self, a时间范围):
		self.f执行时间范围命令(True, a时间范围)
	def f删除(self, a时间范围):
		self.f执行时间范围命令(False, a时间范围)
