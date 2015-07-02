#Imports
import time
import random
from telnetlib import Telnet
	
#Define an EOS/EXOS device to connect to.
class Device(object):
	#Create Device object and assign type (EOS/EXOS), IP, port, and username/password.
	def __init__(self, type, address, port, login='admin', passwd=''):
		self.username = login
		self.password = passwd
		print('Connecting to ' + type + ' device...')
		if type == 'EOS':
			self.reset_cmd = 'reset sys'
		elif type == 'EXOS':
			self.reset_cmd = 'reboot'
		else:
			raise ValueError("Invalid device type!")
		self.type = type
		
		self.tn = Telnet(address, port, 20)
		print(self.tn.read_until(b'Username:', 20))
		print("Connected to %s" % address)
	
	#Reset the device.
	def reset(self):
		self.write([self.reset_cmd, 'y'])
			
	#Close telnet connection
	def closeconnection(self):
		self.tn.close()
		
	#Login to the device
	def login(self):
		self.write(self.username + '\n')
		time.sleep(1)
		self.write(self.password + '\n')
		time.sleep(1)
		print(self.tn.read_very_eager())
		if self.type == 'EXOS':
			d.write('disable clipaging')
		if self.type == 'EOS':
			d.write('set cli completion disable')
			
	#Write command(s) to the device.
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
	
	#Read output
	def read(self):
		time.sleep(1)
		return self.tn.read_very_eager()

#Some object testing.
if __name__ == '__main__':
	'''d = device('10.52.2.222', 10027)
	d.login()
	d.write('sh port stat -i')
	print(d.read())
	d.reset()
	time.sleep(60)
	d.login()
	print(d.read())
	d.closeconnection()
	#print(d.read())'''
	d = Device('EXOS', '10.52.2.33', 2009)
	d.login()
	d.write('sh port no')
	print(d.read())
	d.reset()
	time.sleep(60)
	