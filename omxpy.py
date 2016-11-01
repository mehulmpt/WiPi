import pexpect
import re
import os
from threading import Thread
import time

class omxpy(object):
    _DONE_REXP = re.compile(b"have a nice(.*?)")

    _LAUNCH_CMD = '/usr/bin/omxplayer "%s" -b --key-config=keys'
    _PAUSE_CMD = 'x'
    _TOGGLE_SUB_CMD = 's'
    _QUIT_CMD = 'q'

    _JUMP_30SEC = 'm'
    _FALL_30SEC = 'o'
    _JUMP_10MIN = 'n'
    _FALL_10MIN = 'z'
    _REWIND_ = 'r'
    _FORWARD_ = 'f'
    _SUBTITLE_ = 't'
    _DELAYSUB_ = 'd'
    _FASTSUB_ = 'i'

    subtitles_visible = True

    def killchild(self):
        while True:
            time.sleep(3)
            index = self._process.expect([pexpect.TIMEOUT,pexpect.EOF,self._DONE_REXP], timeout=5)
            if index != 0:
                os.system("pkill -f media.py")
                os.system("pkill -f youtube.py")
                os.system("pkill -f pyomxplayer.py")
                self._process.kill(0)
                
    def kickstart(self, cmd):
        self._process = pexpect.spawn(cmd)
        self._process.interact() # remove this in production
        
    def __init__(self, mediafile, args=None, start_playback=False):
        if not args:
            args = ""
        cmd = self._LAUNCH_CMD % (mediafile)
        if args == "youtube":
            cmd = '/bin/bash -c "/usr/bin/omxplayer -s `youtube-dl -g -f best '+mediafile+'` --key-config=keys"'

        Thread(target=self.kickstart, args=(cmd,)).start()
        Thread(target=self.killchild, args=()).start()

    def jump30s(self):
        self._process.send(self._JUMP_30SEC)

    def fall30s(self):
        self._process.send(self._FALL_30SEC)

    def jump10min(self):
        self._process.send(self._JUMP_10MIN)

    def fall10min(self):
        self._process.send(self._FALL_10MIN)        

    def toggle_pause(self):
        self._process.send(self._PAUSE_CMD)

    def toggle_subtitles(self):
        self._process.send(self._TOGGLE_SUB_CMD)

    def fastf(self):
        self._process.send(self._FORWARD_)

    def rewind(self):
        self._process.send(self._REWIND_)

    def delaysub(self):
        self._process.send(self._DELAYSUB_)

    def fastsub(self):
        self._process.send(self._FASTSUB_)

    def stop(self):
        self._process.send(self._QUIT_CMD)
        self._process.terminate(force=True)
