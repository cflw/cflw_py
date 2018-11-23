import cflw小说下载 as 小说下载
import 小说下载.求书网 as 求书网
import 小说下载.笔趣看 as 笔趣看
import 小说下载.笔趣阁 as 笔趣阁
import 小说下载.顶点小说 as 顶点小说
import 小说下载.无限小说网 as 无限小说网
def f获取小说():
	#v小说 = 笔趣看.f获取小说("http://www.biqukan.com/2_2844/")
	#v小说 = 求书网.f获取小说("http://www.qiushu.cc/txt74524/")
	# v小说 = 顶点小说.f获取小说("https://www.23us.so/xiaoshuo/3574.html")
	# v小说 = 无限小说网.f获取小说("http://www.555x.org/read/45842.html")
	v小说 = 笔趣阁.f获取小说("http://www.biqutxt.com/0_310/")
	return v小说
def f获取章节():
	# v章节 = 顶点小说.C章节(*顶点小说.f提取链接("https://www.23us.so/files/article/html/3/3574/11462885.html"))
	# v章节 = 无限小说网.C章节(*无限小说网.f提取链接("http://www.555x.org/read/45842_1.html"))
	v章节 = 笔趣阁.C章节(*笔趣阁.f提取链接("http://www.biqutxt.com/0_310/186398.html"))
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
	f目录()
	# f正文()
if __name__ == "__main__":
	main()