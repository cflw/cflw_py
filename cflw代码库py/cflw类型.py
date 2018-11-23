#===============================================================================
# 类型判断
#===============================================================================
def fi类型(a):
	return a == type
def fi整数(a):
	return type(a) == int
def fi浮点数(a):
	return type(a) == float
def fi字符串(a):
	return type(a) == str
def fi函数(a):
	return hasattr(a, "__call__")
def fi迭代(a):
	return hasattr(a, "__iter__")