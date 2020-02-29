import sys
import pathlib
import time
from PIL import Image	#pillow
import cflw代码库py.cflw图像 as 图像
def main():
	v图像路径 = sys.argv[1]
	v图像 = Image.open(v图像路径)
	#处理
	v图像 = 图像.f最低有效位校验(v图像)
	#保存
	v保存路径0 = pathlib.PurePath(v图像路径)
	v时间 = time.strftime('%Y%m%d%H%M%S', time.localtime())
	v保存路径1 = pathlib.Path(v保存路径0.parent) / f"{v保存路径0.stem}_设置校验{v时间}.png"
	print(f"保存到: {v保存路径1}")
	v图像.save(v保存路径1)
if __name__ == "__main__":
	main()