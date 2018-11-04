import string
import cflw网络设备 as 设备
c明文 = 0
c强密文 = 5
c弱密文 = 7
c密码 = "password"
c秘密 = "secret"
ca强加密级别映射 = {
	0: c秘密,
	5: c秘密,
	7: c密码,
}
ca弱加密级别映射 = {
	0: c密码,
	5: c秘密,
	7: c密码,
}
@staticmethod
def f提取密码0(a字符串: str):
	v开始位置 = a字符串.find(c密码)
	v加密命令 = c密码
	if not v开始位置:
		v开始位置 = a字符串.find(c秘密)
		v加密 = c秘密
	v加密命令长度 = len(v加密命令)
	if a字符串[v加密命令长度 + 2] == ' ':
		v加密级别 = int(a字符串[v加密命令长度 + 1])
		v密码位置 = v加密命令长度 + 3
	else:
		v加密级别 = 0
		v密码位置 = v加密命令长度 + 1
	v结束位置 = a字符串.find("\n", v位置)
	return a字符串[v开始位置 : v结束位置]
class C弱密码助手(设备.I密码助手):
	"尽量使用明文密码或弱密码"
	@staticmethod
	def f生成密码(a密码, a加密级别 = c明文):
		v密码 = a密码
		v加密级别 = a加密级别
		if v加密级别 == 7:
			v密码 = f解密7(v密码)
			v加密级别 = 0
		return C包装(ca弱加密级别映射[v加密级别], v加密级别, v密码)	
	f提取密码 = f提取密码0
class C强密码助手(设备.I密码助手):
	"尽量使用强加密密码"
	@staticmethod
	def f生成密码(a密码, a加密级别 = c明文):
		v密码 = a密码
		v加密级别 = a加密级别
		if v加密级别 == 7:
			v密码 = f解密7(v密码)
			v加密级别 = 0
		return C包装(ca强加密级别映射[v加密级别], v加密级别, v密码)
	f提取密码 = f提取密码0
class C包装:
	def __init__(self, a加密级别命令, a加密级别数字, a密码):
		self.m命令 = a加密级别命令
		self.m数字 = a加密级别数字
		self.m密码 = a密码
	def __str__(self):
		return "%s %s %s" % (self.m命令, self.m数字, self.m密码)
#===============================================================================
# 思科类型7密码解密
# 思科相关页面: https://www.cisco.com/c/en/us/support/docs/security-vpn/remote-authentication-dial-user-service-radius/107614-64.html
# 算法参见: https://www.cnblogs.com/blakegao/articles/3300214.html
# 网络上的在线解密工具: https://www.xiaopeiqing.com/cisco-password-cracker/
#===============================================================================
def f解密7(a: str):
	crypttext = a.upper()
	plaintext = ""
	xlat = "dsfd;kfoA,.iyewrkldJKDHSUBsgvca69834ncxv9873254k;fg87"
	val = 0

	if len(crypttext) & 1:
		raise ValueError()

	seed = (ord(crypttext[0]) - 0x30) * 10 + ord(crypttext[1]) - 0x30
	if seed > 15 or not crypttext[0].isdigit() or not crypttext[1].isdigit():
		raise ValueError()

	for i in range(2, len(crypttext) + 1):
		if (i != 2) and not (i & 1):
			plaintext += chr(val ^ ord(xlat[seed]))
			seed += 1
			seed %= len(xlat)
			val = 0
		val *= 16
		if i == len(crypttext):
			break
		if crypttext[i].isdigit():
			val += ord(crypttext[i]) - 0x30
			continue
		if ord(crypttext[i]) >= 0x41 and ord(crypttext[i]) <= 0x46:
			val += ord(crypttext[i]) - 0x41 + 0x0a
			continue
		if len(crypttext) != i:
			raise ValueError()

	return plaintext
#===============================================================================
# 思科类型5密码解密
# 算法参见: https://insecure.org/sploits/cisco.passwords.html
# 在线解密工具: https://www.xiaopeiqing.com/cisco-password-cracker/type5.html
#===============================================================================
def f解密5(a: str):
	raise NotImplementedError()