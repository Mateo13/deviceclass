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
		print("////////////////////////////////////////////////////////////")
		print("mtest execution completed")
		if b'0 errors' in self.res:
			print("Test Result: PASS")
		else: 
			print("Test Result: FAIL")
		print("////////////////////////////////////////////////////////////")

	#Execute test.
	def execute(self):
		self.tn.login()
		print("===============================================================================")
		print("Beginning " + self.name)
		print("===============================================================================")
		print("Reseting device for BootROM testing...")
		self.tn.reset()
		self.tn.read_until('enter the bootrom:')
		print("Executing mtest from BootROM...")
		self.tn.write('     ')
		self.tn.read_until('BootRom >')
		self.tn.write('mtest\n')
		self.res = self.tn.read()
		self.res = self.tn.read_until('BootRom >')
		print(self.res)
		self.tn.write('boot\n')		
	
if __name__ == '__main__':
	tel = Device('EXOS', '10.52.2.33', 2009)
	test = BootROMTest('BootROM Test', tel)
	test.execute()
	test.checkResult()