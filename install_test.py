#This test will run 100 installs and verify that each one is successful.

#Imports.
from test import Test
from device import Device
import sys

#Global vars
numIter = 100
dut_ip = '192.168.1.9/24'
dut_gw = '192.168.1.1'

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
	def checkStatus(self):
		boot_count = self.getBootCount()
		if (self.bootCount + 1) == boot_count and self.testFailed == False:
			self.testResult = 'PASS'
		else: 
			self.testResult = 'FAIL'
			self.testFailed = True
		self.bootCount = boot_count
		self.logOutput("New boot count: " + str(self.bootCount))
	
	#Check test run results.
	def checkResult(self):
		self.logOutput("////////////////////////////////////////////////////////////")
		self.logOutput("Image downloads/reboots completed.")
		self.logOutput("Total number of reboots: " + str(self.bootCount - self.startingBootCount))
		self.logOutput("Test Result: " + self.testResult)
		self.logOutput("////////////////////////////////////////////////////////////")

	#Execute test.
	def execute(self):
		self.logOutput("===============================================================================")
		self.logOutput("Beginning " + self.name)
		self.logOutput("===============================================================================")
		self.tn.login()
		self.logOutput("Configuring network access...")
		self.configNetwork(dut_ip, dut_gw)
		self.logOutput("Network access configured.")
		self.logOutput("Getting current partition...")
		self.getCurPartition()
		self.logOutput("Starting partition is: " + self.partition)
		self.startingBootCount = self.getBootCount()
		self.bootCount = self.startingBootCount
		self.logOutput("Starting boot count is: " + str(self.startingBootCount))
		for i in range(1,(numIter + 1)):
			self.logOutput("============================================================")
			self.logOutput("Beginning iteration " + str(i))
			self.logOutput("============================================================")
			self.logOutput("Downloading image...")
			self.tn.read()
			self.tn.write('download image ' + self.tftp_ip + ' ' + self.image + ' vr VR-Mgmt')
			self.tn.write(['y', 'y'])
			self.tn.read_until_prompt()
			self.logOutput("Image downloaded.")
			if self.partition == 'primary':
				self.partition = 'secondary'
			elif self.partition == 'secondary':
				self.partition = 'primary'
			else:
				self.logOutput('ERROR: Invalid partition!  Exiting...')
				self.logOutput('Test Result: FAIL')
				return
			self.logOutput("Setting boot partition to " + self.partition + "...")
			self.tn.write('use image ' + self.partition)
			self.logOutput("Rebooting...")
			self.tn.reset()
			self.tn.read_until('Authentication Service (AAA) on the master node is now available for login.')
			self.logOutput("Reboot complete.")
			self.tn.read()
			self.tn.login()
			self.checkStatus()

#Some class testing.
if __name__ == '__main__':
	tel = Device('EXOS', '10.52.2.33', 2009)
	test = InstallTest("InstallTest", tel, '10.52.4.40', 'firmware/images/summitX-16.1.1.4.xos')
	f = open('testLog.txt', 'ab')
	test.setLog(f)
	test.execute()
	test.checkResult()
	f.close()