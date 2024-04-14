import os
if os.name == "nt":
	from .cflw操作系统_win import *
else:
	from .cflw操作系统_linux import *