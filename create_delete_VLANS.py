#This test will create and delete 1000 VLANs for a specified number of repetitions.

#Imports
from device import Device
import random


#Define the test.
class VLANTest(object):
	#Create VLANTest object and assign associated telnet object to test.
	def __init__(self, telnetDevice):
		self.tn = telnetDevice
		self.rnd = random.Random()
		self.rnd.seed()
		self.testResult = 'FAIL'
		
	#Create 1000 random VLANs.
	def createVLANs(self):
		self.tn.read()
		vlanList = [i for i in range(2,4095)]
		for i in range(1,1001):
			rndNum = self.rnd.choice(vlanList)
			vlanList.remove(rndNum)
			print("Creating VLAN " + str(rndNum) + "...")
			self.tn.write('create vlan ' + str(rndNum) + '\n')
			self.tn.read_until('#')
			print("VLAN " + str(rndNum) + " created.")
	
	#Delete all VLANs.
	def deleteVLANs(self):
		self.tn.read()
		print("Deleting all non-default VLANs...")
		self.tn.write('delete VLAN 2-4094\n')
		self.tn.read_until('#')
		print("VLANs deleted.")
	
	#Check if test passed.
	def checkCreate(self):
		self.tn.read()
		self.tn.write('show vlan\n')
		temp = self.tn.read_until('#')
		if b'Total number of VLAN(s) : 12' in temp:
			self.testResult = 'PASS'
	
	#Check if VLANs were successfully deleted.
	def checkDelete(self):
		self.tn.read()
		self.tn.write('show vlan\n')
		temp = self.tn.read_until('#')
		if b'Total number of VLAN(s) : 2' not in temp:
			self.testResult = 'FAIL'
		
	#Execute test.
	def execute(self):
		self.tn.login()
		for i in range(1,20):
			print("=====================================================")
			print("Beginning iteration " + str(i))
			print("=====================================================")
			self.createVLANs()
			self.checkCreate()
			self.deleteVLANs()
			self.checkDelete()
			print("Test Result: " + self.testResult)

#Class testing.			
if __name__ == '__main__':
	tel = Device('EXOS', '10.52.2.33', 2009)
	test = VLANTest(tel)
	test.execute()