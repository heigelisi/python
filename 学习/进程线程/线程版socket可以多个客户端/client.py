import socket
client = socket.socket()#连接规定协议并且创建对象(连接类型默认为tcp)
client.connect(('192.168.1.112',9896))#要连接的ip和端口
while True:
	msg = input('请输入要发送的内容').strip()
	if msg:
		client.send(msg.encode('utf-8'))#发送数据 只能发送biz
		data = client.recv(1024)#接受返回来的数据 指定大小为1024字节
		print(data.decode())
client.close()#关闭连接