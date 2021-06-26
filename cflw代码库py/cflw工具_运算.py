﻿import operator
def f原值(a):	#不做任何处理的函数
	return a
def f空(*a, **b):
	pass
def f空0():
	pass
def f空1(a0):
	pass
def f总是真(*a, **b):
	return True
def f总是假(*a, **b):
	return False
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
def f位拆分(a整数: int)->list:
	v位 = 1
	v列表 = []
	while v位 <= a整数:
		if a整数 & v位:
			v列表.append(v位)
		v位 *= 2
	return v列表
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
f包含 = operator.contains	#b in a
def f不包含(a, b):
	"not b in a"
	return not b in a
def f属于(a, b):
	"a in b"
	return a in b
def f不属于(a, b):
	"not a in b"
	return not a in b
def F包含(a):
	def f包含(b):
		return b in a
	return f包含
def F属于(a):
	def f属于(b):
		return a in b
	return f属于