import string
import re
import functools
from . import cflw工具_运算 as 运算
#===============================================================================
# 常量
#===============================================================================
c换行符 = "\n"
#字符串
c字符串_半角字母数字符号 = string.ascii_letters + string.digits + string.punctuation
c字符串_全角数字 = '０１２３４５６７８９'
c字符串_全角小写字母 = 'ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ'
c字符串_全角大写字母 = 'ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ'
#编码范围，使用unicode编码
c编码范围_半角字符 = range(0x21, 0x7f)
c编码范围_全角字符 = range(0x2e80, 0xd7ff)
c编码范围_汉字 = range(0x4e00, 0x9fa6)
#正则表达式,需要编译
c正则表达式_文字 = r"[\w\u4e00-\u9fa6]"
ca汉字大小写 = [
	("一", "壹"),
	("二", "贰"),
	("三", "叁"),
	("四", "肆"),
	("五", "伍"),
	("六", "陆"),
	("七", "柒"),
	("八", "捌"),
	("九", "玖"),
	("十", "拾"),
	("百", "佰"),
	("千", "仟")
]
#===============================================================================
# 字符计算&判断
#===============================================================================
def fi半角字符(a字符):
	v编码 = ord(a字符)
	return v编码 in c编码范围_半角字符
def fi汉字(a字符):
	v编码 = ord(a字符)
	return v编码 in c编码范围_汉字
def f计算字符宽度(a字符: str):
	"汉字，全角字符算2个字符宽，tab算8个字符宽"
	v编码 = ord(a字符)
	if v编码 in c编码范围_半角字符:	#半角字符
		return 1
	elif v编码 in c编码范围_全角字符:	#全角字符
		return 2
	elif v编码 == 9:	#制表符
		return 8
	else:	#未知
		return 0
def fi闭(a字符):
	return a字符 in "[]"
def fi开(a字符):
	return a字符 in "()"
#===============================================================================
# 字符串查找&计算
#===============================================================================
def f计算字符串宽度(a字符串):
	v字符串 = str(a字符串)
	v宽度 = 0
	for v in v字符串:
		v宽度 += f计算字符宽度(v)
	return v宽度
def f统计汉字数量(a字符串):
	"统计字符串中出现的汉字的字数"
	v字符串 = str(a字符串)
	v数量 = 0
	for v in v字符串:
		if fi汉字(v):
			v数量 += 1
	return v数量
def f全部找(a字符串: str, a找: str):
	"""a找 在 a字符串 中出现位置,返回列表"""
	v列表 = []
	v位置 = 0
	while True:
		v位置 = a字符串.find(a找, v位置)
		if v位置 >= 0:
			v列表.append(v位置)
			v位置 += 1
		else:
			break
	return v列表
def fe找(a字符串: str, a找: str):
	"""返回迭代器"""
	v位置 = 0
	while True:
		v位置 = a字符串.find(a找, v位置)
		if v位置 >= 0:
			yield v位置
			v位置 += 1
		else:
			break
def f连续找最后(a字符串: str, *aa找, a开始 = 0):
	"根据要找的字符串一直往后找"
	v位置 = a开始 - 1
	for v找 in aa找:
		v位置 = a字符串.find(v找, v位置 + 1)
		if v位置 < 0:
			break
	return v位置
def fe分隔后每组长度(a字符串, a分隔):
	va分隔 = a字符串.split(a分隔)
	for v字符串 in va分隔:
		yield len(v字符串)
def f找前面匹配(aa字符串, a找, a标记 = 0):
	'从列表中找出前面与a字符串匹配的项'
	v正则 = re.compile(r"^" + a找, a标记)
	for v字符串 in aa字符串:
		if type(v字符串) != str:
			raise TypeError("元素类型必须是字符串")
		if re.search(v正则, v字符串):
			return v字符串
def fi前面匹配(a原始字符串, a查找字符串, a标记 = 0):
	v正则 = re.compile(a查找字符串, a标记)
	if re.match(v正则, a原始字符串):
		return True
	else:
		return False
def f查找_保留找到(a位置: int):
	"""保留找到值,找不到则返回None"""
	if a位置 == -1:
		return None
	else:
		return a位置
