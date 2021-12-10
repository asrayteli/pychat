import socket
import datetime as dt
import pickle
import threading
import struct

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
jv = []
jv.append("/join")
jv = pickle.dumps(jv)
svj = len(jv)
svj = struct.pack("l",svj)
soc.sendall(svj)
soc.send(jv)


#Usernameリクエスト
un = []
un.append("/UserName")
un.append(input("使用する名前を入力してください : "))
un = pickle.dumps(un)
svu = len(un)
svu = struct.pack("l",svu)
soc.sendall(svu)
soc.send(un)

# クライアント起動
print("The client has Started!")

#クライアント入力開始
print('Input any messages, Type [/end] to exit')

def recv_data(soc):
    while True:
        try:
            rv = soc.recv(msize)
            rv = pickle.loads(rv)
            try:
                print(f"[{rv[2]}]:", rv[0], "  ||", rv[1])
            except:
                print(rv)
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
        if message == "/end":
            # svはsendvalue 送る物
            sv = pickle.dumps(sv)
            sve = len(sv)
            sve = struct.pack("l",sve)
            soc.sendall(sve)
            soc.sendall(sv)
            print('closing socket')
            soc.close()
            soc.close()
            print('done')
            break
        elif message == "/filesend":
            sbfl = []
            filename = input("送りたいファイルをD&Dしてください")
            with open(filename, 'rb') as fp:
                sbf = fp.read()#sbfはsend binary file
            sbfl.insert(0,"/filesend")
            sbfl.append(sbf)
            fileidx = filename.find(".")
            fileext = filename[fileidx:]
            sbfl.append(fileext)
            sfm = filename.rfind("\\")
            sfm = filename[sfm:]
            sfm = sfm.strip("\\")
            sfm2 = sfm.rfind(".")
            sfm = sfm[:sfm2]
            sbfl.append(sfm)
            print(sfm)
            print(fileext)
            print(type(sbfl))
            sbfl = pickle.dumps(sbfl,protocol=5)
            svf = len(sbfl)
            print(svf)
            svf = struct.pack("l",svf)
            soc.sendall(svf)
            soc.sendall(sbfl)
            """
            print("a")
            dc = soc.recv(4096)
            print("b")
            dc = pickle.loads(dc)
            while True:
                print("c")
                if dc == "receive Complete!":break
                else:
                    svlack = dc
                    print(type(svlack),svlack)
                    break
                """

            print("ファイルを送信しました。: ")
        else:
            sv = pickle.dumps(sv)
            svr = len(sv)
            svr = struct.pack("l",svr)
            soc.sendall(svr)
            soc.sendall(sv)
    except ConnectionResetError:
        print("ConnectionError")
        break
soc.shutdown(socket.SHUT_RDWR)
soc.close()

