import cflw小说下载 as 小说下载
import cflw小说下载_求书网 as 求书网
import cflw小说下载_笔趣看 as 笔趣看
import cflw小说下载_顶点小说 as 顶点小说
def f获取小说():
	#v小说 = 笔趣看.f获取小说("http://www.biqukan.com/2_2844/")
	#v小说 = 求书网.f获取小说("http://www.qiushu.cc/txt74524/")
	v小说 = 顶点小说.f获取小说("https://www.23us.so/xiaoshuo/3574.html")
	return v小说
def f获取章节():
	v章节 = 顶点小说.C章节(*顶点小说.f提取链接("https://www.23us.so/files/article/html/3/3574/11462885.html"))
	return v章节
def f一键下载():
	v小说 = f获取小说()
	小说下载.f一键下载(v小说, "d:/")
def f小说信息():
	v小说 = f获取小说()
	print(v小说.fg小说信息())
def f目录():
	v小说 = f获取小说()
	for v in v小说.fe目录():
		print(v[0], v[1].fg地址())
def f正文():
	v章节 = f获取章节()
	v正文 = v章节.fg正文()
	print(v正文)
def main():
	#f目录()
	f正文()
if __name__ == "__main__":
	main()