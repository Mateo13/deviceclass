import time
import sys
import re

from telnetlib import Telnet

# Device base class.
class Device():
	def __init__(self, address, port, login='admin', passwd=''):
		self.username = login
		self.password = passwd
		self.tn = Telnet(address, port, 20)
	
	# READ functions
	# Basic read function.
	def read(self):
		# Basic read function.  Just read whatever is ready.
		return self.tn.read_very_eager()
	# Read until we find what is specified.
	def read_until(self, s, timeout=300):
		return self.tn.read_until(s.encode('ascii'), timeout)
	# Same as read_until except returns None if nothing is found.
	def read_find(self, s, timeout=300):
		output = self.read_until(s, timeout)
		if s in str(output):
			return output
		else:
			return None
	# Read until ANY prompt is found.
	def read_until_prompt(self, timeout=300):
		reYesNo = b'\([yY]/[nN](/q)*\)'
		(index, match, output) = self.tn.expect([reYesNo, self.prompt, b'Username:', b'login:', b'[pP]assword'], timeout)
		return output
	
	# WRITE functions
	# Accepts either a string or list of strings.  Returns all output it gets while waiting for prompts.
	def write(self, commands):
		if isinstance(commands, str):
			self.tn.write(commands.encode('ascii') + b'\n')
			time.sleep(1)
		else:
			for command in commands:
				self.tn.write(command.encode('ascii') + b'\n')
				time.sleep(1)
				#temp = temp + self.read_until_prompt(timeout)
		
	
	# Usability commands - Better living thru laziness.
	def reset(self):
		return self.write(self.reset_cmd)

	def login(self):
		self.write('\n')
		output = self.read_until_prompt()
		self.write(self.username )
		self.write(self.password )
		output = output + self.read_until_prompt()
		return output
		
	# Close the telnet connection.
	def closeconnection(self):
		self.tn.close()


# EOS device.
class EOSDevice(Device):
	# attributes specific to EOS devices.
	prompt = b'->'
	reset_cmd = ['reset sys', 'y']

	def login(self):
		super().login()
		self.write('set cli completion disable')

class EXOSDevice(Device):
	# attributes specific to ExOS devices.
	prompt = b' # '
	reset_cmd = ['reboot', 'y']

	def login(self):
		super().login()
		self.write('disable clipaging')


