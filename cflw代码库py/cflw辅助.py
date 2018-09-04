import sys
#===============================================================================
# 制约
#===============================================================================
class A制约:
	"包装f(t: type)->bool"
	g异常开关 = True
	def __init__(self, f):
		self.mf = f
	def __call__(self, t):
		v = bool(self.mf(t))
		if A制约.g异常开关 and not v:
			if t.__class__ == type:	#是类型
				raise TypeError("类型 %s 违反制约 %s" % (t.__name__, self.mf.__name__))
			else:	#不是类型
				raise TypeError("类型 %s 违反制约 %s" % (type(t).__name__ , self.mf.__name__))
		return v
#===============================================================================
# 包管理
# 引用: https://my.oschina.net/chaosannals/blog/743579
#===============================================================================
g包 = {}
def A导出(a项):
	v模块 = sys.modules[a项.__module__]
	v包 = sys.modules[v模块.__package__]
	v包.__dict__[a项.__name__] = a项
	if not v包.__name__ in g包:
		g包[v包.__name__] = []
	g包[v包.__name__].append(a项.__name__)
	return a项
def f包(a名称):
	if not a名称 in g包:
		g包[a名称] = []
	return g包[a名称]