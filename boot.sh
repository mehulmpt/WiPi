#!/bin/bash

# checking for all requirements, etc.

echo "----------------------------------------";
echo "Checking for all the dependencies.";

echo "----------------------------------------";
echo "----------------------------------------";
echo "Updating repos \n";
echo "----------------------------------------";

sudo apt-get update;

echo "----------------------------------------";
echo "Installing/Updating omxplayer...";
echo "----------------------------------------";

sudo apt-get install omxplayer;

echo "----------------------------------------";
echo "Make sure you have python3 available! (Just sayin')";
echo "----------------------------------------";

echo "----------------------------------------";
echo "Installing/Updating pexpect python module\n";

echo "----------------------------------------";
sudo pip3 install pexpect;

echo "----------------------------------------";
echo "Installed all dependencies.. Should work (probably :P).";

echo "----------------------------------------";


echo "----------------------------------------";

echo "Starting WiPi. Enjoy!";

echo "----------------------------------------";

python3 sock.py;
