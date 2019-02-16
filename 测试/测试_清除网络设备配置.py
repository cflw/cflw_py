import time
import cflw网络连接_串口 as 串口
import cflw网络设备_华三 as 华三
def main():
	v连接 = 串口.C串口("COM1")
	v设备 = 华三.f创建设备(v连接, 华三.E型号.s3100, 7.1)
	v设备.fs回显(True)
	v启动模式 = v设备.f模式_启动()
	v启动模式.f登录()
	v启动模式.f清除配置()
	v启动模式.f重新启动()
	while True:
		v设备.f输出()
		time.sleep(1)
if __name__ == "__main__":
	main()