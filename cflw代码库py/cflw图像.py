import enum
from PIL import Image, ImageDraw	#pillow
from . import cflw数学_向量 as 向量
from . import cflw数学_图形 as 图形
class E寻址(enum.IntEnum):
	e环绕 = enum.auto()
	e镜面 = enum.auto()
	e夹取 = enum.auto()
	e颜色 = enum.auto()
class E采样(enum.IntEnum):
	e最近点 = enum.auto()
	e线性 = enum.auto()
class E模式(enum.Enum):
	e一位 = "1"
	e灰度 = "L"
	rgb = "RGB"
	rgba = "RGBA"
	cmyk = "CMYK"
c水印掩码 = 0x03
#===============================================================================
# 图像处理
#===============================================================================
def f调整画布大小(a图像, a尺寸, a寻址 = E寻址.e环绕, a颜色 = 图形.S颜色.c黑):
	v图像 = Image.new("RGB", a尺寸, ft颜色(a颜色))
	v画图 = ImageDraw.Draw(v图像)
	v尺寸x, v尺寸y = ft尺寸(a尺寸)
	for x in range(0, v尺寸x, a图像.width):
		for y in range(0, v尺寸y, a图像.height):
			v画图.bitmap((x, y), a图像)
	return v图像
def f调整图像大小(a图像, a尺寸, a采样 = E采样.e线性):
	raise NotImplementedError()
def fs不重要像素位水印(a图像, a水印):
	v图像数据 = list(a图像.getdata())
	v水印数据 = list(a水印.getdata())
	v处理数据 = list(f像素位写0(v图像像素, v水印像素, c水印掩码) for v图像像素, v水印像素 in zip(v图像数据, v水印数据))
	v新图 = Image.new("RGB", a图像.size)
	v新图.putdata(v处理数据)
	return v新图
def fg不重要像素位水印(a图像):
	v图像数据 = list(a图像.getdata())
	v处理数据 = list(f像素位读0(v图像像素, c水印掩码) for v图像像素 in v图像数据)
	for i in range(len(v处理数据)):
		v处理数据[i] = tuple(v * 255 // c水印掩码 for v in v处理数据[i])	#颜色信号放大
	v新图 = Image.new("RGB", a图像.size)
	v新图.putdata(v处理数据)
	return v新图	
#===============================================================================
# 算法&数据结构
#===============================================================================
def f像素位写0(a像素: tuple, a写: tuple, a掩码: int):
	"多通道"
	return tuple(f像素位写1(v像素, v数据, a掩码) for v像素, v数据 in zip(a像素, a写))
def f像素位写1(a像素: int, a写: int, a掩码: int):
	"单通道"
	return (a像素 & ~a掩码) | (a写 & a掩码)
def f像素位读0(a像素: tuple, a掩码: int):
	"多通道"
	return tuple(f像素位读1(v像素, a掩码) for v像素 in a像素)
def f像素位读1(a像素: int, a掩码: int):
	"单通道"
	return a像素 & a掩码
def ft尺寸(a):
	v类型 = type(a)
	if v类型 in (向量.S向量2, 向量.S向量3, 向量.S向量4):
		return a.x, a.y
	elif v类型 in (list, tuple):
		if len(a) >= 2:
			return tuple(a)
		else:
			raise ValueError("长度必需>=2")
	else:
		raise ValueError("无法识别的类型")
def ft颜色(a):
	v类型 = type(a)
	if v类型 == 图形.S颜色:
		return tuple(int(v * 255) for v in a.fe分量())
	elif v类型 in (list, tuple):
		if len(a) >= 3:
			return tuple(a)
		else:
			raise ValueError("长度必需>=3")
	else:
		raise ValueError("无法识别的类型")