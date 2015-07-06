#This test will execute 'mt' from BootROM to test all memory.

#Imports
from device import Device

#Define class to execute test.
class BootROMTest(object):
	#Initialize class.
	def __init__(self, telnet_device):
		self.tn = telnet_device
		
	#Check if test passed.
	def check(self):
		if b'0 errors' in self.res:
			print("Test Result: PASS\n")
		else: 
			print("Test Result: FAIL\n")

	#Execute test.
	def execute(self):
		self.tn.login()
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
		self.check()
		
	
if __name__ == '__main__':
	tel = Device('EXOS', '10.52.2.33', 2009)
	test = BootROMTest(tel)
	test.execute()
	