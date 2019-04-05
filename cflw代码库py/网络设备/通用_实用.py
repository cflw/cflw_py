import re
import math
import fractions
import cflw网络设备 as 设备
c匹配数字 = re.compile(r'(?<!\w)\d+\.?\d*(?!\w)')
c接口正则 = re.compile(r"\w+\d+(\/\d+)*(\.\d+)?")	#字母加数字就是接口
def f设备名_括号包围式(a文本):
	return a文本[1:-1]
def f设备名_前缀式(a文本):
	return re.split(r'>#(', a文本)[0]
def f时间(a周, a日, a时, a分):
	return (((int(a周) * 7 + int(a日)) * 24 + int(a时)) * 60 + int(a分)) * 60
def f取数字(a文本):
	v结果 = c匹配数字.findall(a文本)
	i = 0
	while i < len(v结果):
		if '.' in v结果[i]:
			v结果[i] = float(v结果[i])
		else:
			v结果[i] = int(v结果[i])
		i += 1
	return v结果
def f去头尾行(a文本, a头行 = 1, a尾行 = 1, a行分割符 = '\n', a转列表 = False):
	if a转列表:
		v文本 = a文本.split(a行分割符)
		if a头行:
			v文本 = v文本[a头行:]
		if a尾行:
			v文本 = v文本[:-a尾行]
		return v文本
	else:
		v头行位置 = 0
		for i in range(a头行):
			v头行位置 = a文本.find(a行分割符, v头行位置)
			if v头行位置 == -1:
				return ""
				#raise ValueError('头行位置超出范围')
			v头行位置 += 1
		v尾行位置 = len(a文本)
		for i in range(a尾行):
			v尾行位置 = a文本.rfind(a行分割符, v头行位置, v尾行位置)
			if v尾行位置 == -1:
				return ""
				#raise ValueError('尾行位置超出范围')
		return a文本[v头行位置 : v尾行位置]
def f参数等级(a, a最高):
	"不同厂商对于权限等级的定义不同。为了统一，参数限制为只能用[0,1]之间的值"
	v类型 = type(a)
	if v类型 == int:
		return v类型 * a最高
	elif v类型 == str:
		if '/' in a:	#分数
			v数字 = fractions.Fraction(a)
		else:
			v数字 = a
	else:
		v数字 = a
	return math.floor(float(v数字) * a最高 + 0.5)
def f命令补全(a, *a元组):
	v匹配程度 = 0
	v匹配字符串 = ''
	for v字符串 in a元组:
		v当前匹配程度 = 0
		for i in range(min(len(a), len(v字符串))):
			if a[i] == v字符串[i]:
				v当前匹配程度 += 1
			else:
				break
		if v当前匹配程度 > v匹配程度:
			v匹配程度 = v当前匹配程度
			v匹配字符串 = v字符串
	return v匹配字符串
def f生成开关命令(a命令, a不, a操作):
	v命令 = 设备.C命令(a命令)
	if a操作 == True or a操作 == 设备.E操作.e设置:
		pass
	elif a操作 == False or a操作 == 设备.E操作.e删除:
		v命令.f前面添加(a不)
	elif a操作 == 设备.E操作.e重置:
		v命令.f前面添加("default")
	return v命令
def f生成描述命令(a命令, a不, a描述, a操作):
	v命令 = 设备.C命令(a命令)
	if a操作 == 设备.E操作.e设置:
		v命令 += a描述
	elif a操作 == 设备.E操作.e删除:
		v命令.f前面添加(a不)
	return v命令
#操作
def f解析操作(a操作):
	v类型 = type(a操作)
	if v类型 == 设备.E操作:
		return a操作
	elif v类型 == bool:
		return 设备.E操作.e设置 if a操作 else 设备.E操作.e删除
	elif v类型 == int:
		return 设备.E操作.e设置 if a操作 else 设备.E操作.e删除
	elif v类型 == str:
		if a操作.isdigit():
			return 设备.E操作.e设置 if int(a操作) else 设备.E操作.e删除
		elif a操作 in ("no", "undo", "delete", "del"):
			return 设备.E操作.e删除
		elif a操作 in ("default", "reset"):
			return 设备.E操作.e重置
		elif a操作 in ("add",):
			return 设备.E操作.e添加
		elif a操作 in ("set",):
			return 设备.E操作.e设置
		elif a操作 == "":
			return 设备.E操作.e设置
		else:
			raise ValueError("无法解析的字符串")
	else:
		raise TypeError("无法解析的类型")
ca加操作 = (设备.E操作.e设置, 设备.E操作.e新建, 设备.E操作.e添加, 设备.E操作.e修改)
ca减操作 = (设备.E操作.e删除, 设备.E操作.e重置)
def fi加操作(a操作):
	"设置,添加,修改都是加操作"
	return a操作 in ca加操作
def fi减操作(a操作):
	return a操作 in ca减操作