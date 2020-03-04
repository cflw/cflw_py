import enum
import functools
from PIL import Image, ImageDraw	#pillow
from . import cflw数学 as 数学
from . import cflw数学_向量 as 向量
from . import cflw数学_图形 as 图形
class E定位(enum.IntEnum):
	e左上 = enum.auto()
	e中上 = enum.auto()
	e右上 = enum.auto()
	e左中 = enum.auto()
	e中间 = enum.auto()
	e右中 = enum.auto()
	e左下 = enum.auto()
	e中下 = enum.auto()
	e右下 = enum.auto()
class E寻址(enum.IntEnum):
	e环绕 = enum.auto()
	e镜面 = enum.auto()
	e夹取 = enum.auto()
	e颜色 = enum.auto()
class E采样(enum.IntEnum):
	e最近点 = enum.auto()
	e线性 = enum.auto()
class C模式:
	c二值 = "1"
	c灰度 = "L"
	c红绿蓝 = "RGB"
	c红绿蓝阿 = "RGBA"
	c印刷四色 = "CMYK"
	rgb = "RGB"
	rgba = "RGBA"
	cmyk = "CMYK"
c水印掩码 = 3
def fe坐标(a尺寸: tuple):
	for y in range(a尺寸[1]):
		for x in range(a尺寸[0]):
			yield x, y
def fc图像(a数据: list, a模式: str, a尺寸: tuple, a颜色 = 0):
	v新图 = Image.new(str(a模式), a尺寸, a颜色)
	v新图.putdata(a数据)
	return v新图
def F坐标到索引(a尺寸: tuple):
	return lambda x, y: int(y * a尺寸[0] + x)
#===============================================================================
# 简单计算
#===============================================================================
#像素
def f双像素运算m(a像素0: tuple, a像素1: tuple, af运算s):
	return tuple(af运算s(v像素1, v像素2) for v像素1, v像素2 in zip(a像素0, a像素1))
def F双像素运算m(a像素0: tuple, a像素1: tuple, af运算s):
	return functools.partial(f双像素运算m, af运算s = af运算s)
def f单像素运算m(a像素: tuple, af运算s):
	return tuple(af运算s(v像素) for v像素 in a像素)
def F单像素运算m(a像素: tuple, af运算s):
	return functools.partial(f单像素运算m, af运算s = af运算s)
#类型转换
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
def ft颜色(a颜色, a模式):
	#生成元组
	v类型 = type(a颜色)
	if v类型 == int:
		return a颜色
	elif v类型 == 图形.S颜色:
		return tuple(int(v * 255) for v in a颜色.fe分量())
	elif v类型 in (list, tuple):
		if len(a颜色) >= 3:
			return tuple(a颜色)
		else:
			raise ValueError("长度必需>=3")
	else:
		raise ValueError("无法识别的类型")
#===============================================================================
# 像素读写
#===============================================================================
def f像素写m(a像素: tuple, a写: tuple, a掩码: int):
	"多通道"
	return f双像素运算m(a像素, a写, functools.partial(f像素写s, a掩码 = a掩码))
def f像素写s(a像素: int, a写: int, a掩码: int):
	"单通道"
	return (a像素 & ~a掩码) | (a写 & a掩码)
def f像素读m(a像素: tuple, a掩码: int):
	"多通道"
	return f单像素运算m(a像素, functools.partial(f像素读s, a掩码 = a掩码))
def f像素读s(a像素: int, a掩码: int):
	"单通道"
	return a像素 & a掩码
def f颜色缩小m(a像素: tuple, a掩码: int):
	"多通道"
	return f单像素运算m(a像素, functools.partial(f颜色缩小s, a掩码 = a掩码))
def f颜色缩小s(a像素: int, a掩码: int):
	"单通道"
	return a像素 // (256 // (a掩码 + 1))
def f颜色放大m(a像素: tuple, a掩码: int):
	"多通道"
	return f单像素运算m(a像素, functools.partial(f颜色放大s, a掩码 = a掩码))
def f颜色放大s(a像素: int, a掩码: int):
	"单通道"
	return a像素 * 255 // a掩码
#===============================================================================
# 二维图像计算
#===============================================================================
def f对(af0, af1, a: tuple):
	return af0(a[0]), af1(a[1])
def f内(a坐标: int, a尺寸: int):
	return a坐标 if 数学.fi限制内(a坐标, 0, a尺寸 - 1) else None
def f计算偏移(a原尺寸: tuple, a新尺寸: tuple, a定位: E定位):
	v差x = a新尺寸[0] - a原尺寸[0]
	v差y = a新尺寸[1] - a原尺寸[1]
	if a定位 in (E定位.e左上, E定位.e左中, E定位.e左下):
		v偏移x = 0
	elif a定位 in (E定位.e中上, E定位.e中间, E定位.e中下):
		v偏移x = v差x // 2
	elif a定位 in (E定位.e右上, E定位.e右中, E定位.e右下):
		v偏移x = v差x
	if a定位 in (E定位.e左上, E定位.e中上, E定位.e右上):
		v偏移y = 0
	elif a定位 in (E定位.e左中, E定位.e中间, E定位.e右中):
		v偏移y = v差y // 2
	elif a定位 in (E定位.e左下, E定位.e中下, E定位.e右下):
		v偏移y = v差y
	return v偏移x, v偏移y
def F寻址_相对(a偏移: tuple):
	"给定新尺寸坐标, 计算出原尺寸坐标"
	return lambda x, y: (x - a偏移[0], y - a偏移[1])
def F寻址_环绕(a原尺寸: tuple, a偏移: tuple):
	vf相对 = F寻址_相对(a偏移)
	vf循环x = functools.partial(数学.f循环, a最小值 = 0, a最大值 = a原尺寸[0] - 1)
	vf循环y = functools.partial(数学.f循环, a最小值 = 0, a最大值 = a原尺寸[1] - 1)
	return lambda x, y: f对(vf循环x, vf循环y, vf相对(x, y))
