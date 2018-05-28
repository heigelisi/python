import sys

# 111111111111
#基本使用
from PyQt5.QtWidgets import QApplication,QWidget
# app = QApplication(sys.argv)

# #创建窗口
# w = QWidget()

# # w.resize(1000,400)#设置窗口大小
# w.setWindowTitle('欢迎')#设置标题
# w.setGeometry(40,100,1000,300)#x y 宽 高
# w.setStyleSheet('QWidget{background-color:#f00}')#设置背景颜色
# w.show()#显示窗口
# app.exec_()

#用类来使用
# class myform(QWidget):
# 	def __init__(self):
# 		super().__init__()
# 		self.setStyleSheet('QWidget{background-color:#f00}')#设置背景颜色


# app = QApplication(sys.argv)
# w = myform()
# w.show()
# app.exec_()
# 2222222222222222222
#控件
from PyQt5.QtWidgets import QLabel,QPushButton,QVBoxLayout
# class myform(QWidget):
# 	"""docstring for myform"""
# 	def __init__(self):
# 		super().__init__()
# 		self.label = QLabel(self)
# 		self.label.setText('hello')
# 		self.label.move(50,10)
# 		self.label.setFrameShape(1)#边框	

# 		btn = QPushButton(self)
# 		btn.setText('按钮')

# 		v = QVBoxLayout(self)
# 		v.addWidget(self.label)
# 		v.addWidget(btn)
# 		self.setLayout(v)	

# 		btn.clicked.connect(self.btn_clicked)#绑定事件
# 	def btn_clicked(self):
# 		self.label.setText('PYTHON')

# if __name__ == '__main__':
# 	app = QApplication(sys.argv)
# 	w = myform()
# 	w.show()
# 	app.exec_()



# 3333333333
# 工具栏

