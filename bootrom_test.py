#This test will execute 'mt' from BootROM to test all memory.

#Imports
from test import Test
from device import Device

#Define class to execute test.
class BootROMTest(Test):
	#Initialize class.
	def __init__(self, name, telnet_device):
		super().__init__(name)
		self.tn = telnet_device
		
	#Check if test passed.
	def checkResult(self):
		self.logOutput("////////////////////////////////////////////////////////////")
		self.logOutput("mtest execution completed")
		if b'0 errors' in self.res:
			self.logOutput("Test Result: PASS")
		else: 
			self.logOutput("Test Result: FAIL")
		self.logOutput("////////////////////////////////////////////////////////////")

	#Execute test.
	def execute(self):
		self.tn.login()
		self.logOutput("===============================================================================")
		self.logOutput("Beginning " + self.name)
		self.logOutput("===============================================================================")
		self.logOutput("Reseting device for BootROM testing...")
		self.tn.reset()
		self.tn.read_until('enter the bootrom:')
		self.logOutput("Executing mtest from BootROM...")
		self.tn.write('     ')
		self.tn.read_until('BootRom >')
		self.tn.write('mtest\n')
		self.res = self.tn.read()
		self.res = self.tn.read_until('BootRom >')
		self.logOutput(self.res)
		self.tn.write('boot\n')		
	
if __name__ == '__main__':
	tel = Device('EXOS', '10.52.2.33', 2009)
	test = BootROMTest('BootROM Test', tel)
	f = open('bootrom_testLog.txt','ab')
	test.setLog(f)
	test.execute()
	test.checkResult()
	f.close()