
import hashlib
print(dir(hashlib))
#md5
md5 = hashlib.md5()
md5.update('123456'.encode())
passwd = md5.hexdigest()
print(passwd)

#sha1
sha1 = hashlib.sha1()
sha1.update('123456'.encode())
passwd = sha1.hexdigest()
print(passwd)

#sha224
sha224 = hashlib.sha224()
sha224.update('123456'.encode())
passwd = sha224.hexdigest()
print(passwd)

#sha256
sha256 = hashlib.sha256()
sha256.update('123456'.encode())
passwd = sha256.hexdigest()
print(passwd)

#sha384
sha384 = hashlib.sha384()
sha384.update('123456'.encode())
passwd = sha384.hexdigest()
print(passwd)


#sha3_384
sha3_384 = hashlib.sha3_384()
sha3_384.update('123456'.encode())
passwd = sha3_384.hexdigest()
print(passwd)


# 621226 2013016 988801

exit()

# # 第一步，安装crypto
# pip install crypto
# # 第二步，安装 pycryptodome
# pip install pycryptodome
# # 第三步，改文件夹名称
# 进入Python3的目录下的\lib\site-packages，将crypto文件夹更名为Crypto（注意是大写的C，否则导入模块失败）

# 作者：葛木瓜
# 链接：https://www.jianshu.com/p/bdadf8607a3b
# 來源：简书
# 简书著作权归作者所有，任何形式的转载都请联系作者获得授权并注明出处。
# import Crypto
# print(dir(Crypto))
# exit()
import base64
from Crypto.Cipher import AES

# AES加密
def aes_crypt(key, iv, passwd):
    """
    AES加密算法（key，iv，passwd输入均应为bytes类型，选择MODE_CBC类型加密）
    :param key: 秘钥（定值，16位长度）
    :param iv: 偏移（定值，位长度）
    :param passwd: 密码
    :return: 返回值再经过base64加密后
    """
    BS = AES.block_size  # 获取AES数据位数（16位）
    # 补位，补够16位
    pad = (lambda s: s + (BS - len(s) % BS) * '#')
    print(pad(passwd))
    aes = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv.encode('utf-8'))
    print(aes)
    return base64.b64encode(aes.encrypt(pad(passwd).encode('utf-8')))

aes_key = 'QWHeJfoWQgaYasdf'
aes_iv = '1111111111222345'
password = '123456'
# 注意，经过aes_crypt加密的密文是bytes类型
password = aes_crypt(aes_key, aes_iv, password).decode('utf-8')
print(password)
#解密
# password.decrypt(password)