import socket
import datetime as dt
import pickle
import urllib.request
import ssl
import threading

#ssl証明
ssl._create_default_https_context = ssl._create_unverified_context


#グローバルIP取得
globalip = urllib.request.urlopen('https://inet-ip.info/ip').read().decode('utf-8')


#サーバー設定
host = "0.0.0.0"
port = 55525
hostadd = (host,port)
msize = 4096
br = 0


#ソケット作成
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.bind(hostadd)
soc.listen()


#クライアントリスト
clist = [] #クライアントリスト本体
clistn = [[]] #名前用リスト
del clistn[0] #clistnの0番目（空の要素）を消す
clistc = [] #コピー用リスト
global clistnn #clistnを回すための変数、ただの数
clistnn = 0


#ここまで初期設定
print("The server has Started!")
print("IP address :",globalip," Port number :",port)
print("================================================")

#メイン関数
def recdata(sock,addr):
    global clistnn #clistn
    socadd = sock , addr
    name = ""
    
    #データ受信ループ
    while True:
        #受信データ処理、例外は切断対応
        try:
            rv = sock.recv(4096) 
            rv = pickle.loads(rv)

            #参加対応
            if rv == "join":
                print(type(rv))
                print(f'Client Join: {addr}')
            #endの入力の対応
            elif rv[0] == "end":
                print("The client requested a disconnect.")
                soc.close()
                break
            #ユーザー名の処理 clistnに格納しているnnは新規ユーザーの誘導
            elif rv[0] == "UserName":
                print("Entry Name : ",rv[1])
                clistn[clistnn].append(rv[1])
                clistnn = clistnn + 1
            else:#通常メッセージ対応
                #ユーザー名(clistn)とIPアドレス(clist)の紐付け
                for i,v in enumerate(clistn):
                    try:
                        idxserchf , idxserchb = (i, v.index(socadd) + 1)
                        break
                    except:
                        pass
                print(f"{clistn[idxserchf][idxserchb]}: {rv}")
                rv.append(clistn[idxserchf][idxserchb])
                print(rv)
                #クライアントから受け取ったメッセージにユーザー名を紐付てバイナリ化
                rv = pickle.dumps(rv)
                #clistを素に、作ったデータを全クライアントへ送信
                for client in clist:
                    client[0].send(rv)
        #以降切断時処理
        except ConnectionResetError:
            print("Error!")
            break
    print("ConnectionError socket Close")
    print(f"RemoveClient for {addr}")
    #切断時刻取得＆格納
    nowtime_dt = dt.datetime.now()
    nowtime = dt.datetime.strftime(nowtime_dt, "%Y/%m/%d %H:%M:%S")
    try:
        disn = clistn[idxserchf][idxserchb]
    except:
        disn = addr
    dissv = [f"Disconnect client for [{disn}]",f"{nowtime}","Server"]
    dissv = pickle.dumps(dissv)
    #clistの要素が0なら何もせず、あるなら切断したクライアントデータを削除
    if len(clist) == 0:
        pass
    else:
        try:
            clist.remove((clisoc,cliadd,name))
        except:
            clist.remove(socadd)
    #切断されたことを残ったクライアントに送信
    for client in clist:
        client[0].send(dissv)
    



while True:
    clisoc, cliadd = soc.accept()
    clist.append((clisoc,cliadd))
    clistc.append((clisoc,cliadd))
    clistn.append(clistc.copy())
    clistc.clear()
    #recdata関数をスレッド化
    connthread = threading.Thread(target=recdata, args=(clisoc, cliadd))
    connthread.start()