def f查找_计算偏移(a位置, a偏移: int):
	"""判断位置是否有效,有效则计算"""
	if a位置 != None:
		return a位置 + a偏移
	else:
		return None
def f找字符串之间(a字符串: str, a开始: str, a结束: str, a包含开始: bool = False, a反向查找: bool = False)->slice:
	"""找原始字符串中开始到结束字符串之间的字符串,返回切片
例如:f("a.b.c.d", "." ,".")返回slice(1,3)
	"""
	#找位置
	if a反向查找:
		if a结束:
			v结束位置 = a字符串.rfind(a结束)
			v结束位置 = f查找_保留找到(v结束位置)
		else:
			v结束位置 = None
		if a开始:
			v结束位置1 = f查找_计算偏移(v结束位置, (-len(a结束) if a结束 else -1))
			v开始位置 = a字符串.rfind(a开始, None, v结束位置1)
			v开始位置 = f查找_保留找到(v开始位置)
		else:
			v开始位置 = 0
	else:	#正向查找
		if a开始:
			v开始位置 = a字符串.find(a开始)
			v开始位置 = f查找_保留找到(v开始位置)
		else:
			v开始位置 = 0
		if a结束:
			v开始位置1 = f查找_计算偏移(v开始位置, (len(a开始) if a开始 else 1))
			v结束位置 = a字符串.find(a结束, v开始位置1)
			v结束位置 = f查找_保留找到(v结束位置)
		else:
			v结束位置 = None
	#返回
	if a包含开始 or v开始位置 == None:
		return slice(v开始位置, v结束位置)
	else:
		if a开始:
			return slice(v开始位置 + len(a开始), v结束位置)
		else:
			return slice(v开始位置, v结束位置)
def f找行开始位置(a字符串: str, a位置: int, a换行符: str = c换行符)->int:
	"""查找当前位置所在行的开始位置,不含换行符"""
	v行开始位置 = a字符串.rfind(a换行符, None, a位置)
	if v行开始位置 == -1:
		return 0
	else:
		return v行开始位置 + 1
def f找行结束位置(a字符串: str, a位置: int, a换行符: str = c换行符)->int:
	"""查找当前位置所在行的结束位置,含换行符"""
	v行结束位置 = a字符串.find(a换行符, a位置)
	if v行结束位置 == -1:
		return len(a字符串)
	else:
		return v行结束位置
def f找包含行(a字符串: str, a查找: str, a开始位置: int = 0, a换行符: str = c换行符)->slice:
	"""查找目标字符串所在的行的切片"""
	v查找位置 = a字符串.find(a查找, a开始位置)
	if v查找位置 == -1:
		return None	#找不到
	v行开始位置 = f找行开始位置(a字符串, v查找位置)
	v行结束位置 = f找行结束位置(a字符串, v查找位置)
	return slice(v行开始位置, v行结束位置)
def fe包含行(a字符串: str, a查找: str, a开始位置: int = 0, a换行符: str = c换行符):
	v位置 = a开始位置
	while True:
		v切片 = f找包含行(a字符串, a查找, v位置, a换行符)
		if v切片 == None:
			break
		yield a字符串[v切片]
		v位置 = v切片.stop
def f找上一行位置(a字符串: str, a位置: int, a换行符: str = c换行符, a循环: int = 1)->int:
	v行结束位置 = a位置
	for i in range(a循环):
		v行结束位置 = a字符串.rfind(a换行符, 0, v行结束位置)
		if v行结束位置 == -1:
			return -1	#没有上一行
		v行开始位置 = f找行开始位置(a字符串, v行结束位置)
	return v行开始位置
def f找下一行位置(a字符串: str, a位置: int, a换行符: str = c换行符, a循环: int = 1)->int:
	v行开始位置 = a位置
	for i in range(a循环):
		v行开始位置 = a字符串.find(a换行符, v行开始位置)
		if v行开始位置 == -1:
			return -1	#没有下一行
		v行开始位置 = v行开始位置 + 1
	return v行开始位置
def f找当前行切片(a字符串: str, a位置: int, a换行符: str = c换行符)->slice:
	"""定位当前行的切片"""
	v行开始位置 = a字符串.rfind(a换行符, 0, a位置) + 1	#找到换行符位置,+1才是行开始位置
	v行结束位置 = a字符串.find(a换行符, a位置)
	return slice(max(v行开始位置, 0), v行结束位置)
