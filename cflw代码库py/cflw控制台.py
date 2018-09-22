import sys
import cflw字符串 as 字符串
g单行覆盖输出宽度 = 0
def f单行覆盖输出(a文本):
	"反复调用会覆盖之前输出的字符,不想覆盖了就换行"
	v宽度 = 字符串.f计算字符串宽度(a文本)
	sys.stdout.write(a文本)
	if g单行覆盖输出宽度 > v宽度:
		sys.stdout.write(" " * (g单行覆盖输出宽度 - v宽度))
		g单行覆盖输出宽度 = v宽度
	sys.stdout.write("\r")
	sys.stdout.flush()
class C参数解析器:
	class S参数属性:
		def __init__(self):
			self.m参数名 = ""
			self.m类型 = str
			self.m帮助 = ""
			self.m默认 = ""
	def __init__(self):
		self.ma参数属性 = {}
	def f添加参数(self, *aa参数, a类型 = str, a帮助 = "", a默认 = ""):
		v属性 = C参数解析器.S参数属性()
		v属性.m类型 = a类型
		v属性.m帮助 = a帮助
		v属性.m默认 = a默认
		for v参数名 in aa参数:
			v属性.m参数名 = v参数名
			self.ma参数属性[v参数名] = v属性
	def fg帮助文本(self):
		raise NotImplementedError()
	def f解析参数(self, a = None):
		#取参数
		if a == None:
			if len(sys.argv) < 2:
				return {}
			va参数 = sys.argv[1:]
		else:
			va参数 = str(a).split()
		#解析参数
		v结果 = {}
		v参数名 = None
		for v参数 in va参数:
			if v参数名 == None:
				if v参数 in self.ma参数属性:
					v参数名 = v参数
					v结果[v参数名] = None
			else:
				v结果[v参数名] = self.ma参数属性[v参数名].m类型(v参数)
				v参数名 = None
		#赋默认值
		for k, v in v结果:
			if v == None and self.ma参数属性[k].m默认:
				v结果[k] = self.ma参数属性[k].m默认
		#返回
		return v结果
class C命令解析器:
	class S命令属性:
		def __init__(self):
			self.m命令名 = ""
			self.mf命令 = None
			self.m参数名 = ""
			self.m命令帮助 = ""
	def __init__(self):
		self.ma命令属性 = {}
	def f添加命令(self, a命令名, af命令, a参数名 = "参数", a帮助 = ""):
		v属性 = S命令属性()
		v属性.m命令名 = a命令名
		v属性.mf命令 = af命令
		v属性.m参数名 = a参数名
		v属性.m命令帮助 = a帮助
		self.ma命令属性[a命令名] = v属性
	def f循环(self):
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
			self.ma命令属性[va命令[0]].mf命令(*v参数)
		except Exception as e:
			print(e)
