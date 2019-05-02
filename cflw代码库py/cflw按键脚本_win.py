import ctypes
import time
import win32api	#pywin32
import win32con	#pywin32
import win32gui	#pywin32
from . import cflw数学 as 数学
from . import cflw数学_向量 as 向量
from . import cflw输入_win as 输入
#===============================================================================
# 视窗原生结构
#===============================================================================
class POINT(ctypes.Structure):
	_fields_ = [("x", ctypes.c_ulong), ("y", ctypes.c_ulong)]
#===============================================================================
# 鼠标按键
#===============================================================================
ca鼠标按键 = {
	#按键					按下							松开
	输入.E鼠标按键.e左键: (win32con.MOUSEEVENTF_LEFTDOWN, win32con.MOUSEEVENTF_LEFTUP),
	输入.E鼠标按键.e右键: (win32con.MOUSEEVENTF_RIGHTDOWN, win32con.MOUSEEVENTF_RIGHTUP),
	输入.E鼠标按键.e中键: (win32con.MOUSEEVENTF_MIDDLEDOWN, win32con.MOUSEEVENTF_MIDDLEUP),
}
def fg鼠标坐标():
	v点 = POINT()
	ctypes.windll.user32.GetCursorPos(ctypes.byref(v点))
	return 向量.S向量2(v点.x, v点.y)
def f鼠标移动到(a坐标):
	ctypes.windll.user32.SetCursorPos(int(a坐标.x), int(a坐标.y))
def f鼠标移动向(a移动):
	v坐标 = fg鼠标坐标()
	v移动 = v坐标 + a移动
	f鼠标移动到(v移动)
def f鼠标平滑移动到(a坐标, a时间 = 1, a细分 = 10):
	v开始坐标 = fg鼠标坐标()
	f鼠标平滑移动(v开始坐标, a坐标, a时间, a细分)
def f鼠标平滑移动向(a移动, a时间 = 1, a细分 = 10):
	v开始坐标 = fg鼠标坐标()
	f鼠标平滑移动(v开始坐标, v开始坐标 + a移动, a时间, a细分)
def f鼠标平滑移动(a开始坐标, a结束坐标, a时间 = 1, a细分 = 10):
	v时间间隔 = a时间 / a细分
	for i in range(1, a细分 + 1):
		v坐标 = 数学.f插值(a开始坐标, a结束坐标, i / a细分)
		f鼠标移动到(v坐标)
		time.sleep(v时间间隔)
def f鼠标按下(a按键):
	win32api.mouse_event(ca鼠标按键[a按键][0], 0, 0, 0, 0)
def f鼠标松开(a按键):
	win32api.mouse_event(ca鼠标按键[a按键][1], 0, 0, 0, 0)
def f鼠标按键(a按键, a时间 = 0):
	f鼠标按下(a按键)
	time.sleep(a时间)
	f鼠标松开(a按键)
#===============================================================================
# 键盘按键
#===============================================================================
def f键盘按下(a按键):
	win32api.keybd_event(a按键, 0, 0, 0)
def f键盘松开(a按键):
	win32api.keybd_event(a按键, 0, win32con.KEYEVENTF_KEYUP, 0)
def f键盘按键(a按键, a时间 = 0):
	f键盘按下(a按键)
	time.sleep(a时间)
	f键盘松开(a按键)