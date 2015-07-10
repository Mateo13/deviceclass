'''A test to perform a rescue image download on the device.'''

#Imports
from test import Test
from device import Device 


#Define test class.
class RescueTest(Test):
	#Initialize class.
	def __init__(self, name, telnet_device, tftp_server_ip, test_image_directory, f, num_iter = 2, 
		dut_ip = '192.168.1.9', dut_gw = '192.168.1.1', dut_nm = '255.255.255.0'):
		super().__init__(name, f)
		self.tn = telnet_device
		self.tftp_ip = tftp_server_ip
		self.image = test_image_directory
		self.num_iter = num_iter
		self.dut_ip = dut_ip
		self.dut_gw = dut_gw
		self.dut_nm = dut_nm
		self.testResult = 'PASS'

	#Check test result.
	def checkResult(self):
		if self.testResult == 'PASS':
			self.finalResultPass = True
		else:
			self.finalResultPass = False
		self.printResultBanner("Rescue testing complete.\nTotal iterations: " + self.num_iter + '\n',
			self.finalResultPass)


	#Execute test
	def execute(self):
		self.printBeginBanner()
		for i in range(1,(self.num_iter + 1)):
			self.printBeginIterBanner(i)
			self.tn.login()
			self.logOutput("Resetting device for rescue image testing...")
			self.tn.reset()
			self.tn.read_until('enter the bootrom:')
			self.logOutput("Executing rescue image test...")
			self.tn.write('     ')
			self.tn.read_until('BootRom >')
			self.tn.write('enable')
			self.tn.read_until('BootRom >')
			self.tn.write('configip ip ' + self.dut_ip + ' gw ' + self.dut_gw + ' nm ' + self.dut_nm)
			self.tn.read_until('BootRom >')
			self.tn.write('download image ' + self.tftp_ip + ' ' + self.image)
			self.tn.read_until('Ok to continue? (Y/N)')
			self.tn.write('y')
			self.tn.read_until('ENTER to reboot:')
			self.tn.write('\n')
			self.tn.read_until('Authentication Service (AAA) on the master node is now available for login.')
			self.tn.write('q')

if __name__ == '__main__':
	t = Device('EXOS', '10.52.2.33', 2009)
	f = open('rescueTestLog.txt', 'ab')
	r = RescueTest("Rescue Test", t, '10.52.4.40', 'firmware/images/summitX-16.1.1.4.xos', f, 1)
	r.execute()
	r.checkResult()