def f找上一行切片(a字符串: str, a位置: int, a换行符: str = c换行符, a循环: int = 1)->slice:
	"""往前定位行"""
	v行结束位置 = a位置
	for i in range(a循环):
		v行结束位置 = a字符串.rfind(a换行符, 0, v行结束位置)
		if v行结束位置 == -1:
			return None	#没有上一行
		v行开始位置 = f找行开始位置(a字符串, v行结束位置)
	return slice(v行开始位置, v行结束位置)
def f找下一行切片(a字符串: str, a位置: int, a换行符: str = c换行符, a循环: int = 1)->slice:
	"""往后定位行, 循环0次是当前行, 循环1次是下一行"""
	v行开始位置 = a位置
	for i in range(a循环):
		v行开始位置 = a字符串.find(a换行符, v行开始位置)
		if v行开始位置 == -1:
			return None	#没有下一行
		v行开始位置 = v行开始位置 + 1
		v行结束位置 = f找行结束位置(a字符串, v行开始位置)
	return slice(v行开始位置, v行结束位置)
def fi数字(a字符串: str)->bool:
	"a字符串.strip().isdigit()"
	return a字符串.strip().isdigit()
def fi连续范围(a字符串: str)->bool:
	"""为真: "a-b", "a~b" """
	if "-" in a字符串:
		v分割 = a字符串.split("-")
	elif "~" in a字符串:
		v分割 = a字符串.split("~")
	else:
		return False
	if len(v分割) != 2:
		return False
	a, b = v分割
	if not fi数字(a):
		return False
	if not fi数字(b):
		return False
	return True
def fi区间范围(a字符串: str)->bool:
	"""为真: "(a, b)", "[a, b]" """
	if not a字符串[0] in "([":
		return False
	if not a字符串[-1] in ")]":
		return False
	v分割 = a字符串[1:-1].split(",")
	if len(v分割) != 2:
		return False
	a, b = v分割
	if not fi数字(a):
		return False
	if not fi数字(b):
		return False
	return True
def f取行缩进(a行: str, a制表符长度: int = 4)->int:
	v缩进 = 0
	for i in range(len(a行)):
		c = a行[i]
		if c == ' ':
			v缩进 += 1
		elif c == '\t':
			v缩进 = v缩进 + a制表符长度 - v缩进 % a制表符长度
		else:
			break
	return v缩进
#===============================================================================
# 字符串操作,返回字符串
#===============================================================================
def f去头尾空白(a字符串: str):
	return a字符串.strip()
def f去前面(a字符串: str, a前面: str):
	"前面及更前的字符串全部去除"
	v位置 = a字符串.find(a前面)
	if v位置 > 0:
		return a字符串[v位置 + len(a前面):]
	return a字符串
def f去后面(a字符串: str, a后面: str):
	"后面及更后的字符串全部去除"
	v位置 = a字符串.rfind(a后面)
	if v位置 > 0:
		return a字符串[:v位置]
	return a字符串
def f去非十六进制数字(a字符串):
	if len(a字符串) < 2:
		v字符串 = a字符串
	elif a字符串[1] in "xX":	#去掉0x
		v字符串 = a字符串[2:]
	else:
		v字符串 = a字符串
	v字符串 =  "".join([v for v in v字符串 if v in "0123456789abcdefABCDEF"])	#提取数字
	return v字符串
def f去非数字(a字符串):
	return "".join([v for v in a字符串 if v in "0123456789"])
def f去词(a字符串, a序号, a分隔 = " "):
	va文本 = a字符串.split(a分隔)
	va文本.pop(a序号)
	return a分隔.join(va文本)
def f插入字符串(a字符串, a位置, a插入字符串):
	return a字符串[:a位置] + a插入字符串 + a字符串[a位置:]
