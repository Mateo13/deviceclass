#This test will create and delete 1000 VLANs for a specified number of repetitions.

#Imports
from test import Test
from device import Device
import random

#Global Vars
num_ports = 24
numIter = 20
numVLANS = 1000

#Define the test.
class VLANTest(Test):
	#Create VLANTest object and assign associated telnet object to test.
	def __init__(self, name, telnetDevice):
		super().__init__(name)
		self.tn = telnetDevice
		self.rnd = random.Random()
		self.rnd.seed()
		self.testResult = 'FAIL'
		self.iterResults = []
		
	#Create 1000 random VLANs.
	def createVLANs(self):
		self.tn.read()
		vlanList = [i for i in range(2,4095)]
		for i in range(1,(numVLANS + 1)):
			rndNum = self.rnd.choice(vlanList)
			vlanList.remove(rndNum)
			print("Creating VLAN " + str(rndNum) + "...")
			self.tn.write('create vlan ' + str(rndNum) + '\n')
			self.tn.read_until('#')
			self.tn.write('conf vlan ' + str(rndNum) + ' add port 1-' + str(num_ports) + ' tag\n')
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
	
	#Log result of current iteration of test.
	def updateIterResult(self, iter):
		if self.testResult == 'PASS':
			self.iterResults[iter] = True
		else:
			self.iterResults[iter] = False

	#Return final test result
	def checkResult(self):
		numPassed = 0
		for i in self.iterResults:
			if i:
				numPassed += 1
		print("////////////////////////////////////////////////////////////")
		print("VLAN testing completed.")
		print("Number of passing runs: " + str(numPassed))
		if numPassed == numIter:
			print("Test Result: PASS")
		else:
			print("Test Result: FAIL")
		print("////////////////////////////////////////////////////////////")
		
	#Execute test.
	def execute(self):
		print("===============================================================================")
		print("Beginning " + self.name)
		print("===============================================================================")
		self.tn.login()
		for i in range(1,(numIter + 1)):
			print("============================================================")
			print("Beginning iteration " + str(i))
			print("============================================================")
			self.createVLANs()
			self.checkCreate()
			self.deleteVLANs()
			self.checkDelete()
			self.updateIterResult(i)

#Class testing.			
if __name__ == '__main__':
	tel = Device('EXOS', '10.52.2.33', 2009)
	test = VLANTest('Create/Delete VLANs Test', tel)
	test.execute()
	test.checkResult()