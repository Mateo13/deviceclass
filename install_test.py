#This test will run 100 installs and verify that each one is successful.

#Imports.
from test import Test
from device import Device
import sys

#Define test class.
class InstallTest(Test):
	#Initialize class.
	def __init__(self, name, telnet_device, tftp_server_ip, test_image_directory):
		super().__init__(name)
		self.tn = telnet_device
		self.tftp_ip = tftp_server_ip
		self.image = test_image_directory
		self.testResult = 'FAIL'
		self.testFailed = False
	
	#Configure Mgmt VLAN for network access (required to run image downloads).
	def configNetwork(self, device_ip, device_gw):
		self.tn.write('conf vlan Mgmt ip ' + device_ip)
		self.tn.write('conf ipr add def ' + device_gw + ' vr VR-Mgmt')
	
	#Get current partition (primary/secondary) being used on the DUT.
	def getCurPartition(self):
		self.tn.read()
		self.tn.write('\n')
		self.tn.write('show switch')
		output = self.tn.read_until('Image Booted:')
		output = self.tn.read_until('\n').strip()
		self.partition = output.decode('utf-8')
		
	#Get current boot count.
	def getBootCount(self):
		self.tn.read()
		self.tn.write('\n')
		self.tn.write('show switch')
		output = self.tn.read_until('Boot Count:')
		output = self.tn.read_until('\n').strip()
		return int(output.decode('utf-8'))
		
	#Check if image was installed successfully.
	def checkResult(self):
		boot_count = self.getBootCount()
		if (self.startingBootCount + 1) == boot_count and self.testFailed == False:
			self.testResult = 'PASS'
		else: 
			self.testResult = 'FAIL'
			self.testFailed = True
			print("Test Result: FAIL")
			sys.exit()
		self.startingBootCount = boot_count
		print("New boot count: " + str(self.startingBootCount))
	
	#Execute test.
	def execute(self):
		print(self)
		self.tn.login()
		print("Configuring network access...")
		self.configNetwork('192.168.1.9/24', '192.168.1.1')
		print("Network access configured.")
		print("Getting current partition...")
		self.getCurPartition()
		print("Starting partition is: " + self.partition)
		self.startingBootCount = self.getBootCount()
		print("Starting boot count is: " + str(self.startingBootCount))
		for i in range(1,3):
			print("=====================================================")
			print("Beginning iteration " + str(i))
			print("=====================================================")
			print("Downloading image...")
			self.tn.read()
			self.tn.write('download image ' + self.tftp_ip + ' ' + self.image + ' vr VR-Mgmt')
			self.tn.write(['y', 'y'])
			self.tn.read_until_prompt()
			print("Image downloaded.")
			if self.partition == 'primary':
				self.partition == 'secondary'
			elif self.partition == 'secondary':
				self.partition == 'primary'
			else:
				print('ERROR: Invalid partition!  Exiting...')
				print('Test Result: FAIL')
				return
			print("Setting boot partition to " + self.partition + "...")
			self.tn.write('use image ' + self.partition)
			print("Rebooting...")
			self.tn.reset()
			self.tn.read_until('Authentication Service (AAA) on the master node is now available for login.')
			print("Reboot complete.")
			self.tn.read()
			self.tn.login()
			self.checkResult()
		print("Test Result: PASS")

#Some class testing.
if __name__ == '__main__':
	tel = Device('EXOS', '10.52.2.33', 2009)
	test = InstallTest("InstallTest", tel, '10.52.4.40', 'firmware/images/summitX-16.1.1.4.xos')
	test.execute()