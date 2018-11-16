import time
import cflw网络连接_串口 as 串口
def main():
	v连接 = 串口.C串口("com1")
	# v连接.fs编码("gb2312")
	print(v连接.f读_最新())
	while True:
		v内容 = input(">")
		v连接.f写(v内容 + "\n")
		time.sleep(1)
		print(v连接.f读_最新())
if __name__ == "__main__":
	main()