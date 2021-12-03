import socket
import datetime as dt
import pickle
import threading

# クライアント設定
port = 55525
address = "127.0.0.1"
serv_add = (address, port)
msize = 4096

# 接続先設定
joinip = input("接続先のサーバーのIPアドレスを入力してください : ")
if not joinip == "":
    address = joinip

# IP更新
serv_add = (address, port)

# ソケット作成
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.connect(serv_add)

# joinリクエスト
jv = "join"
jv = pickle.dumps(jv)
soc.send(jv)

#Usernameリクエスト
un = []
un.append("UserName")
un.append(input("使用する名前を入力してください : "))
un = pickle.dumps(un)
soc.send(un)

# クライアント起動
print("The client has Started!")

#クライアント入力開始
print('Input any messages, Type [end] to exit')

def recv_data(soc):
    while True:
        try:
            rv = soc.recv(msize)
            rv = pickle.loads(rv)
            print(f"[{rv[2]}]:", rv[0], "  ||", rv[1])
        except ConnectionResetError:
            print("ConnectionError")
            soc.shutdown(socket.SHUT_RDWR)
            soc.close()
            break

connthread = threading.Thread(target=recv_data, args=(soc,))
connthread.start()

while True:
    #messageを送信する
    nowtime_dt = dt.datetime.now()
    nowtime = dt.datetime.strftime(nowtime_dt, "%Y/%m/%d %H:%M:%S")
    message = input()
    sv = list()
    sv.append(message)
    sv.append(nowtime)
    try:
        if message != 'end':
            # svはsendvalue 送る物
            sv = pickle.dumps(sv)
            soc.send(sv)
        else:
            sv = pickle.dumps(sv)
            soc.send(sv)
            soc.send(sv)
            print('closing socket')
            soc.close()
            print('done')
            break
    except ConnectionResetError:
        print("ConnectionError")
        break
soc.shutdown(socket.SHUT_RDWR)
soc.close()

