import cflw网络连接 as 连接
import cflw网络地址 as 地址
import cflw网络设备 as 设备
import cflw网络设备_华为 as 华为
def main():
	v连接 = 连接.C网络终端("ensp.localhost", 2000)
	v设备 = 华为.f创建设备(v连接, 华为.E型号.s5700)
	v设备.fs回显(True)
	v用户 = v设备.f模式_用户()
	v用户.fs终端监视(False)
	v全局配置 = v用户.f模式_全局配置()
	v序号 = 10
	for i in range(1, 25, 4):
		v接口 = 设备.S接口.fc标准(设备.E接口.e千兆以太网, 0, 0, range(i, i+4))
		v接口配置0 = v全局配置.f模式_虚拟局域网(v接口)
		v接口配置0.fs链路类型(设备.E链路类型.e接入)
		v虚拟局域网 = v全局配置.f模式_虚拟局域网(v序号)
		v虚拟局域网.fs端口(v接口, a操作 = 设备.E操作.e添加)
		v虚拟接口 = 设备.S接口.fc标准(设备.E接口.e虚拟局域网, v序号)
		v接口配置1 = v全局配置.f模式_接口配置(v虚拟接口)
		v接口配置1.fs网络地址4(地址.S网络地址4.fc四段(10, 0, v序号, 1, 24))
		v序号 += 1
if __name__ == "__main__":
	main()