import cflw爬虫_代理列表 as 代理
def fg过时文档():
	v文件 = open("测试_代理列表.txt", "r", encoding = "utf-8")
	return v文件.read()
def fg实时文档():
	return 代理.f获取文档()
def main():
	v列表 = 代理.f解析文档(fg过时文档())
	for v行 in v列表:
		print(v行)
if __name__ == "__main__":
	main()