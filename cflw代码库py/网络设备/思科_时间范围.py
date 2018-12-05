import cflw网络设备 as 设备
import cflw英语 as 英语
from 网络设备.思科_常量 import *
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
def f生成绝对时间(a时间元组: tuple)->str:
	"(年,月,日,时,分)"
	return "%s:%s %s %s %s" % (a元组[3], a元组[4], a元组[2], 英语.f月份(a元组[1])[:3], a元组[0])	#时:分 日 月 年
def f生成定期时间(a时间元组: tuple)->str:
	"(时,分)"
	return "%s:%s" % (a元组[0], a元组[1])	#时:分
def f生成命令(a时间范围):
	if a时间范围.m绝对:
		v命令 = 设备.C命令("absolute")
		v命令 += "start" + f生成绝对时间(a时间范围.m开始时间)
		v命令 += "end" + f生成绝对时间(a时间范围.m结束时间)
	else:	#定期
		v命令 = 设备.C命令("periodic")
		v命令 += ca日子[a时间范围.m日子]
		v命令 += f生成定期时间(a时间范围.m开始时间)
		v命令 += "to"
		v命令 += f生成定期时间(a时间范围.m结束时间)
	return v命令
class C时间范围(设备.I时间范围配置模式):
	def __init__(self, a, a名称):
		设备.I时间范围配置模式.__init__(self, a)
		self.m名称 = a名称
	def fg进入命令(self):
		return "time-range " + self.m名称
	def f执行时间范围命令(self, ai: bool, a时间范围):
		v命令 = f生成命令(a时间范围)
		v命令.f前置否定(ai, c不)
		self.f执行当前模式命令(v命令)
	def f添加(self, a时间范围):
		self.f执行时间范围命令(True, a时间范围)
	def f删除(self, a时间范围):
		self.f执行时间范围命令(False, a时间范围)
