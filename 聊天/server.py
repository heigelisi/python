import socket
import threading
import sys
import os
import base64
import hashlib
import struct
import time

MAGIC_STRING = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
HANDSHAKE_STRING = "HTTP/1.1 101 Switching Protocols\r\n" \
      "Upgrade:websocket\r\n" \
      "Connection: Upgrade\r\n" \
      "Sec-WebSocket-Accept: {}\r\n" \
      "WebSocket-Location: ws://{}\r\n" \
      "WebSocket-Protocol:chat\r\n\r\n"


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', 8081))
sock.listen(1000)

headers = {}
conn,addr = sock.accept()
data = conn.recv(1024).decode()#接受数据
print(data)

# print(data.split("\r\n"))


# for i in data:
	# print(i)

header, data = data.split('\r\n\r\n', 1)
for line in header.split('\r\n')[1:]:
	key, val = line.split(': ', 1)
	headers[key] = val
sec_key = headers['Sec-WebSocket-Key']+MAGIC_STRING
print(headers)
res_key = base64.b64encode(hashlib.sha1(sec_key.encode()).digest())

str_handshake = HANDSHAKE_STRING.format(res_key.decode(),headers['Host'])
print(str_handshake)
# str_handshake = HANDSHAKE_STRING.replace('{1}', res_key).replace('{2}', HOST + ':' + str(PORT))

connect = conn.send(str_handshake.encode())
print(connect)
# data = conn.recv(1024)#接受数据
# print(data.decode())
# conn.send('你好'.encode())
# data = '你好'
# token = b"\x81"
# length = len(data)
# if length < 126:
#     token += struct.pack("B", length)
# elif length <= 0xFFFF:
#     token += struct.pack("!BH", 126, length)
# else:
#     token += struct.pack("!BQ", 127, length)

# # struct为Python中处理二进制数的模块，二进制流为C，或网络流的形式。
# data = '%s%s' % (token, data)
# conn.send(data.encode())

# time.sleep(20)


def parse_data( data):
    v = data[1] & 0x7f
    if v == 0x7e:
        p = 4
    elif v == 0x7f:
        p = 10
    else:
        p = 2
    mask = data[p: p+4]
    data = data[p+4:]
    print(data.decode())
    i = 0
    raw_str = ""
    for d in data:
        raw_str += chr(d ^ mask[i%4])
        i += 1
    return raw_str
data = conn.recv(1024)#接受数据
print(parse_data(data))


def sendMessage(connection,message):
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
    print(type(backMsgList[0]))
    for c in backMsgList:
        # if type(c) != bytes:
        # print(bytes(c, encoding="utf8"))
        message_byte += c
    message_byte += bytes(message, encoding="utf8")
    #print("message_str : ", str(message_byte))
    # print("message_byte : ", bytes(message_str, encoding="utf8"))
    # print(message_str[0], message_str[4:])
    # self.connection.send(bytes("0x810x010x63", encoding="utf8"))
    connection.send(message_byte)


sendMessage(conn,'111')
time.sleep(20)
