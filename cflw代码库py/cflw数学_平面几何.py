import math
from cflw数学_向量 import *
#===============================================================================
# 几何结构
#===============================================================================
class S圆形:
	def __init__(self, a坐标: S向量2, a半径: float):
		self.m坐标 = a坐标
		self.m半径 = a半径
	@staticmethod
	def fc坐标半径(a坐标: S向量2, a半径: float):
		return S圆形(a坐标, a半径)
	@staticmethod
	def fc坐标直径(a坐标: S向量2, a直径: float):
		return S圆形(a坐标, a直径 / 2)
	def f相交判定(self, a):
		if isinstance(a, S圆形):
			return f圆形相交判定(self, a)
class S矩形:
	def __init__(self, a坐标: S向量2, a半尺寸: S向量2):
		self.m坐标 = a坐标
		self.m半尺寸 = a半尺寸
	@staticmethod
	def fc坐标半尺寸(a坐标: S向量2, a半尺寸: S向量2):
		return S矩形(a坐标, a半尺寸)
	@staticmethod
	def fc坐标尺寸(a坐标: S向量2, a尺寸: S向量2):
		return S矩形(a坐标, a尺寸 / 2)
class S旋转矩形:
	def __init__(self, a坐标: S向量2, a半尺寸: S向量2, a方向: float):
		self.m坐标 = a坐标
		self.m半尺寸 = a半尺寸
		self.m方向 = a方向
	@staticmethod
	def fc坐标半尺寸(a坐标: S向量2, a半尺寸: S向量2, a方向: float = 0):
		return S旋转矩形(a坐标, a半尺寸, a方向)
	@staticmethod
	def fc坐标尺寸(a坐标: S向量2, a尺寸: S向量2, a方向: float = 0):
		return S旋转矩形(a坐标, a尺寸 / 2, a方向)
	def f相交判定(self, a):
		raise NotImplementedError()
#===============================================================================
# 相交判定函数
#===============================================================================
def f相交判定(a0, a1):
	return a0.f相交判定(a1)
def f圆形相交判定(a0: S圆形, a1: S圆形):
	v距离 = a0.m坐标.fg到点距离(a1.m坐标)
	return v距离 <= a0.m半径 + a1.m半径
def f矩形相交判定(a0: S矩形, a1: S矩形):
	v距离x = abs(a0.m坐标.x - a1.m坐标.x)
	v距离y = abs(a0.m坐标.y - a1.m坐标.y)
	if v距离x <= a0.m半尺寸.x + a1.m半尺寸.x:
		return True
	elif v距离y <= a0.m半尺寸.y + a1.m半尺寸.y:
		return True
	else:
		return False
