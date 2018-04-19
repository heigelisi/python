ban = ['错误','404','页面不存在','找不回','新闻','医生','医学','医院','自行车','单车','摩托车','旅游','投资','金融','垂钓','钓鱼','学院','财经','网赚','医疗','残疾','寻亲','减肥','房产','民航','诗词','教育','唐诗','诗歌','招聘','幼儿园','司法','千峰IT','QQ','糖尿病','安卓','中国','驴友','白癜风','Discuz! 官方']
for i in range(100):


	if '404' in ban:
		continue
	print(i)



exit()

# from tkinter import *
# import tkinter
# from PIL import Image as MyImages, ImageTk
# import sys,os
# path = os.path.dirname(sys.argv[0])+'/'

# #设置窗口
# root = Tk()
# root.title('测试')#设置title
# root.geometry('500x500+200+200')#设置窗口大小和位置

# # canvas=Canvas(root,width=200,height=180,scrollregion=(0,0,520,520)) #创建canvas
# # canvas.place(x = 75, y = 265) #放置canvas的位置
# # frame=Frame(canvas) #把frame放在canvas里
# # frame.place(width=180, height=180) #frame的长宽，和canvas差不多的
# # vbar=Scrollbar(canvas,orient=VERTICAL) #竖直滚动条
# # vbar.place(x = 180,width=20,height=180)
# # vbar.configure(command=canvas.yview)
# # hbar=Scrollbar(canvas,orient=HORIZONTAL)#水平滚动条
# # hbar.place(x =0,y=165,width=180,height=20)
# # hbar.configure(command=canvas.xview)
# # canvas.config(xscrollcommand=hbar.set,yscrollcommand=vbar.set) #设置  
# # canvas.create_window((90,240), window=frame)  #create_window


# load = MyImages.open(path+'static/load.gif')
# pic = ImageTk.PhotoImage(load)
# label = tkinter.Label(root,image=pic)
# label.place(x=10,y=10)



# root.mainloop()

#coding=utf-8

import tkinter,re,time

# def handler(event, a, b, c):
# 	'''事件处理函数'''
# 	print (event)
# 	print ("handler", a, b, c)

# def handlerAdaptor(fun, **kwds):
# 	'''事件处理函数的适配器，相当于中介，那个event是从那里来的呢，我也纳闷，这也许就是python的伟大之处吧'''
# 	return lambda event,fun=fun,kwds=kwds: fun(event, **kwds)

if __name__=='__main__':
	root = tkinter.Tk()
	def func(event):
		try:
			compile_ = re.compile(r'.*?(button\d+)',re.S)
			page_list = compile_.findall(str(event.widget))[0]
			compile_2 = re.compile(r'.*?(\d+)',re.S)
			page_ = int(compile_2.findall(page_list)[0])
			eval('e%d'%page_-1).set('#000')
			time.sleep(1)
			eval('e%d'%page_-1).set('#f00')

		except Exception as e:
			e0.set('#000')
			time.sleep(1)
			e0.set('#f00')
			pass
	def func1(event):
		pass

	# 通过中介函数handlerAdaptor进行事件绑定
	for i in range(5):
		exec('e%d = tkinter.Variable()'%i)
		eval('e%d'%i).set('#f00')
		btn = tkinter.Button(text='按钮',textvariable=eval('e%d'%i),fg=eval('e%d'%i).get())
		btn.bind('<Button-1>',func1)
		btn.bind("<ButtonRelease-1>", func)
		btn.pack()

	root.mainloop()

# 'test'+'1' = 'test1'
# test ='test1'
# test+'1' = 'ssss' 


# def func(k,v):

# 	return (k == v)

# print(func('t','11111'))


# exec('t = 222')
# print(t)
# <ButtonRelease-1>


for i in range(5):
	exec('varName%d = i'%i)
	print(eval('varName%d'%i))

# ar = "This is a string"
# varName = 'var'
# s= locals()['varName']
# s2=vars()['varName']

# # print (s)
# # print (s2)
# print (eval('varName'))

# print(vars())

e = {}
e[1] = 3