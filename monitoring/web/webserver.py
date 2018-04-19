import socket
import websocket




s = socket.socket()
s.bind(('0.0.0.0', 8081))
s.listen(500)
while True:
    # cli, addr = s.accept()
    conn,addr = s.accept()
    data = conn.recv(1024)#接受数据
    conn.send('sssssssssssssss'.encode())#发送数据给客户端
    print('ssss')

