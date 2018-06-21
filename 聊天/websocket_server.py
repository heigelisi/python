import socket
import threading
import sys
import os
import base64
import hashlib
import struct
import time
import json
MAGIC_STRING = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
HANDSHAKE_STRING = "HTTP/1.1 101 Switching Protocols\r\n" \
      "Upgrade:websocket\r\n" \
      "Connection: Upgrade\r\n" \
      "Sec-WebSocket-Accept: {}\r\n" \
      "WebSocket-Location: ws://{}\r\n" \
      "WebSocket-Protocol:chat\r\n\r\n"


class ChatRoom(object):
	def __init__(self, *args):
		self.args = args
		self.host = args[0]#主机名
		self.port = args[1]#端口
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.bind((self.host, int(self.port)))
		self.sock.listen(1000)
		self.clients = {}#存放所以客服端链接



	def shakeHands(self,conn,data):
		'握手'
		headers = {}
		try:
			header, data = data.split('\r\n\r\n', 1)
			for line in header.split('\r\n')[1:]:
				key, val = line.split(': ', 1)
				headers[key] = val
			sec_key = headers['Sec-WebSocket-Key']+MAGIC_STRING
			res_key = base64.b64encode(hashlib.sha1(sec_key.encode()).digest())

			str_handshake = HANDSHAKE_STRING.format(res_key.decode(),headers['Host'])
			connect = conn.send(str_handshake.encode())
			return True
		except Exception as e:
			return False
	def sendMsg(self,message):
		if self.clients:
			for key,val in self.clients.items():
				msgLen = len(message)
				backMsgList = []
				backMsgList.append(struct.pack('B', 129))

				if msgLen <= 125:
				    backMsgList.append(struct.pack('b', msgLen))
				elif msgLen <=65535:
				    backMsgList.append(struct.pack('b', 126))
				    backMsgList.append(struct.pack('>h', msgLen))
				elif msgLen <= (2^64-1):
				    backMsgList.append(struct.pack('b', 127))
				    backMsgList.append(struct.pack('>h', msgLen))
				else :
				    print("the message is too long to send in a time")
				    return
				message_byte = bytes()
				print(key)
				for c in backMsgList:
				    message_byte += c
				message_byte += bytes(message, encoding="utf8")
				try:
					val.send(message_byte)
				except Exception as e:
					pass
					val.close()

	def recvMsg(self,conn):

		while True:
			# if self.clients:
			# 	for key,val in self.clients.items():
			# 		msg = val.recv(1024).decode()#接受数据
			# 		data = {'code':200,'msg':msg}
			# 		self.sendMsg(json.dumps(data))
			# time.sleep(1)
			print('接受数据')
			info = conn.recv(1024)#接受数据
			print(info)
			print(info[1])
			code_len = info[1] & 127
			if code_len == 126:
			    masks = info[4:8]
			    data = info[8:]
			elif code_len == 127:
			    masks = info[10:14]
			    data = info[14:]
			else:
			    masks = info[2:6]
			    data = info[6:]
			print(data)
			i = 0
			raw_str = ""
			for d in data:
			    # print(masks, masks[i % 4])
			    print(d)
			#     raw_str += chr(d ^ ord(masks[i % 4]))
			#     i += 1
			# print(raw_str)
			# print(msg.decode())
			data = {'code':200,'msg':'123'}
			self.sendMsg(json.dumps(data))


		





	def main(self):
		
		while True:
			conn,addr = self.sock.accept()
			data = conn.recv(2048)#接受数据
			print(data)
			data = data.decode()
			print('ddddddddddddddddddd',data,'ddddddddddddddddddddddddddd')
			if self.shakeHands(conn,data):
				self.clients[addr[0]+':'+str(addr[1])] = conn
				w = threading.Thread(target=self.recvMsg,args=(conn,))
				w.start()

			else:
				continue


if __name__ == '__main__':
	ChatRoom('localhost',8082).main()




# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.bind(('localhost', 8082))
# sock.listen(1000)


# while 1:
# 	headers = {}
# 	conn,addr = sock.accept()
# 	data = conn.recv(1024).decode()#接受数据
