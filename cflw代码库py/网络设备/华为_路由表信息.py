import cflw网络设备 as 设备
import cflw字符串 as 字符串
import cflw网络地址 as 地址
import 网络设备.华为_接口 as 接口
ca协议 = {
	"Direct": 设备.E路由协议.e直连,
	"Static": 设备.E路由协议.e静态,
	"RIP": 设备.E路由协议.e路由信息协议,
	"OSPF": 设备.E路由协议.e开放最短路径优先,
	"BGP": 设备.E路由协议.e边界网关协议,
}
class C路由表4:
	"""display ip routing-table"""
	c网络号 = 0
	c协议 = 20
	c优先级 = 28
	c开销 = 33
	c标志 = 43
	c下一跳 = 49
	c接口 = 65
	ca列开始 = (c网络号, c协议, c优先级, c开销, c标志, c下一跳, c接口)
	c标题行 = "Destination/Mask    Proto   Pre  Cost      Flags NextHop         Interface"
	def __init__(self, a文本):
		v位置 = 字符串.f连续找最后(a文本, C路由表4.c标题行, "\n")
		self.m文本 = a文本[v位置+1:]
	def __iter__(self):
		return self.fe行()
	def fe行(self):
		for v行 in self.m文本.split("\n"):
			if len(v行) < C路由表4.c接口:
				continue
			if "InLoopBack" in v行:
				continue
			v网络号s, v协议s, v优先级s, v开销s, v标志s, v下一跳s, v接口s = 字符串.fe按位置分割(v行, *C路由表4.ca列开始)
			if v网络号s:	#没有网络号是负载均衡
				v网络号 = 地址.S网络地址4.fc自动(v网络号s)
			v协议 = ca协议[v协议s]
			v优先级 = int(v优先级s)
			v开销 = int(v开销s)
			v下一跳 = 地址.S网络地址4.fc自动(v下一跳s)
			v接口 = 接口.f创建接口(v接口s)
			yield 设备.S路由条目(a网络号 = v网络号, a下一跳 = v下一跳, a出接口 = v接口, a路由协议 = v协议, a优先级 = v优先级, a度量值 = v开销)
