import socket
import time
import json
import os
import select
import re
import sys
import signal
import threading
import subprocess
import pexpect

s = None
client = None
proc = None
proc2 = None

connected = False


def send(head, message, icon="important"):
    os.system("DISPLAY=:0 notify-send '"+head+"' '"+message+"' -i "+icon+" --hint int:transient:1")

def startsockreq(name):
    global x
    global proc
    proc = pexpect.spawn("/usr/bin/python3 media.py")
    print(proc)
    proc.sendline(name)
    x = proc.pid
    time.sleep(1)
    k = proc.expect_exact(["filefound", "filenotfound"])
    if k == 0: client.send("filefound\n".encode())
    else: client.send("filenotfound\n".encode())
    proc.interact()
    

def startyoutubereq(url):
    global proc2
    proc2 = pexpect.spawn("/usr/bin/python3 youtube.py")
    proc2.sendline(url)
    proc2.interact()

def getip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("111.111.111.111",111)) # dont ask.
    return s.getsockname()[0]

def sendNotifications(ip):
    print(ip)
    while True:
        send("SUCCESS", "CONNECT YOUR DEVICE TO: "+ip)
        time.sleep(10)
        if connected: break
    
def main():
    global tx
    global proc
    global client
    global proc2
    global x
    global connected

    raspip = getip()
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        s.bind((raspip, 3141))
        s.listen(1)
        threading.Thread(target=sendNotifications, args=(raspip,)).start()
    except Exception as e:
        send("ERROR", "Failed to open socket. Are you connected to WiFi? (Restarting Script)")
        time.sleep(10)
        return
        
    (client, (ip, port)) = s.accept()
    print("they see me rollin'")
    send("Connected", "A device just connected to pi")
    connected = True   
    proc = None

    while True:
        dataX = client.recv(1024)

        if not dataX:
            send("Disconnected", "Your devcie was disconnected. Restarting pi server")
            break

        dataX = dataX.decode("UTF-8")
        
        print(dataX)

        j = json.loads(dataX)[0]

        if(j['msg'] == 'omxcmd' and proc != None):
            proc.sendline(str(j['p1']))
            time.sleep(0.4)
            proc.sendline(str(j['p1']))

        if(j['msg'] == 'omxyt' and proc2 != None):
            proc2.sendline(str(j['p1']))
            time.sleep(0.4)
            proc2.sendline(str(j['p1']))

        if(j['msg'] == 'startmediacontroller'):
            os.system("pkill omxplayer")
            tx = threading.Thread(target=startsockreq, args=(j['p1'],))
            tx.start()
            send("Data Receiving", "Receiving your media file to play. Please be patient")

        if(j['msg'] == 'startyoutubecontroller'):
            threadYT = threading.Thread(target=startyoutubereq, args=(str(j['p1']),))
            threadYT.start()
            send("Received Video Link", "Connecting to YouTube...")

if __name__ == "__main__":
    main()
    os.execv(sys.executable, ['python3'] +sys.argv)
