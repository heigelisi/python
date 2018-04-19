import requests
import re
import time
import pyquery
import tkinter


# class Crack(object):
# 	"""docstring for Crack"""
	def __init__(self):
		self.root = tkinter.Tk()
		self.root.title('dz破解')#设置title
		self.root.geometry('500x500+200+200')#设置窗口大小和位置
		
		#url
		url = tkinter.Entry(self.root)
		url.pack()

		# entry2 = Entry(root,show="*")#用*号现在输入的字符 可以用于密码

	def main(self):
		l = tkinter.Label(self.root, text="你好", bg="pink", font=("Arial",12), width=8, height=3)
		l.pack() 
		self.root.mainloop()

		pass



# Crack().main()


lis = [1,2,3,4,5,5]
lis[1] = 3333
print(lis[1])


