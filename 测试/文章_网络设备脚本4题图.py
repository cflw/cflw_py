import cflw网络连接 as 连接
import cflw网络设备 as 设备
import cflw网络设备_思科 as 思科
def main():
	v连接 = 连接.C网络终端("gns3.localhost", 5000)
	v设备 = 思科.f创建设备(v连接, 思科.E型号.c7200)
	v设备.fs回显(True)
	v用户 = v设备.f模式_用户()
	v全局配置 = v用户.f模式_全局配置()
	v接口配置 = v全局配置.f模式_接口配置("f0/0-1")
	v接口配置.fs描述("12345")
	v接口配置 = v全局配置.f模式_接口配置("f0-1/0")
	v接口配置.fs描述("54321")
if __name__ == "__main__":
	main()