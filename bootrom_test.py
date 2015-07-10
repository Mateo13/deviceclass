'''This test will execute 'mt' from BootROM to test all memory.'''

#Imports
from test import Test
from device import Device

#Define class to execute test.
class BootROMTest(Test):
	#Initialize class.
	def __init__(self, name, telnet_device, f):
		super().__init__(name, f)
		self.tn = telnet_device
		
	#Check if test passed.
	def checkResult(self):
		if b'0 errors' in self.res:
			self.finalResultPass = True
		else: 
			self.finalResultPass = False
		self.logOutput(self.res.decode('utf-8'))
		self.printResultBanner("mtest execution completed", self.finalResultPass)

	#Execute test.
	def execute(self):
		self.tn.login()
		self.printBeginBanner()
		self.logOutput("Reseting device for BootROM testing...")
		self.tn.reset()
		self.tn.read_until('enter the bootrom:', 120)
		self.tn.write('     ')
		self.logOutput("Executing mtest from BootROM...")
		self.tn.read_until('BootRom >', 2)
		self.res = self.tn.write('mtest\n') + self.tn.read_until('BootRom >', 120)
		self.tn.write('boot\n', 200)		
	
if __name__ == '__main__':
	tel = Device('EXOS', '10.52.2.33', 2009)
	f = open('bootrom_testLog.txt','ab')
	test = BootROMTest('BootROM Test', tel, f)
	test.execute()
	test.checkResult()
	f.close()