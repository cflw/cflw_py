import cflw网络设备 as 设备
import cflw网络地址 as 地址
c版本4 = "ip"
c版本6 = "ipv6"
c不 = "no"
class C前缀列表(设备.I前缀列表, 设备.C同级模式):
	def __init__(self, a, a名称, a版本, t地址):
		设备.I前缀列表.__init__(self, a)
		self.m名称 = a名称
		self.m版本 = a版本
		if not t地址 in (地址.S网络地址4, 地址.S网络地址6):
			raise TypeError()
		self.t地址 = t地址
		self.c最大前缀长度 = t地址.c最大前缀长度
	def f生成命令(self, a序号 = None, a规则 = None):
		v命令 = 设备.C命令()
		v命令 += "%s prefix-list %s" % (self.m版本, self.m名称)
		if a序号:
			v命令 += "seq %d" % (a序号,)
		if a规则:
			if not a序号 and a规则.m序号:
				v命令 += "seq %d" % (a规则.m序号,)
			v命令 += "permit %s/%d" % (a规则.m网络号.fg网络号s(), a规则.m网络号.fg前缀长度())
			if a规则.m最小长度:
				v命令 += "ge %d" % (a规则.m最小长度,)
			if a规则.m最大长度:
				v命令 += "le %d" % (a规则.m最大长度,)
		return v命令
	def f添加规则(self, a序号, a规则):
		v命令 = self.f生成命令(a序号, a规则)
		self.f执行当前模式命令(v命令)
	def f删除规则(self, a序号):
		raise NotImplementedError("删除规则需要完整规则")
		v命令 = self.f生成命令(a序号)
		v命令.f前面添加(c不)
		self.f执行当前模式命令(v命令)
	