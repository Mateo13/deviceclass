#Imports
import time
import random
from telnetlib import Telnet
import sys
import re

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
		self.write('\n')
		self.read_until_prompt(10)
		print("Connected to %s:%d" % (address, port))
	
	#Reset the device.
	def reset(self):
		self.write([self.reset_cmd, 'y'])
			
	#Close telnet connection
	def closeconnection(self):
		self.tn.close()
		
	#Login to the device
	def login(self):
		self.write(self.username + '\n')
		self.write(self.password + '\n')
		if self.type == 'EXOS':
			temp = self.read_find('#', 4)
			if temp == None:
				print("Error logging into device: Incorrect username or bad password!\n")
				sys.exit()
			self.write('disable clipaging\n')
		else:
			temp = self.read_find('->', 4)
			if temp == None:
				print("Error logging into device: Incorrect username or bad password!\n")
				sys.exit()
			self.write('set cli completion disable\n')
		temp = temp + self.read()
		return temp
			
	#Write command(s) to the device.
	def write(self, commands, timeout=1):
		if isinstance(commands, str):
			#print('It is a string')
			self.tn.write(commands.encode('ascii') + b'\n')
			temp = self.read_until_prompt(timeout)
		else:
			#print('It is a list')
			temp = b''
			for command in commands:
				self.tn.write(command.encode('ascii') + b'\n')
				temp = temp + self.read_until_prompt(timeout)
		return temp
		
	#Read output
	def read(self):
		self.read_until_prompt(1)
		return self.tn.read_very_eager()

	#Read until given string.
	def read_until(self, s, timeout=300):
		return self.tn.read_until(s.encode('ascii'), timeout)
	
	#Same as read_until except returns null if timeout was reached (timeout was reached if the "read_until" string isn't in the return output).
	def read_find(self, s, timeout=300):
		temp = self.read_until(s, timeout)
		if s in str(temp):
			return temp
		else:
			return None
	
	#Read until OS prompt.
	def read_until_prompt(self, timeout=300):
		reYesNo = b'\([yY]/[nN](/q)*\)'
		(index, match, output) = self.tn.expect([reYesNo, b' # ', b'->', b'Username:', b'login:', b'[pP]assword'], timeout)
		#(index, match, output) = self.tn.expect([b' # ',b'->',reYesNo], timeout)
		return output

	#Clear running configuration on device.
	def clearConfig(self):
		if self.type == 'EOS':
			self.write(['clear config all', 'y'])
		if self.type == 'EXOS':
			self.write(['unconfig swi all', 'y'])
			
#Some object testing.
if __name__ == '__main__':
	d = Device('EXOS', '10.52.2.33', 2009)
	d.login()
	d.write('sh port no')
	print(d.read().decode("utf-8"))
	#d.reset()
	#time.sleep(60)
	