def f隔段插入字符串(a字符串, a插入字符串, a间隔):
	"""每隔一段距离插入字符串
	a间隔 的类型可以是int或range"""
	v字符串 = str(a字符串)
	v类型 = type(a间隔)
	if v类型 == int:
		v长度 = len(a字符串)
		v余数 = v长度 % a间隔
		if v余数 == 0:	#不能包含尾
			i = v长度 - a间隔
		else:
			i = v长度 - v余数
		while i > 0:
			v字符串 = f插入字符串(v字符串, i, a插入字符串)
			i -= a间隔
	elif v类型 == range:
		v长度 = len(a字符串)
		v尾 = int(a间隔.stop)
		v头 = int(a间隔.start)
		v步进 = int(a间隔.step)
		if v头 < 0:
			v头 = v步进
		v余数 = (v尾 - v头) % v步进
		if v余数 == 0:	#不能包含尾
			i = v长度 - v步进
		else:
			i = v长度 - v余数
		while i >= v头:
			v字符串 = f插入字符串(v字符串, i, a插入字符串)
			i -= v步进
			if i == 0:
				break	#不能包含头
	else:
		raise TypeError()
	return v字符串
def f填充_(a字符串, a填充, a目标长度, af填充):
	"""af填充(a原字符串, a填充字符串)"""
	if not a填充:
		raise ValueError()
	v当前长度 = len(a字符串)
	if v当前长度 < a目标长度:
		v填充数量 = (a目标长度 - v当前长度) // len(a填充)
		return af填充(a字符串, a填充 * v填充数量)
	else:
		return a字符串
def f前面填充(a字符串, a填充, a目标长度):
	"""当a字符串长度小于a目标长度,则填充到目标长度"""
	return f填充_(a字符串, a填充, a目标长度, lambda a, b: b + a)
def f后面填充(a字符串, a填充, a目标长度):
	"""当a字符串长度小于a目标长度,则填充到目标长度"""
	return f填充_(a字符串, a填充, a目标长度, lambda a, b: a + b)
def f匹配补全(a字符串, aa字符串):
	for v字符串 in aa字符串:
		if a字符串 in v字符串:
			return v字符串
	return None
def f前面匹配补全(a字符串, aa字符串, a正则标志 = 0):
	v正则 = re.compile(r"^" + a字符串, a正则标志)
	for v字符串  in aa字符串:
		if a字符串 == v字符串:
			return v字符串
		elif re.search(v正则, v字符串):
			return v字符串
	return None
def fe字符串特定字符之间(a字符串, a字符, a开始位置 = 0):
	v字符长度 = len(a字符)
	v开始位置 = a开始位置
	v结束位置 = 0
	while True:
		v结束位置 = a字符串.find(a字符, v开始位置 + 1)
		if v结束位置 == -1:
			yield a字符串[v开始位置 : ]
		else:
			yield a字符串[v开始位置 : v结束位置]
		v开始位置 = v结束位置 + v字符长度
def f提取字符串之间(a字符串, a开始, a结束, a包含开始 = False, a反向查找 = False, a结束严谨 = True):
	"""找原始字符串中开始到结束字符串之间的字符串,找不到返回""
	例如:f("a.b.c.d", "." ,".")返回"b"
	a包含开始: 返回的字符串包含开始字符串
	a反向查找: 
	a结束严谨: 结果找不到结束就返回"", 不严谨则返回开始到字符串结尾"""
	v位置 = f找字符串之间(a字符串, a开始, a结束, a包含开始, a反向查找)
	#找不到则返回空字符串
	if v位置.start == None:
		return ""
	if v位置.stop == None:
		if not a结束:	#没有 a结束
			return a字符串[v位置.start:]
		if a结束严谨:	#有 a结束
			return ""
		return a字符串[v位置.start:]
	#正常返回
	return a字符串[v位置]
def f转大写数字(a字符串):
	v字符串 = str(a字符串)
	for v in ca汉字大小写:
		v字符串.replace(v[0], v[1])
	return v字符串
def fe分割(a字符串, a分割 = "\n", a开始位置 = 0):
	v开始位置 = a开始位置
	v长度 = len(a字符串)
	while True:
		v结束位置 = a字符串.find(a分割, v开始位置)
		if v结束位置 == -1:
			yield a字符串[v开始位置:]
			break
		else:
			yield a字符串[v开始位置 : v结束位置]
			v开始位置 = v结束位置 + 1
			if v开始位置 >= v长度:
				break
