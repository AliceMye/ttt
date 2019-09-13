import os
from conf import settings
from tcpclient import socket_client
from lib import common

# 管理员
user_dic = {'cookie':None}


def register(client):
    while True:
        name = input('输入用户名:').strip()
        password = input('输入密码:').strip()
        re_pwd = input('输入用户密码:').strip()
        if re_pwd == password:
            send_dic = {'type': 'register', 'name':name, 'password':common.get_pwd(password), 'user_type': 'admin'}
            back_dic = common.send_back(send_dic, client)
            if back_dic['flag']:
                print(back_dic['msg'])
                break
            else:
                print(back_dic['msg'])
        else:
            print('两次密码不一致')
            break


def login(client):
    while True:
        name = input('输入用户名:').strip()
        password = input("输入用户密码:").strip()
        if name and password:
            send_dic = {'type':'login','name':name, 'password': common.get_pwd(password),'user_type':'admin'}
            back_dic = common.send_back(send_dic,client)
            if back_dic['flag']:
                print(back_dic['msg'])
                user_dic['cookie'] = back_dic['session']
                # print(user_dic)
                # print(back_dic)
                break
            else:
                print(back_dic['msg'])
        else:
            print('用户名或密码不正确')
            break


def upload_movie(client):
    # 获取本地电影的列
    while True:
        movie_list = common.get_movie_list()
        if not movie_list:
            print('暂无本地电影')
            break
        for index, movies in enumerate(movie_list,1):
            print(index,movies)
        choice = input('输入电影的编号：').strip()
        if not choice.isdigit():
            continue
        choice = int(choice)-1
        if choice not in range(len(movie_list)):
            continue
        movie_name = movie_list[choice]
        file_path = os.path.join(settings.LOCAL_MOVIE_PATH,movie_name)  # 文件路径
        file_md5 = common.get_md5(file_path)
        send_dic = {'type':'check_movie','session':user_dic['cookie'],'file_md5':file_md5}
        file_size = os.path.getsize(file_path)
        back_dic = common.send_back(send_dic,client)
        if back_dic['flag']:
            print('选择上传的电影is_free')
            is_free = input('输入是否是免费<y/>n:').strip()

            # if is_free == 'y':
            #     is_free =1
            # else:
            #     is_free = 0

            is_free = 1 if is_free == 'y' else 0
            send_dic = {'type':'upload_movie','session':user_dic['cookie'],'file_md5':file_md5,'file_size':file_size,
                        'movie_name':movie_name,'is_free':is_free}
            back_dic = common.send_back(send_dic,client,file_path)
            if back_dic['flag']:
                print(back_dic['msg'])
                break
            else:
                print(back_dic['msg'])
                break

        else:
            print(back_dic['msg'])
            break


def delete_movie(client):
    # 获取所有电影
    while True:
        send_dic = {'type':'get_movie_list','session':user_dic['cookie'],'movie_type':'all'}
        back_dic = common.send_back(send_dic,client)
        if back_dic['flag']:
            movie_list = back_dic['movie_list']
            for index,movies in enumerate(movie_list,1):

                print(index,movies)
            choice = input('输入电影的编号：').strip()
            if not choice.isdigit():
                continue
            choice = int(choice)-1
            if choice not in range(len(movie_list)):
                continue
            movie_name = movie_list[choice]
            movie_id = movie_list[choice][2]
            send_dic = {'type':'delete_movie','session':user_dic['cookie'],
                        'movie_id':movie_id}
            back_dic = common.send_back(send_dic,client)
            if back_dic['flag']:
                print(back_dic['msg'])
                break
            else:
                print(back_dic['msg'])
                break
        else:
            print(back_dic['msg'])


def release_notice(client):
    title = input('输入主题：').strip()
    content = input('输入内容：').strip()
    send_dic = {'type':'release_notice','session':user_dic['cookie'],
                'title':title,'content': content}
    back_dic = common.send_back(send_dic,client)
    if back_dic['flag']:
        print(back_dic['msg'])
        return
    else:
        print(back_dic['msg'])



func_dic = {
    "1":register,
    "2":login,
    "3":upload_movie,
    "4":delete_movie,
    "5":release_notice,
}

def admin_view():
    sk_client = socket_client.SocketClient()
    client = sk_client.get_client()
    while True:
        print("""
        1.注册
        2.登录
        3.上传电影
        4.删除电影
        5.发布公告
        q.退出
     
        """)
        choice = input('输如功能编号:').strip()
        if choice == 'q':
            break
        elif choice in func_dic:
            func_dic.get(choice)(client)