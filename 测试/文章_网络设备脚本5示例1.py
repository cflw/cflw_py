import cflw网络连接 as 连接
import cflw网络连接_串口 as 串口
import cflw网络设备 as 设备
import cflw网络设备_思科 as 思科
import cflw网络设备_华为 as 华为
import cflw网络设备_华三 as 华三
ca设备信息 = [
	#创建连接函数		连接参数						创建设备函数	型号				版本
	(连接.C网络终端,	("gns3.localhost", 5000),		思科.f创建设备,	思科.E型号.c7200,	15.2),
	(连接.C网络终端,	("gns3.localhost", 5001),		思科.f创建设备,	思科.E型号.l2iou,	15.1),
	(连接.C网络终端,	("ensp.localhost", 2000),		华为.f创建设备,	华为.E型号.ne40e,	8.18),
	(连接.C网络终端,	("ensp.localhost", 2001),		华为.f创建设备,	华为.E型号.s5700,	5.20),
	(串口.C命名管道,	(r"\\.\pipe\topo1-device1",),	华三.f创建设备,	华三.E型号.msr3620,	7.1),
	(串口.C命名管道,	(r"\\.\pipe\topo1-device2",),	华三.f创建设备,	华三.E型号.s5820v2,	7.1),
]
def f创建设备(a设备信息):
	v连接 = a设备信息[0](*a设备信息[1])
	v设备 = a设备信息[2](v连接, a设备信息[3], a设备信息[4])
	return v设备
def main():
	for v设备信息 in ca设备信息:
		v设备 = f创建设备(v设备信息)
		print("\n" + "=" * 40)
		v用户模式 = v设备.f模式_用户()
		v用户模式.f登录()
		v设备.fs回显(True)
		v用户模式.fs终端监视(False)
		v全局配置 = v用户模式.f模式_全局配置()
		v登录配置 = v全局配置.f模式_登录(设备.E登录方式.e虚拟终端, range(0, 5))
		v访问列表名 = v登录配置.fg访问控制列表()
		v访问列表配置 = v全局配置.f模式_访问控制列表(v访问列表名)
		v条件1 = False	#允许10.0.0.1
		c新规则 = 设备.S访问控制列表规则(a允许 = True, a源地址 = "10.0.0.1")
		for v规则 in v访问列表配置.fe规则():
			v匹配1 = v规则.f匹配(a源地址 = "10.0.0.1")
			if v匹配1 == True and v条件1 == False:
				v条件1 = True
				break
			elif v匹配1 == False and v条件1 == False:
				if v规则.m源地址.fi主机():
					v访问列表配置.fs规则(v规则.m序号, c新规则, a操作 = 设备.E操作.e修改)
				else:
					v访问列表配置.fs规则(v规则.m序号-1, c新规则, a操作 = 设备.E操作.e新建)
				v条件1 = True
				break
		if not v条件1:
			v访问列表配置.fs规则(None, c新规则, a操作 = 设备.E操作.e新建)
if __name__ == "__main__":
	main()