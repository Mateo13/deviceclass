'''This test will create and delete a specified number of VLANs for a specified number of 
repetitions.  These parameters can be modified when initializing the test.'''

#Imports
from test import Test
from device import Device
import random
import time


#Define the test.
class VLANTest(Test):
	#Create VLANTest object and assign associated telnet object to test.
	def __init__(self, name, telnetDevice, f, num_ports=48, num_iter=20, num_VLANs=1000):
		super().__init__(name, f)
		self.tn = telnetDevice
		self.rnd = random.Random()
		self.num_ports = num_ports
		self.num_iter = num_iter
		self.num_VLANs = num_VLANs
		self.rnd.seed()
		self.testResult = 'FAIL'
		self.iterResults = []
	
	#Change number of ports to add to VLANS.
	def changeNumPorts(self, num):
		self.num_ports = num

	#Change number of iterations.
	def changeNumIter(self, num):
		self.num_iter = num

	#Change number of VLANs to create.
	def changeNumVLANs(self, num):
		self.num_VLANs = num

	#Create n random VLANs.
	def createVLANs(self):
		self.tn.read()
		vlanList = [i for i in range(2,4095)]
		for i in range(1,(self.num_VLANs + 1)):
			rndNum = self.rnd.choice(vlanList)
			vlanList.remove(rndNum)
			self.logOutput("Creating VLAN " + str(rndNum) + "...")
			self.tn.write('create vlan ' + str(rndNum) + '\n',300)
			self.tn.write('conf vlan ' + str(rndNum) + ' add port 1-' + str(self.num_ports) 
				+ ' tag\n', 300)
			self.logOutput("VLAN " + str(rndNum) + " created.")
			time.sleep(1)
	
	#Delete all VLANs.
	def deleteVLANs(self):
		self.tn.read()
		self.logOutput("Deleting all non-default VLANs...")
		self.tn.read_until_prompt(1)
		self.tn.write('delete VLAN 2-4094\n', 500)
		self.logOutput("VLANs deleted.")
	
	#Check if test passed.
	def checkCreate(self):
		self.tn.read()
		temp = self.tn.write('show vlan | include "Total"\n', 500)
		self.logOutput(temp.decode('utf-8'), False)
		match = b'Total number of VLAN(s) : ' + str(self.num_VLANs + 2).encode('ascii')
		if match  in temp:
			self.testResult = 'PASS'
	
	#Check if VLANs were successfully deleted.
	def checkDelete(self):
		self.tn.read()
		temp = self.tn.write('show vlan\n', 500)
		self.logOutput(temp.decode('utf-8'), False)
		if b'Total number of VLAN(s) : 2' not in temp:
			self.testResult = 'FAIL'
	
	#Log result of current iteration of test.
	def updateIterResult(self, iter):
		if self.testResult == 'PASS':
			self.iterResults.append(True)
		else:
			self.iterResults.append(False)

	#Return final test result
	def checkResult(self):
		numPassed = 0
		for i in self.iterResults:
			if i:
				numPassed += 1
		if numPassed == self.num_iter:
			self.finalResultPass = True
		else:
			self.finalResultPass = False
		self.printResultBanner(["VLAN testing completed.", "Number of passing runs: " 
			+ str(numPassed)], self.finalResultPass)
		
	#Execute test.
	def execute(self):
		self.printBeginBanner()
		self.tn.login()
		self.deleteVLANs()
		for i in range(1,(self.num_iter + 1)):
			self.printBeginIterBanner(i)
			self.createVLANs()
			self.checkCreate()
			self.deleteVLANs()
			self.checkDelete()
			self.updateIterResult(i)

#Class testing.			
if __name__ == '__main__':
	tel = Device('EXOS', '10.52.2.33', 2009)
	f = open('vlans_testLog.txt', 'wb')
	test = VLANTest('Create/Delete VLANs Test', tel, f)
	test.execute()
	test.checkResult()
	f.close()