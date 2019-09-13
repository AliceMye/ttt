import time

from tcpclient import socket_client
from lib import common
import os
from conf import settings

user_dic = {'cookie': None,
            'is_vip': None}

def register(client):
    while True:
        name = input('输入用户名:').strip()
        password = input('输入密码:').strip()
        re_pwd = input('输入用户密码:').strip()
        if re_pwd == password:
            send_dic = {'type': 'register', 'name':name, 'password':common.get_pwd(password), 'user_type': 'user'}
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
            send_dic = {'type':'login','name':name, 'password': common.get_pwd(password),'user_type':'user'}
            back_dic = common.send_back(send_dic,client)
            if back_dic['flag']:
                print(back_dic['msg'])
                user_dic['cookie'] = back_dic['session']
                user_dic['is_vip'] = back_dic['is_vip']

                # print(user_dic)
                # print(back_dic)
                break
            else:
                print(back_dic['msg'])
        else:
            print('用户名或密码不正确')
            break


def buy_vip(client):
    # 判断
    if user_dic['is_vip']:  # True 才会走
        print('已经是Vip ')
        return
    cmd = input('是否要购买vip<y/n>:').strip()
    if cmd == 'y':

        send_dic = {'type':'buy_vip','session':user_dic['cookie']}

        back_dic = common.send_back(send_dic,client)
        if back_dic['flag']:
            print(back_dic['msg'])
            user_dic['is_vip'] = 1
            return
        else:
            print(back_dic['msg'])
            return
    else:
        print('欢迎下次再来')
def check_movie(client):
    # 查看电影
    send_dic = {'type':'get_movie_list','session':user_dic['cookie'], 'movie_type':'all'}
    back_dic = common.send_back(send_dic,client)
    if back_dic['flag']:
        movie_list = back_dic['movie_list']
        for index,movie in enumerate(movie_list):
            print(index, movie)
            # 不能接return 只能拿一条
    else:
        print(back_dic['msg'])


def download_free_movie(client):
    # 下载 删除 先获取所有的电影免费 和上面一样 改 free
    while True:
        send_dic = {'type': 'get_movie_list', 'session': user_dic['cookie'], 'movie_type': 'free'}
        back_dic = common.send_back(send_dic, client)
        if back_dic['flag']:
            movie_list = back_dic['movie_list']

            # print(movie_list,'999')
            # [['163cebcf86db5f949ec4ce1ea458b33f668573_150157400119_2.jpg', '收费', 4]
            for index, movie in enumerate(movie_list,1):

                # print(index, movie)
                print(index,movie)
            choice = input('输入电影的编号:').strip()
            if not choice.isdigit():
                continue
            choice = int(choice)-1
            if choice not in range(len(movie_list)):
                continue
            movie_name = movie_list[choice][0]
            # print(movie_name,'777')
            movie_id = movie_list[choice][2]
            send_dic = {'type':'download_movie','session':user_dic['cookie'],'movie_id':movie_id,
                        'movie_name':movie_name,'movie_type':'free'}
            back_dic = common.send_back(send_dic,client)
            if back_dic['flag']:
                # 获取文件的大小 文件名 with 上下文管理
                file_size = back_dic['file_size']
                wait_time = back_dic['wait_time']
                # movie_name = back_dic['movie_name']
                time.sleep(wait_time)
                # print(movie_name,'===')
                file_path = os.path.join(settings.DOWNLOAD_MOVIE,movie_name)
                # print('开始下载')
                recv_size = 0

                with open(file_path,'wb')as f:
                    while recv_size<file_size:
                        data = client.recv(1024)
                        f.write(data)
                        recv_size += len(data)
                    print('下载完成')
                    return


def download_charge_movie(client):
    # 下载收费电影
    # 先获取所有电影
    while True:
        send_dic = {'type': 'get_movie_list', 'session': user_dic['cookie'], 'movie_type': 'charge'}
        back_dic = common.send_back(send_dic, client)
        if back_dic['flag']:
            movie_list = back_dic['movie_list']

            # print(movie_list,'999')
            # [['163cebcf86db5f949ec4ce1ea458b33f668573_150157400119_2.jpg', '收费', 4]
            for index, movie in enumerate(movie_list,1):

                # print(index, movie)
                print(index,movie)
            choice = input('输入电影的编号:').strip()
            if not choice.isdigit():
                continue
            choice = int(choice)-1
            if choice not in range(len(movie_list)):
                continue
            movie_name = movie_list[choice][0]
            # print(movie_name,'777')
            movie_id = movie_list[choice][2]
            send_dic = {'type':'download_movie','session':user_dic['cookie'],'movie_id':movie_id,
                        'movie_name':movie_name,'movie_type':'charge'}
            back_dic = common.send_back(send_dic,client)
            if back_dic['flag']:
                # 获取文件的大小 文件名 with 上下文管理
                file_size = back_dic['file_size']
                wait_time = back_dic['wait_time']
                # movie_name = back_dic['movie_name']
                time.sleep(wait_time)
                # print(movie_name,'===')
                file_path = os.path.join(settings.DOWNLOAD_MOVIE,movie_name)
                # print('开始下载')
                recv_size = 0

                with open(file_path,'wb')as f:
                    while recv_size<file_size:
                        data = client.recv(1024)
                        f.write(data)
                        recv_size += len(data)
                    print('下载完成')
                    return



def check_download_record(client):
    send_dic = {'type':'check_download_record','session':user_dic['cookie']}
    back_dic = common.send_back(send_dic,client)
    if back_dic['flag']:
        print(back_dic['record_list'])
        return
    else:
        print(back_dic['msg'])

def check_notice(client):
    send_dic = {'type':'check_notice','session':user_dic['cookie']}
    back_dic = common.send_back(send_dic,client)
    if back_dic['flag']:
        print(back_dic['notice_list'])

    else:
        print(back_dic['msg'])



func_dic = {
    "1": register,
    "2": login,
    "3": buy_vip,
    "4": check_movie,
    "5": download_free_movie,
    "6": download_charge_movie,
    "7":check_download_record,
    "8":check_notice

}

def user_view():
    sk_client = socket_client.SocketClient()
    client = sk_client.get_client()
    while True:
        print("""
        1.注册
        2.登录
        3.冲会员
        4.查看电影
        5.下载免费电影
        6.下载收费电影
        7.查看下载电影记录
        8.查看公告
        q.退出

        """)
        choice = input('输如功能编号:').strip()
        if choice == 'q':
            break
        elif choice in func_dic:
            func_dic.get(choice)(client)