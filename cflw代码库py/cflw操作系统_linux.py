import os
import os.path
import pathlib
def fi程序存在(a目录: str, a文件名: str):
	v目录 = pathlib.Path(a目录)
	v程序路径 = v目录 / a文件名
	if os.path.exists(v程序路径):
		return v程序路径
def f搜索程序路径(a文件名: str, a环境变量: str = "PATH"):
	"""搜索环境变量的程序,返回绝对路径"""
	v环境变量值 = os.environ[a环境变量]
	if ":" in v环境变量值:	#linux使用:分隔
		for v环境变量值1 in v环境变量值.split(":"):
			if v路径 := fi程序存在(v环境变量值1, a文件名):
				return v路径
	else:
		if v路径 := fi程序存在(v环境变量值, a文件名):
			return v路径
