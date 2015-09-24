from telnetlib import Telnet



'''
interface vlan-if3
 ip address 10.0.1.1/24
 exit
interface tengige4_0
 access vlan  1
exit

'''
class DPTech(object):
	def __init__(self, address, port):
		print('Conntecting to device at %s:%d' %(address, port))
		self.tn = Telnet(address, port, 20)
		
	def write(self, cmd):
		cmd = cmd.encode('ascii')
		self.tn.write(cmd)
	
	def read_until(self, text, timeout=2):
		text = text.encode('ascii')
		return self.tn.read_until(text, timeout)



# connect to device
dut = DPTech('10.52.2.222', 10017)
# login
dut.write('\n')
print(dut.read_until('Password:', 3))
dut.write('DPTECH\n')
print(dut.read_until('<DPTECH>'))

# get to conf mode
dut.write('conf\n')
print(dut.read_until('[DPTECH]', 10))

# create 64 vlan interfaces
for vlan in range(2,66):
	print('		***** Making vlan %d  *****' % vlan)
	dut.write('interface vlan-if%d\n' % vlan)
	dut.write('no ip address 192.85.%d.2/24\n' % vlan)
	dut.write('ip address 192.85.%d.1/24\n' % vlan)
	dut.write('exit\n')
	print(dut.read_until('[DPTECH]',10))

#for portNum in range(0,32):
#	print('		***** assigning %d to interface tengige2_%d  *****' % (portNum + 2, portNum))
#	dut.write('interface tengige2_%d\n' % portNum )
#	dut.write('access vlan %d\n' % (portNum + 2))
#	dut.write('exit\n')
#	print(dut.read_until('[DPTECH]',10))

#for portNum in range(0,32):
#	print('		***** assigning %d to interface tengige2_%d  *****' % (portNum + 34, portNum))
#	dut.write('interface tengige4_%d\n' % portNum )
#	dut.write('access vlan %d\n' % (portNum + 34))
#	dut.write('exit\n')
#	print(dut.read_until('[DPTECH]',10))

	