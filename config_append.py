
from device import Device
import time




if __name__ == '__main__':
	f = open('output.log', 'w', buffering=0)
	DUT = Device('EOS', '10.52.2.222', 10022)
	DUT.write('\n')
	time.sleep(3)
	print(DUT.read_until('Username'))
	
	f.write(DUT.login())
	
	for x in range(500):
		print('*** Starting iteration %d ***' % x)
		f.write('\n\n*** Starting iteration %d ***\n\n' % x)
		DUT.clearConfig()
		# It takes about 3 minutes to come back online.
		output = DUT.read_until('Username:')
		output = output + DUT.login()
		f.write(output)
		# append the backup config.
		DUT.write(['config slot2/backup2.cfg append','y','y'])
		# This should wait for the append to finish.
		output = DUT.read_until_prompt()
		f.write(output)
		if 'MII' in output:
			print('Found an issue')
			break
		else:
			print('No issue found')
		#DUT.clearConfig()
	f.close()