# 乘风龙王的代码库(python)
主要是一些随便写写的东西，其中有很多没写完的半成品，有的甚至从来没运行过。代码文件的编码为**utf-8无bom**。

项目依赖项：此代码库所引用的其他第三方库在代码文件开头导入语句后面用注释给出库名，可通过pip安装。
* requests
* beautifulsoup4
* pyserial
* pywin32
* paramiko

**网络设备脚本**相关代码已从此代码库拆分并转移到 https://github.com/cflw/network_device_script

### 文章
按时间顺序排列
* [用python编写小说网站爬虫](https://zhuanlan.zhihu.com/p/51309019) \[知乎\]

## 内容包含
### 工具
* **cflw字符串**：用来判断中文的函数和正则表达式，和一些计算处理字符串的函数。
* **cflw时间**：一些时间类。
* **cflw辅助**：一些装饰器，*没什么用*。
* **cflw工具_运算**：一些小函数

### 数学
* **cflw数学**：常用数学函数
* **cflw数学_向量**
* **cflw数学_平面几何**
* **cflw数学_图形**：颜色
* **cflw数学_矩阵**
* **cflw数学_随机**：抄袭c++标准库的\<random\>

### 网络
* **cflw网络地址**：提供对IPv4和IPv6地址的解析与计算，提供对物理(Media Access Control)地址的解析与计算
* **cflw网络连接**：提供统一的接口，通过Telnet、SSH、Console等方式连接到网络设备。
* ~~cflw网络设备~~(已移到[网络设备脚本](https://github.com/cflw/network_device_script))：提供统一的接口对路由器、交换机等网络设备进行控制。

### 爬虫
* **cflw爬虫**：提供爬虫相关实用工具
* **cflw爬虫_代理列表**：获取可用的HTTP代理
* **cflw小说下载**：从一些盗版小说网站上下载小说(～￣▽￣)～ 。

### 输入
* **cflw输入_win**：只有一些枚举。完整内容见[乘风龙王的代码库(c++)](https://github.com/cflw/cflw_cpp)中的**cflw输入_win**
* **cflw按键脚本_win**：模拟键盘鼠标输入

### 其他
* **cflw英语**：包含常用单词的字符串数组

## 使用说明
见[使用说明](文档/使用说明.md)