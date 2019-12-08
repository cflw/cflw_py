import re
from . import cflw时间 as 时间
from . import cflw字符串 as 字符串
#身份证正则和区域信息 https://raw.githubusercontent.com/jayknoxqu/id-number-util/master/constant.py
c十五位身份证正则 = re.compile(r"[1-9]\d{5}\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{2}")
c十八位身份证正则 = re.compile(r"[1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]")
#取身份证信息
def fg区域(a号码: str):
	return int(a号码[:6])
def fg年(a号码: str):
	return int(a号码[6: 10])
def fg月(a号码: str):
	return int(a号码[10: 12])
def fg日(a号码: str):
	return int(a号码[12: 14])
def fg性别(a号码: str):
	return int(a号码[16]) % 2
def fg校验码(a号码: str):
	return a号码[17]
def fs月(a号码, a月):
	return a号码[:10] + 字符串.f数字整齐化(a月, 2) + a号码[12:]
def fs日(a号码, a日):
	return a号码[:12] + 字符串.f数字整齐化(a月, 2) + a号码[14:]
def fs月日(a号码, a月, a日):
	return a号码[:10] + 字符串.f数字整齐化(a月, 2) + 字符串.f数字整齐化(a日, 2) + a号码[14:]
#计算
def f计算校验码(a号码: str):
	"""计算第18位
	a号码: 17位号码,18位号码"""
	v校验和 = 0
	for i in range(17):
		v校验和 += ((1 << (17 - i)) % 11) * int(a号码[i])
	v校验码 = (12 - (v校验和 % 11)) % 11
	return str(v校验码) if v校验码 < 10 else "X"
def f验证身份证号(a号码: str):
	v校验码 = f计算校验码(a号码)
	return a号码[17] == v校验码
def fe补全出生月日(a号码: str):
	"""补全出生月日, 适用于:火车票
	a号码: 18位身份证号,出生月日随意"""
	v年 = fg年(a号码)
	for v月, v日 in 时间.fe全年月日(时间.fi闰年(v年)):
		v号码 = fs月日(a号码, v月, v日)
		if f验证身份证号(v号码):
			yield v号码