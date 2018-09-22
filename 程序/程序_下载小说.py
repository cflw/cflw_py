import sys
import pathlib
import os.path
import cflw小说下载 as 小说下载
import cflw小说下载_求书网 as 求书网
import cflw小说下载_笔趣看 as 笔趣看
import cflw小说下载_顶点小说 as 顶点小说
c版权 = "下载小说 (c)2018 cflw"
g保存路径 = pathlib.Path(sys.argv[0]).parent
class C命令解析器:
	def __init__(self):
		self.m横幅 = c版权 + os.linesep + '''输入"帮助"显示帮助'''
		self.ma命令 = {
			"下载": self.f命令_下载,
			"退出": self.f命令_退出,
			"路径": self.f命令_路径,
			"帮助": self.f命令_帮助,
		}
	def f循环(self):
		print(self.m横幅)
		while True:
			v输入 = input(">")
			self.f解析命令(v输入)
	def f解析命令(self, a命令: str):
		va命令 = a命令.split()
		if len(va命令) > 1:
			v参数 = tuple(va命令[1:])
		else:
			v参数 = ()
		try:
			self.ma命令[va命令[0]](*v参数)
		except Exception as e:
			print(e)
	def f命令_下载(self, a地址):
		for v模块 in (求书网, 笔趣看, 顶点小说):
			if v模块.c地址 in a地址:
				v小说 = v模块.f获取小说(a地址)
				小说下载.f一键下载(v小说, g保存路径)
	def f命令_退出(self):
		exit()
	def f命令_路径(self, a路径 = ""):
		global g保存路径
		if a路径:
			g保存路径 = pathlib.Path(a路径)
		print(g保存路径)
	def f命令_帮助(self):
		print("""
下载 地址\t\t下载小说
路径 [路径]\t\t获取/设置保存路径
帮助\t\t\t显示帮助
退出\t\t\t退出程序
""")
g命令解析器 = C命令解析器()
def main():
	g命令解析器.f循环()
if __name__ == "__main__":
	main()