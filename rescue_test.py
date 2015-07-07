#A test to perform a rescue image download on the device.

#Imports
from test import Test
from device import Device 

#Global vars
numIter = 2
dut_ip = '192.168.1.9'
dut_gw = '192.168.1.1'
dut_nm = '255.255.255.0'

#Define test class.
class RescueTest(Test):
	#Initialize class.
	def __init__(self, name, telnet_device, tftp_server_ip, test_image_directory):
		super().__init__(name)
		self.tn = telnet_device
		self.tftp_ip = tftp_server_ip
		self.image = test_image_directory
		self.testResult = 'PASS'

	#Check test result.
	def checkResult(self):
		print("////////////////////////////////////////////////////////////")
		print("Rescue testing complete.")
		print("Total iterations: " + numIter)
		print("Test Result: " + self.testResult)
		print("////////////////////////////////////////////////////////////")


	#Execute test
	def execute(self):
		print("===============================================================================")
		print("Beginning " + self.name)
		print("===============================================================================")
		for i in range(1,(numIter + 1)):
			print("============================================================")
			print("Beginning iteration " + str(i))
			print("============================================================")
			self.tn.login()
			print("Resetting device for rescue image testing...")
			self.tn.reset()
			self.tn.read_until('enter the bootrom:')
			print("Executing rescue image test...")
			self.tn.write('     ')
			self.tn.read_until('BootRom >')
			self.tn.write('enable')
			self.tn.read_until('BootRom >')
			self.tn.write('configip ip ' + dut_ip + ' gw ' + dut_gw + ' nm ' + dut_nm)
			self.read_until('BootRom >')
			self.tn.write('download image ' + self.tftp_ip + ' ' + self.image)
			self.tn.read_until('Ok to continue? (Y/N)')
			self.tn.write('y')
			self.tn.read_until('ENTER to reboot:')
			self.tn.write('\n')
			self.tn.read_until('Authentication Service (AAA) on the master node is now available for login.')
			self.tn.write('q')