def fe按位置分割(a字符串, *aa位置, af暂回 = str.strip):
	"包含位置字符"
	v开始 = 0
	vf暂回处理 = af暂回 if af暂回 else 运算.f原值
	for v位置 in aa位置:
		if v位置 == 0:
			continue
		v结束 = v位置
		yield vf暂回处理(a字符串[v开始:v结束])
		v开始 = v结束
	yield vf暂回处理(a字符串[v开始:])	#最后一列
def fe按字符分割(a字符串, *aa字符, af暂回 = str.strip):
	"不包含分割字符"
	v开始 = 0
	vf暂回处理 = af暂回 if af暂回 else 运算.f原值
	for v字符 in aa字符:
		v结束 = a字符串.find(v字符, v开始)
		yield vf暂回处理(a字符串[v开始:v结束])
		v开始 = v结束 + 1
	if v开始 < len(a字符串):
		yield vf暂回处理(a字符串[v开始:])
def f回车处理(a字符串: str):
	"\\r后的字符会覆盖行首内容"
	va行 = []
	for v原行 in a字符串.split("\n"):
		v新行 = ""
		#遍历\r,覆盖行首
		v开始位置 = 0
		while True:
			v结束位置 = v原行.find("\r", v开始位置)
			if v结束位置 >= 0:
				v新行 = f覆盖(v新行, v原行[v开始位置 : v结束位置])
			else:
				v新行 = f覆盖(v新行, v原行[v开始位置:])
				break
			v开始位置 = v结束位置 + 1
		va行.append(v新行)
	return "\n".join(va行)
def f覆盖(a原: str, a新: str, a开始位置 = 0):
	if not a新:	#没东西不覆盖
		return a原
	v原长度 = len(a原)
	if a开始位置 > v原长度:
		raise ValueError("开始位置不能超过原字符串长度")
	v目标长度 = a开始位置 + len(a新)
	if v目标长度 > v原长度:
		return a原[0 : a开始位置] + a新
	else:
		return a原[0 : a开始位置] + a新 + a原[v目标长度:]
def f提取字符串周围(a字符串: str, a前: str, a中: str, a后: str):
	"""找包含中间的字符串,返回前后字符串.\n
找不到中间则返回"",找不到两边则取头尾\n
例如: f提取字符串周围("123 456 789", " ", "5", " ")返回" 456 " """
	#找
	if type(a中) == int:
		v位置 = a中
		v长度 = 1
	else:
		v位置 = a字符串.find(a中)
		v长度 = len(a中)
	if not v位置:
		return ""
	#前
	if type(a前) == int:
		v前 = v位置 + a前
	else:
		v前 = a字符串.rfind(a前, 0, v位置)
	if v前 < 0:
		v前 = 0
	#后
	if type(a后) == int:
		v后 = v位置 + v长度 + a后
	else:
		v后 = a字符串.find(a后, v位置 + v长度)
	#结束
	if v后 < 0:
		return a前
	else:
		return a字符串[a前: a后]
def F提取字符串周围(a前: str, a中: str, a后: str):
	return functools.partial(f提取字符串周围, a前 = a前, a中 = a中, a后 = a后)
def f提取包含行(a字符串: str, a包含: str):
	"""从字符串中提取包含指定文本的行, 返回的字符串不含换行符, 找不到则返回"" """
	for v行 in a字符串.split("\n"):
		if a包含 in v行:
			return v行
	return ""
def F提取包含行(a包含: str):
	return functools.partial(f提取包含行, a包含 = a包含)
def f提取第几行(a文本: str, a行数: int):
	"""从0开始, 超出范围则抛出异常"""
	v位置 = 0
	v行数 = 0
	while True:
		v行结束 = a文本.find("\n", v位置)
		v行 = a文本[v位置 : v行结束]
		if v行数 == a行数:
			return v行
		v位置 = v行结束 + 1
		v行数 += 1
class C推进取词:
	def __init__(self, a文本: str):
		self.ma词 = a文本.split()
		self.m数量 = len(self.ma词)
		self.i = 0
	def f取词(self)->str:
		if self.i >= self.m数量:
			return None
		return self.ma词[self.i]
	def f推进(self):
		self.i += 1
	def f取词推进(self)->str:	#先取词再推进
		if self.i >= self.m数量:
			return None
		v词 = self.ma词[self.i]
		self.i += 1
		return v词
