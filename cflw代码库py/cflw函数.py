def A忽略异常(af):
	def f(*args, **kwargs):
		try:
			return af(*args, **kwargs)
		except Exception as e:
			return None
	return f