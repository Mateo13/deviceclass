#Main class to run all test execution.

#Imports
from test import Test
from device import Device
import install_test
import create_delete_VLANS
import rescue_test
import bootrom_test

dut = Device('EXOS', '10.52.2.33', 2009)
tests = []

#Add InstallTest to list of tests to execute.
#t = install_test.InstallTest('Install Test', dut, '10.52.4.40', 'firmware/images/summitX-16.1.1.4.xos')
#t.numIter = 2
#tests.append(t)

#Add VLAN test to list of tests to execute and update num_ports.
t = create_delete_VLANS.VLANTest('VLAN Test', dut)
tests.append(t)

#Add BootROM test to list of tests to execute.
t = bootrom_test.BootROMTest('BootROM Test', dut)
tests.append(t)

#Add Rescue Image Test to list of tests to execute.
t = rescue_test.RescueTest('Rescue Image Test', dut, '10.52.4.40', 'firmware/images/summitX-16.1.1.4.xos')
tests.append(t)

#Create test log.
f = open('testLog.txt', 'ab')

for i in tests:
	i.setLog(f)
	i.execute()
	i.checkResult()
