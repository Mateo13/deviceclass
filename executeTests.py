'''Main class to run all test execution.'''

#Imports
from test import Test
from device import Device
import install_test
import create_delete_VLANS
import rescue_test
import bootrom_test

#############################VARS FOR INDIVIDUAL TEST CONFIGURATION#################################
#DUT Info
DUT_DEVICE_TYPE				= 'EXOS'
DUT_TELNET_IP				= '10.52.2.33'
DUT_TELNET_PORT				= 2009
TEST_LOG_FILENAME			= 'testLog.txt'


#BootROM Test Vars
#None

#Rescue Test Vars
RT_NUMBER_OF_ITERATIONS 	= 2
RT_TFTP_SERVER_IP  			= '10.52.4.40'
RT_IMAGE_LOCATION 			= 'firmware/images/'
RT_IMAGE_NAME 				= 'summitX-16.1.1.4.xos'
RT_DUT_IP_ADDRESS 			= '192.168.1.9'
RT_DUT_GW_ADDRESS 			= '192.168.1.1'
RT_DUT_NETMASK 				= '255.255.255.0'

#Create/Delete VLANs Test Vars
VT_NUM_PORTS_PER_VLAN		= 48
VT_NUM_ITERATIONS 			= 20
VT_NUMBER_OF_VLANS			= 1000

#Install Test Vars
IT_TFTP_SERVER_IP			= '10.52.4.40'
IT_IMAGE_LOCATION			= 'firmware/images/'
IT_IMAGE_NAME				= 'summitX-16.1.1.4.xos'
IT_NUM_ITERATIONS			= 100
IT_DUT_IP_ADDRESS			= '192.168.1.9/24'
IT_DUT_GW_ADDRESS			= '192.168.1.1'
#################################DO NOT EDIT BELOW THIS POINT#######################################

#Create Device object for DUT
dut = Device(DUT_DEVICE_TYPE, DUT_TELNET_IP, DUT_TELNET_PORT)
tests = []

#Create log file
f = open(TEST_LOG_FILENAME, 'wb')

#Add BootROM test to list of tests to execute.
t = bootrom_test.BootROMTest('BootROM Test', dut)
tests.append(t)

#Add Rescue Image Test to list of tests to execute.
t = rescue_test.RescueTest('Rescue Image Test', dut, RT_TFTP_SERVER_IP, 
	RT_IMAGE_LOCATION + RT_IMAGE_NAME, RT_NUMBER_OF_ITERATIONS, RT_DUT_IP_ADDRESS, 
	RT_DUT_GW_ADDRESS, RT_DUT_NETMASK)
tests.append(t)

#Add VLAN test to list of tests to execute and update num_ports.
t = create_delete_VLANS.VLANTest('VLAN Test', dut, f, VT_NUM_PORTS_PER_VLAN, VT_NUM_ITERATIONS,
	VT_NUMBER_OF_VLANS)
tests.append(t)

#Add InstallTest to list of tests to execute.
t = install_test.InstallTest('Install Test', dut, IT_TFTP_SERVER_IP, 
	IT_IMAGE_LOCATION + IT_IMAGE_NAME, f, IT_NUM_ITERATIONS, IT_DUT_IP_ADDRESS, IT_DUT_GW_ADDRESS)
tests.append(t)

#Run all tests.
for i in tests:
	i.execute()
	i.checkResult()
