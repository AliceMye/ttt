import hashlib
import json
import struct
import os
from conf import settings


def get_pwd(pwd):
    md = hashlib.md5()
    md.update(pwd.encode('utf-8'))
    return md.hexdigest()


def send_back(send_dic,client,file=None):

    # 序列化
    header_bytes = json.dumps(send_dic).encode('utf-8')
    header = struct.pack('i',len(header_bytes))
    client.send(header)
    client.send(header_bytes)

    # 上传文件
    if file:
        with open(file,'rb')as f:
            for line in f:
                client.send(line)
    # 收
    back_header = client.recv(4)
    back_len = struct.unpack('i',back_header)[0]

    # 真实数据
    back_size = client.recv(back_len)
    back_dic = json.loads(back_size.decode('utf-8'))
    return back_dic




def get_movie_list():
    movie_list = os.listdir(settings.LOCAL_MOVIE_PATH)
    return movie_list

def get_md5(file_path):
    md = hashlib.md5()
    if os.path.exists(file_path):
        file_size = os.path.getsize(file_path)
        file_index = [0,file_size//3,(file_size//3)*2,file_size-10]
        with open(file_path,'rb')as f:
            for index in file_index:
                f.seek(index)
                data = f.read()
                md.update(data)
            return md.hexdigest()





