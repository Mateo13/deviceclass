
from device import Device
import time
import random



if __name__ == '__main__':
	f = open('output.log', 'w', buffering=0)
	DUT = Device('EOS', '10.52.2.222', 10022)
	DUT.write('\n')
	time.sleep(3)
	print(DUT.read_until('Username'))
	
	f.write(DUT.login())
	
	for x in range(500):
		# Sleep a random amount of time to change the timing slightly each iteration.
		sleeptime = random.randrange(30)
		print('*** Starting iteration %d with a %d second wait.***\n\n' % (x,sleeptime))
		f.write('\n\n*** Starting iteration %d  with a %d second wait.***\n\n' % (x,sleeptime))
		
		print('Clearing config.')
		DUT.clearConfig()
		# It takes about 3 minutes to come back online.
		output = DUT.read_until('Username:')
		print('Logging into DUT')
		output = output + DUT.login()
		f.write(output)
		time.sleep(sleeptime)
		print('Appending the config.')
		# append the backup config.
		output = DUT.write(['config slot2/backup2.cfg append','y'])
		# This should wait for the append to finish.
		output = output + DUT.read_until_prompt()
		f.write(output)
		if 'MII' in output:
			print('Found an issue')
			break
		elif 'Boot ROM' in output:
			print('DUT reset.  quitting.')
			break
		elif 'DistServ' in output:
			print('Possible watchdog error.  Check the logs.')
		else:
			print('No issue found')
		#DUT.clearConfig()
	f.close()