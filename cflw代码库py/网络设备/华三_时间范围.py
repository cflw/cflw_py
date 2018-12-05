import cflw网络设备 as 设备
from 网络设备.华三_常量 import *
ca日子 = {
	设备.E日子.e一: "mon",
	设备.E日子.e二: "tue",
	设备.E日子.e三: "wed",
	设备.E日子.e四: "thu",
	设备.E日子.e五: "fri",
	设备.E日子.e六: "sat",
	设备.E日子.e日: "sun",
	设备.E日子.e工作日: "working-day",
	设备.E日子.e周末: "off-day",
	设备.E日子.e每天: "daily",
}
def f生成绝对时间(a元组: tuple)->str:
	"(年,月,日,时,分)"
	return "%s:%s %s/%s/%s" % (a元组[3], a元组[4], a元组[0], a元组[1], a元组[2])
def f生成相对时间(a元组: tuple)->str:
	"(时,分)"
	return "%s:%s" % a元组
def f生成命令(a名称: str, a时间范围: 设备.S时间范围):
	#前置
	v命令 = 设备.C命令("time-range")
	v命令 += a名称
	#参数
	if a时间范围.m绝对:
		if a时间范围.m开始时间:
			v命令 += "from " + f生成绝对时间(a时间范围.m开始时间)
		v命令 += "to " + f生成绝对时间(a时间范围.m结束时间)
	else:
		v命令 += f生成相对时间(a时间范围.m开始时间)
		v命令 += "to " + f生成相对时间(a时间范围.m结束时间)
	return v命令
class C时间范围(设备.I时间范围配置模式, 设备.C同级模式):
	def __init__(self, a, a名称: str):
		设备.I时间范围配置模式.__init__(self, a)
		self.m名称 = a名称
	def f执行时间范围命令(self, ai: bool, a时间范围: 设备.S时间范围):
		v命令 = f生成命令(self.m名称, a时间范围)
		v命令.f前置否定(ai, c不)
		self.f执行当前模式命令(v命令)
	def f添加(self, a时间范围: 设备.S时间范围):
		self.f执行时间范围命令(True, a时间范围)
	def f删除(self, a时间范围: 设备.S时间范围):
		self.f执行时间范围命令(False, a时间范围)
