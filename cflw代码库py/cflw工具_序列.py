#===============================================================================
# 序列
#===============================================================================
def fe如果(af判断, a序列):
	for v元素 in a序列:
		if af判断(v元素):
			yield v元素
def f折叠(af运算, a初始值, a序列):
	v结果 = a初始值
	for v元素 in a序列:
		v结果 = af运算(v结果, v元素)
	return v结果
def f映射(af运算, a序列):
	for v元素 in a序列:
		yield af运算(v元素)
#===============================================================================
# 字典
#===============================================================================
def f字典按值找键(a字典: dict, a值):
	for v键, v值 in a字典.items():
		if v值 == a值:
			return v键
	return None
def f整数位与键为真则添加值(a整数, a字典):
	v列表 = []
	for k, v in a字典.items():
		if a整数 & k:
			v列表.append(v)
	return v列表
def f字典键值反转(a字典):
	return dict(zip(a字典.values(), a字典.keys()))
def f字典有键则运算(a字典, a键, af运算):
	if a键 in a字典:
		return af运算(a字典[a键])
	return None
#===============================================================================
# 切片
#===============================================================================
def F切片(a开始, a结束, a间距 = None):
	def f切片(a序列):
		return a序列[slice(a开始, a结束, a间距)]
	return f切片
class C切片组:
	"""指定一组序号,按索引取切片"""
	def __init__(self, *aa索引):
		if aa索引[0] == 0:
			self.ma索引 = aa索引
		else:
			self.ma索引 = (0,) + aa索引
		self.m长度 = len(self.ma索引)
	def __getitem__(self, k):
		return self.fg切片(k)
	def __iter__(self):
		for i in range(self.m长度):
			yield self.fg切片(i)
	def fg切片(self, k):
		if self.m长度 > k + 1:
			return slice(self.ma索引[k], self.ma索引[k+1])
		elif self.m长度 == k + 1:
			return slice(self.ma索引[k], None)
		else:
			raise IndexError()
	def F切片(self, k):
		v切片 = self.fg切片(k)
		def f切片(a序列):
			return a序列[v切片]
		return f切片
	def F多切片(self, *k):
		va切片 = list(self.fg切片(kk) for kk in k)
		def f切片(a序列):
			return (a序列[v切片] for v切片 in va切片)
		return f切片