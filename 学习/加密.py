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
    return base64.b64encode(aes.encrypt(pad(passwd).encode('utf-8')))

aes_key = 'QWHeJfoWQgaYasdf'
aes_iv = '1111111111222345'
password = '123456'
# 注意，经过aes_crypt加密的密文是bytes类型
password = aes_crypt(aes_key, aes_iv, password).decode('utf-8')
print(password)
#解密
des.decrypt(password)