'''Bring indicated ports down/up a given number of times'''

#Imports
from device import Device
from test import Test
import time
import sys


#Define test.
class LinkTest(Test):
	#Initialize test.
	def __init__(self, name, telnet_device, f, ports=[26,32], num_iter=2):
		super().__init__(name, f)
		self.tn = telnet_device
		self.ports = ports
		self.num_iter = num_iter

	#Remove a port from the list
	def removePortFromList(self, port):
		try:
			self.ports.remove(port)
		except:
			print("The given port is not in the current portlist.  Ignoring remove request.")

	#Add a port to the list
	def addPortToList(self, port):
		if self.ports.count(port) > 0:
			print("The given port is already in the current portlist.  Ignoring add request.")
		else:
			self.ports.append(port)

	#Print the current portlist
	def printPortList(self):
		print(self.ports)

	#Bring down a given port.
	def downPort(self, port):
		temp = self.tn.read_until_prompt(2)
		self.logOutput("Disabling port " + str(port) + "...")
		temp = temp + self.tn.write('set port disable ge.1.' + str(port), 5)
		self.checkForError(temp)

	#Bring up a given port:
	def upPort(self, port):
		temp = self.tn.read_until_prompt(2)
		self.logOutput("Enabling port " + str(port) + "...")
		temp = temp + self.tn.write('set port enable ge.1.' + str(port), 5)
		self.checkForError(temp)

	#Check for error message and quit if found.
	def checkForError(self, text):
		temp = text.decode('utf-8')
		if "bcmCNTR" in temp:
			self.logOutput(temp)
			self.logOutput("**********ERROR FOUND!  Exiting program...**********")
			sys.quit()

	#Begin linkflap test
	def execute(self):
		self.tn.login()
		self.printBeginBanner()
		if self.num_iter:
			for i in range(1, self.num_iter + 1):
				self.printBeginIterBanner(i)
				for j in self.ports:
					self.downPort(j)
				time.sleep(1)
				for j in self.ports:
					self.upPort(j)
				self.logOutput("Pausing for 5 seconds between iterations...")
				time.sleep(5)
		else:
			i = 1
			while True:
				self.printBeginIterBanner(i)
				for j in self.ports:
					self.downPort(j)
				time.sleep(1)
				for j in self.ports:
					self.upPort(j)
				self.logOutput("Pausing for 5 seconds between iterations...")
				time.sleep(5)
				i += 1

if __name__ == '__main__':
	d = Device('EOS', '10.52.2.33', 2004)
	f = open('linkflapLog.txt', 'wb')
	l = LinkTest('Linkflap Test', d, f, [25,26,27,28,29,30,31,32], False)
	l.execute()