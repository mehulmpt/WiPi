import socket
import json
import os
import select
import threading
import sys
import time
import subprocess
from omxpy import omxpy

name = str(input())
finished = False


def send(head, message, icon="important"):
    os.system("DISPLAY=:0 notify-send '"+head+"' '"+message+"' -i "+icon+" --hint int:transient:1")

def play():
    global omx
    omx = omxpy(os.path.expanduser("~/Desktop/WiPi/Movies/"+name))

def showdatatransfer():
    while True:
        if finished == True: break
        q = "ls ~/Desktop/WiPi/Movies/ -s | grep '"+name+"' | awk -F ' ' '{print $1}'"
        p = subprocess.Popen(q, stdout=subprocess.PIPE, shell=True)
        send("File Status", str(int((p.stdout.read()).decode('utf-8'))/1000) + 'MB Transferred')
        time.sleep(10)

def getip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("111.111.111.111",111)) # dont ask.
    return s.getsockname()[0]

def receiveMedia():
    global s
    global finished
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((getip(), 3143))
    path = os.path.expanduser('~/Desktop/WiPi')

    s.listen(1)
    path = os.path.expanduser('~/Desktop/WiPi')

    if os.path.exists(path) == False:
        os.makedirs(path+'/Movies')
    mediaPath = os.path.expanduser("~/Desktop/WiPi/Movies/"+name)
    if(os.path.isfile(mediaPath)):
        s.close()
        finished = True
        t1 = threading.Thread(target=play, args=())
        t2 = threading.Thread(target=receiveOMXControls, args=())
        t1.start()
        t2.start()
        print("filefound")
        return
    print("filenotfound")
    mediaFile = open(mediaPath, 'wb') # binary data received on socket
    (client, (ip, port)) = s.accept()
    client.settimeout(3)
    finished = False
    threading.Thread(target=showdatatransfer, args=()).start()
    try:
        while True:
            dataX = client.recv(262144)
            mediaFile.write(dataX)
    except socket.timeout as e:
        client.close()
        s.close()
        finished = True
        t1 = threading.Thread(target=play, args=())
        t2 = threading.Thread(target=receiveOMXControls, args=())
        t1.start()
        t2.start()

def receiveOMXControls():
    global s
    while True:
        t = str(input())
        if t == "togglepause":
            omx.toggle_pause()
        elif t == "stop":
            omx.stop()
            s.close()
            sys.exit(1)
        elif t == "jump30s":
            omx.jump30s()
        elif t == "fall30s":
            omx.fall30s()
        elif t == "jump10min":
            omx.jump10min()
        elif t == "fall10min":
            omx.fall10min()
        time.sleep(1)

receiveMedia()
