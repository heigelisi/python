from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

app = QApplication([])

view = QWebEngineView()
view.load(QUrl("http://www.baidu.com"))
print(dir(view))
# print(view.windowTitle(app,'ssssssssssssssssss'))
view.show()
app.exec_()