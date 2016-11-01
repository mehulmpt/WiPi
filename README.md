# WiPi
Wireless media server for raspberry pi on LAN. Allows you to stream YouTube videos and your media files on your raspberry (technically, any device connected to your TV through HDMI) and show it on your TV.

#config
0. Connect your raspberry to your home WiFi. Connect your phone to your home WiFi.
1. Clone this repository on your raspberry by running `git clone https://github.com/mehulmpt/WiPi` on your raspberry terminal.
2. Open the WiPi folder (cloned) on raspberry
3. Run `chmod +755 boot.sh` in terminal
4. Run `./boot.sh` in terminal
5. Wait for setup to complete.

Note: For future runs, do `python3 sock.py` from terminal (after navigating to WiPi folder) instead of `./boot.sh`

#Android App

Use this android app to control your Raspberry: https://play.google.com/store/apps/details?id=com.wipi

Tip: To stream youtube videos, open your YouTube app and share the video to WiPi (i.e. open video -> share this video -> select WiPi)

Please let me know about any bugs you face. Feel free to contribute.
