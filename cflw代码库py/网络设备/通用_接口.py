import cflw网络设备 as 设备
#接口展开
def fe接口模式展开(a接口模式):
	for v接口 in a接口模式.m接口.fe接口():
		v接口模式 = copy.copy(a接口模式)
		v接口模式.m模式栈 = a接口模式.m模式栈[:-1] + (v接口模式,)
		v接口模式.m接口 = v接口
		yield v接口模式
def A接口自动展开(af):
	def fi展开(self):
		if not self.m接口.fi范围():
			return False
		elif hasattr(self, "mi接口自动展开"):
			return bool(self.mi接口自动展开)
		else:
			return True
	def f包装(self, *a元组, **a字典):
		if fi展开(self):
			for v接口模式 in fe接口模式展开(self):
				af(v接口模式, *a元组, **a字典)
		else:
			return af(self, *a元组, **a字典)
	return f包装
