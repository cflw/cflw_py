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
def f字典按值找键(a字典: dict, a值):
	for v键, v值 in a字典.items():
		if v值 == a值:
			return v键
	return None
f包含 = operator.contains
def f不包含(a, b):
	return not b in a
def f整数位与键为真则添加值(a整数, a字典):
	v列表 = []
	for k, v in a字典.items():
		if a整数 & k:
			v列表.append(v)
	return v列表