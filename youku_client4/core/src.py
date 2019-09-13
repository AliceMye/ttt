
# 视图层
from core import admin,user

func_dic = {
    '1':admin.admin_view,

    '2':user.user_view
}

def run():
    while True:
        print("""
        1.管理员视图层
        2.用户视图层
        q.退出
        
        
        """)
        choice = input('输入功能编号:').strip()
        if choice == 'q':
            break
        elif choice in func_dic:
            func_dic.get(choice)()
        else:
            print('输入争取的功能编号')
