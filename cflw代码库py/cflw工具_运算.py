import operator
def f原值(a):	#不做任何处理的函数
	return a
def f空(*a, **b):
	pass
def f空0():
	pass
def f空1(a0):
	pass
#比较
f等于 = operator.eq
f不等于 = operator.ne
f小于 = operator.lt
f大于 = operator.gt
f小于等于 = operator.le
f大于等于 = operator.ge
def f比较(a, b):
	if hasattr(a, "__cmp__"):
		return a.__cmp__(b)
	if a > b:
		return 1
	if a < b:
		return -1
	return 0
def f反比较(a, b):
	if hasattr(a, "__cmp__"):
		return -a.__cmp__(b)
	if a > b:
		return -1
	if a < b:
		return 1
	return 0
#逻辑运算
def f且(a, b):
	return a and b
def f或(a, b):
	return a or b
f非 = operator.not_
f真 = operator.truth
f是 = operator.is_
f不是 = operator.is_not
#位运算
f位与 = operator.and_
f位或 = operator.or_
f位异或 = operator.xor
f位反 = operator.invert
#四则运算
f加 = operator.add
f减 = operator.sub
f乘 = operator.mul
f除 = operator.truediv
f正 = operator.pos
f负 = operator.neg
f乘方 = operator.pow
f矩乘 = operator.matmul
#序列运算
f包含 = operator.contains
def f不包含(a, b):
	return not b in a
