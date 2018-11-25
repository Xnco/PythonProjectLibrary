
passward_list = ['*#*#', '123456']

def account_login():
    password = input('Password: ')
    password_correct = password == passward_list[-1]
    password_reset = password == passward_list[0]
    if password_correct:
        print('login success')
    elif password_reset:
        passward_list[-1] = input('new pw: ')
        account_login()
    else:
        print("input error")
        account_login();


account_login()