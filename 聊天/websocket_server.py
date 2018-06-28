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

				for c in backMsgList:
				    message_byte += c
				message_byte += bytes(message, encoding="utf8")
				try:
					val.sendall(message_byte)
				except Exception as e:
					pass
					val.close()

	def recvMsg(self,conn,addr):
		ii = 0
		while True:

			try:
				msg = conn.recv(2048)
				if not msg:
					return False
				# print(msg[1])

				code_len =  msg[1] & 127

				if code_len == 126:

				   masks=msg[4:8]

				   data=msg[8:]

				elif code_len == 127:

				   masks=msg[10:14]
				   data=msg[14:]

				else:
				   masks=msg[2:6]
				   data=msg[6:]

				# print('masks',masks,'data',data,ii)
				raw_str=""
				i=0

				for d in data:
					# print(d)
					raw_str += chr(d ^ masks[i%4])
					i+=1


				message = None
				try:
					message = {'code':200,'msg':raw_str.replace('%','\\').encode('gbk').decode('unicode_escape')}
				except Exception as e:
					pass

				if not message:
					try:
						message = {'code':200,'msg':raw_str.replace('%','\\').encode('utf8').decode('unicode_escape')}
					except Exception as e:
						pass

				#关闭
				if message['msg'] == 'quit':
					conn.close()
					self.clients.pop(addr[0]+':'+str(addr[1]))
					exit()	
				timestamp = int(time.time())
				time_local = time.localtime(timestamp)
				dt = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
				message['date'] = str(dt)
				if ii == 0:
					username = addr[0]+':'+str(addr[1])
					username = raw_str.replace('%','\\').encode('gbk').decode('unicode_escape')
					message['username'] = '系统消息'
					message['msg'] = username+' 进入了聊天室'
					self.sendMsg(json.dumps(message))
				else:
					message['username'] = username
					self.sendMsg(json.dumps(message))
				# print(username,message)
				# print(username,json.dumps(message))
				ii += 1


			except Exception as e:
				print(e)
				print(username,'退出了')
				conn.close()
				self.clients.pop(addr[0]+':'+str(addr[1]))
				exit()


	def main(self):
		
		while True:
			conn,addr = self.sock.accept()
			data = conn.recv(2048)#接受数据
			print(data)
			data = data.decode()
			if self.shakeHands(conn,data):
				self.clients[addr[0]+':'+str(addr[1])] = conn
				w = threading.Thread(target=self.recvMsg,args=(conn,addr,))
				w.start()

			else:
				continue


if __name__ == '__main__':
	ChatRoom('0.0.0.0',8082).main()


# nohup python3 -u /www/pythonScript/liaotian/web.py > /www/pythonScript/liaotian/web.log 2>&1 &
# nohup python3 -u /www/pythonScript/liaotian/websocket_server.py > /www/pythonScript/liaotian/websocket_server.log 2>&1 &