def F寻址_镜面(a原尺寸: tuple, a偏移: tuple):
	vf相对 = F寻址_相对(a偏移)
	vf镜面x = functools.partial(数学.f整数镜面, a最小值 = 0, a最大值 = a原尺寸[0] - 1)
	vf镜面y = functools.partial(数学.f整数镜面, a最小值 = 0, a最大值 = a原尺寸[1] - 1)
	return lambda x, y: f对(vf镜面x, vf镜面y, vf相对(x, y))
def F寻址_夹取(a原尺寸: tuple, a偏移: tuple):
	vf相对 = F寻址_相对(a偏移)
	vf限制x = functools.partial(数学.f限制, a最小值 = 0, a最大值 = a原尺寸[0] - 1)
	vf限制y = functools.partial(数学.f限制, a最小值 = 0, a最大值 = a原尺寸[1] - 1)
	return lambda x, y: f对(vf限制x, vf限制y, vf相对(x, y))
def F寻址_颜色(a原尺寸: tuple, a偏移: tuple):
	vf相对 = F寻址_相对(a偏移)
	vf颜色x = functools.partial(f内, a尺寸 = a原尺寸[0])
	vf颜色y = functools.partial(f内, a尺寸 = a原尺寸[1])
	return lambda x, y: f对(vf颜色x, vf颜色y, vf相对(x, y))
def F取像素(a原数据: list, a原尺寸: tuple, af寻址坐标, a颜色):
	"""高级的取像素"""
	vf索引 = F坐标到索引(a原尺寸)
	def f取像素(x, y):
		vx, vy = af寻址坐标(x, y)
		if vx != None and vy != None:
			return a原数据[vf索引(vx, vy)]
		else:
			return a颜色
	return f取像素
#===============================================================================
# 通用图像处理
#===============================================================================
def f调整画布大小(a图像, a尺寸, a定位: E定位 = E定位.e左上, a寻址: E寻址 = E寻址.e颜色, a颜色: 图形.S颜色 = 图形.S颜色.c黑):
	v原尺寸 = a图像.size
	v新尺寸 = ft尺寸(a尺寸)
	v偏移 = f计算偏移(v原尺寸, v新尺寸, a定位)
	vf寻址 = {
		E寻址.e环绕: F寻址_环绕,
		E寻址.e夹取: F寻址_夹取,
		E寻址.e镜面: F寻址_镜面,
		E寻址.e颜色: F寻址_颜色,
	}[a寻址](v原尺寸, v偏移)
	v原图像 = list(a图像.getdata())
	v颜色 = ft颜色(a颜色, a图像.mode)
	vf取像素 = F取像素(v原图像, v原尺寸, vf寻址, v颜色)
	v新图像 = list(vf取像素(x, y) for x, y in fe坐标(v新尺寸))
	return fc图像(v新图像, a图像.mode, a尺寸)
def f平铺图像(a图像, a尺寸):
	"等于 f调整画布大小(a图像, a尺寸, a定位 = E定位.e左上, a寻址 = E寻址.e环绕, a颜色 = 图形.S颜色.c黑)"
	v图像 = Image.new("RGB", a尺寸, (0, 0, 0))
	v尺寸x, v尺寸y = ft尺寸(a尺寸)
	for y in range(0, v尺寸y, a图像.height):
		for x in range(0, v尺寸x, a图像.width):
			v图像.paste(a图像, (x, y))
	return v图像
def f调整图像大小(a图像, a尺寸, a采样 = E采样.e线性):
	raise NotImplementedError()
def f单图像像素运算(a图像, af运算m):
	v图像数据 = list(a图像.getdata())
	v处理数据 = list(af运算m(v图像像素) for v图像像素 in v图像数据)
	return fc图像(v处理数据, a图像.mode, a图像.size)
def f双图像像素运算_顺序(a图像0, a图像1, af运算m):
	"""逐数据运算,如果图像尺寸不同,运算的像素可能有对不上"""
	v图像数据0 = list(a图像0.getdata())
	v图像数据1 = list(a图像1.getdata())
	v处理数据 = list(af运算m(v图像像素0, v图像像素1) for v图像像素0, v图像像素1 in zip(v图像数据0, v图像数据1))
	return fc图像(v处理数据, a图像0.mode, a图像0.size)
def f双图像像素运算_对齐(a图像0, a图像1, af运算m):
	"""逐坐标运算,能保证2张图的像素坐标对得上"""
	v图像数据0 = list(a图像0.getdata())
	v图像数据1 = list(a图像1.getdata())
	vf索引0 = F坐标到索引(a图像0.size)
	vf索引1 = F坐标到索引(a图像1.size)
	def f运算(x, y):
		if x <= v宽1 and y <= v高1:
			return af运算m(v图像数据0[vf索引0(x, y)], v图像数据1[vf索引1(x, y)])
		else:
			return v图像数据0[vf索引0(x, y)]
	v处理数据 = list(f运算(x, y) for x, y in fe坐标(a图像0.size))
	return fc图像(v处理数据, a图像0.mode, a图像0.size)
#===============================================================================
# 特殊图像处理
#===============================================================================
def f添加最低有效位水印(a图像, a水印, a掩码 = c水印掩码):
	return f双图像像素运算_顺序(a图像, a水印, lambda a像素, a写: f像素写m(a像素, f颜色缩小m(a写, a掩码), a掩码))
def f提取最低有效位水印(a图像, a掩码 = c水印掩码):
	return Image.eval(a图像, lambda a像素: f颜色放大s(f像素读s(a像素, a掩码), a掩码))