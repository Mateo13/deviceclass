import telnetlib
import time
import random
from optparse import OptionParser

prompt = "->"


class device:
	def __init__(self, address, port):
		self.tn = telnetlib.Telnet(address, port, 20)
		print(self.tn.read_until(b'Username:', 20))
		print('Connected to %s' % address)
		
	def reset(self):
		self.write(['admin', '', 'reset sys','y'])
	
	def closeconnection(self):
		self.tn.close()
	def login(self):
		self.write('admin')
		time.sleep(1)
		self.write('\n')
		time.sleep(1)
		print(self.tn.read_until(prompt.encode('ascii'),5))
		
	def write(self, commands):
		if isinstance(commands, str):
			#print('It is a string')
			self.tn.write(commands.encode('ascii') + b'\n')
			time.sleep(1)
		else:
			#print('It is a list')
			for command in commands:
				self.tn.write(command.encode('ascii') + b'\n')
				time.sleep(1)
	def read(self):
		time.sleep(1)
		return self.tn.read_until(prompt.encode('ascii'),5)

if __name__ == '__main__':
	d = device('10.52.2.222', 10027)
	d.login()
	d.write('sh port stat -i')
	print(d.read())
	d.reset()
	time.sleep(60)
	d.login()
	print(d.read())
	d.closeconnection()
	#print(d.read())
	