#===============================================================================
# 字符串转换
#===============================================================================
def ft字符串(*a元组, a分隔符 = "\t"):
	v格式 = "%s" + a分隔符
	return (v格式 * len(a元组)) % a元组
def ft字符串序列(a序列):
	for v in a序列:
		yield str(v)
def ft范围(a字符串: str):
	"""支持的格式:\n
	连字符: "a-b", "a~b"\n
	区间: "(a, b)", "[a, b]" """
	v左闭 = True
	v右闭 = True
	if "-" in a字符串:
		v分割 = a字符串.split("-")
	elif "~" in a字符串:
		v分割 = a字符串.split("~")
	elif "," in a字符串:
		v左闭 = fi闭(a字符串[0])
		v右闭 = fi闭(a字符串[-1])
		v分割 = a字符串[1:-1].split(",")
	else:
		raise ValueError("无法把字符串转换成 range 对象")
	a, b = v分割
	v左 = int(a)
	if not v左闭:	#左开
		v左 += 1
	v右 = int(b)
	if v右闭:	#右闭
		v右 += 1
	return range(v左, v右)
#===============================================================================
# 文本对齐
#===============================================================================
class C文本对齐处理:
	def __init__(self, a宽度, a对齐方向 = -1):
		self.m宽度 = a宽度
		self.fs对齐方向(a对齐方向)
		self.fs边距(0, 0)
	def fs对齐方向(self, a对齐方向):
		if type(a对齐方向) in (int, float):
			self.m对齐方向 = a对齐方向
		elif type(a对齐方向) == str:
			v字符 = a对齐方向[0]
			if 'l' == v字符:
				self.m对齐方向 = -1
			elif 'r' == v字符:
				self.m对齐方向 = 1
			elif 'c' == v字符:
				self.m对齐方向 = 0
			elif '左' == v字符:
				self.m对齐方向 = -1
			elif '右' == v字符:
				self.m对齐方向 = 1
			elif '中' == v字符 or '居中' == a对齐方向[0:2]:
				self.m对齐方向 = 0
			else:
				raise ValueError
		else:
			raise TypeError
	def fs边距(self, a左边距, a右边距):
		self.m左边距 = a左边距
		self.m右边距 = a右边距
	def f处理(self, a字符串):
		'把原字符串转换成对齐后的字符串'
		v宽度 = f计算字符宽度(a字符串)
		v空格 = self.m宽度 - v宽度
		if v空格 < 0:
			raise ValueError('参数字符串的宽度超出范围')
		if self.fi左对齐():
			v处理后 = a字符串 + ' ' * v空格
		elif self.fi右对齐():
			v处理后 = ' ' * v空格 + a字符串
		return ' ' * self.m左边距 + v处理后 + ' ' * self.m右边距
	def fi左对齐(self):
		return self.m对齐方向 < 0
	def fi右对齐(self):
		return self.m对齐方向 > 0
	def fi居中对齐(self):
		return self.m对齐方向 == 0
def f数字整齐化(a数字: int, a位数: int):
	"""前面补零, 使之整齐
	f(1, 2) -> "01" 
	f(998, 2) -> "98"
	"""
	v数字 = str(a数字)
	v长度 = len(v数字)
	if v长度 < a位数:
		return "0" * (a位数 - v长度) + v数字
	elif v长度 > a位数:
		return v数字[v长度 - a位数:]
	else:
		return v数字
#===============================================================================
# 模板
#===============================================================================
class C模板:
	c匹配括号 = re.compile(r"\{" + c正则表达式_文字 + r"+\}")
	def __init__(self, s: str):
		self.m字符串 = s
		self.ma参数 = []
		v列表 = C模板.c匹配括号.findall(s)
		for v in v列表:
			self.ma参数.append((C模板.f去括号(v), v))	#添加("k", "{k}"),前者用于查找,后者用于替换
	def f替换(self, **d):
		v字符串 = self.m字符串
		for v参数 in self.ma参数:
			k = v参数[0]
			if k in d:
				v = str(d[k])
				v字符串 = v字符串.replace(v参数[1], v)
		return v字符串
	@staticmethod
	def f去括号(s: str)->str:
		return s[1:-1]
	@staticmethod
	def f加括号(s: str)->str:
		return "{" + s + "}"