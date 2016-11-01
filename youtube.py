import socket
import json
import os
import time
import select
import sys
import re
import threading
from omxpy import omxpy

t = str(input())

finalurl = re.search("(?P<url>https?://[^\s]+)", t).group("url")

omx = omxpy(finalurl, "youtube")


def receiveOMXControls():
    while True:
        t = str(input())
        if t == "togglepause":
            omx.toggle_pause()
        elif t == "stop":
            omx.stop()
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

receiveOMXControls()
