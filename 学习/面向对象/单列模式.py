
class test(object):

	instance = False
	init_tga = False

	def __new__(self,*args,**wkargs):
		if not self.instance:
			self.instance = super().__new__(self)

		return self.instance


	def __init__(self):
		if self.init_tga:
			return 
		
		print('执行初始化')
		self.tt = 'hehe'
		self.init_tga = True





t1 = test()
print(t1)
print(t1.tt)
t2 = test()
print(t2)
print(t2.tt)
