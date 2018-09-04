import math
#
def f循环(a值, a最小值, a最大值):
	assert(a最小值 < a最大值)
	v差 = a最大值 - a最小值
	v基本倍 = math.floor(a值 / v差)
	v循环倍 = math.ceil(a最小值 / v差)
	return a值 - v差 * (v基本倍 - v循环倍)
def f限制(a值, a最小值, a最大值):
	assert(a最小值 < a最大值)
	if a值 < a最小值:
		return a最小值
	elif a值 > a最大值:
		return a最大值
	else:
		return a值
def f插值(a0, a1, a插值):
	return a0 + (a1 - a0) * a插值
#===============================================================================
def f算术平均数(*a):
	return sum(a) / len(a)
def f几何平均数(*a):
	m = 1
	for v in a:
		m *= v
	return math.sqrt(m)
def f平方和的平方根(*a):
	return math.sqrt(sum(v ** 2 for v in a))
