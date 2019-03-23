import cflw网络连接 as 连接
import cflw网络设备 as 设备
import cflw网络设备_中兴 as 中兴
def main():
	v连接 = 连接.C网络终端("*.*.*.*")
	v设备 = 中兴.f创建设备(v连接, 中兴.E型号.zxr10_m6000)
	v设备.fs回显(True)
	v用户模式 = v设备.f模式_用户()
	v用户模式.f登录("****", "****")
	v用户模式.f提升权限()
	v全局配置 = v用户模式.f模式_全局配置()
	# for v行 in v用户模式.f显示_接口表():
	# 	if not v行.m状态:
	# 		v接口配置 = v全局配置.f模式_接口配置(v行.m接口)
	# 		v接口配置.fs描述("123")
	for v行 in v用户模式.f显示_接口表():
		if v行.m描述 == "123":
			v接口配置 = v全局配置.f模式_接口配置(v行.m接口)
			v接口配置.fs描述(a操作 = 设备.E操作.e删除)
if __name__ == "__main__":
	main()