import D
import time

geteeprom = 'debug hal show optic-info ee port %d'
IP = '10.52.3.3'
portnumber = 10018

def findeepromdump(output):
	#output = output.splitlines()
	eepromdump = []
	linesleft = 0
	for line in output:
		if linesleft > 0:
			eepromdump.append(line)
			linesleft-= 1
		if line.startswith('eeprom:'):
			# the next 13 lines are the eeprom dump
			linesleft = 16
			
	return eepromdump

def eepromprint(eeprom, out):
	for line in eeprom:
		print(line)
		out.write(line)

good = open('davesgood.txt')
debughaloutput = []
goodeeproms = []
portno= -1
for line in good:
	debughaloutput.append(line)
	if 'debug hal show op' in line:
		portno += 1
		eeprom = findeepromdump(debughaloutput)
		if len(eeprom) > 1:
			eeprom.insert(0, 'port number: %d' % portno)
			goodeeproms.append(eeprom)
		debughaloutput = []


good.close()


logfile = open('eepromdumplog.txt', 'w', 1)

DUT = D.EXOSDevice(IP, portnumber)
nochanges = True
attemptcounter = 1


while(nochanges):
	print('Attempt number %d' % attemptcounter)
	attemptcounter+= 1
	eepromstotest = []
	print('Waiting to log in.')
	tempoutput = DUT.login()
	logfile.write(tempoutput.decode())
	print('Logged in.')
	time.sleep(5) # let things settle out a little.

	for port in range(1,6):
		print('Checking eeprom of port %d' % port)
		logfile.write(DUT.read().decode())
		DUT.write(geteeprom % port)
		output = DUT.read_until_prompt()
		output = output.decode(errors='ignore')
		logfile.write(output)
		eeprom = findeepromdump(output.splitlines())
		#print(eeprom)
		if len(eeprom) > 1:
			eeprom.insert(0, 'port number: %d' % port)
			eepromstotest.append(eeprom)

	print('Number of eeproms found: %d' % len(eepromstotest))
	if len(eepromstotest) != len(goodeeproms):
		print('Not all eeproms found.  Quitting.')
		nochanges = False

	for good,test in zip(goodeeproms,eepromstotest):
		for goodline,testline in zip(good,test):
			if goodline.strip() != testline.strip():
				print('Found a difference!')
				print(goodline)
				print(testline)
				print(good[0])
				nochanges = False
	
	if nochanges:
		print('Nothing found.  Rebooting.')
		print('****************')
		DUT.reset()
		time.sleep(170)
		logfile.write(DUT.read().decode())

logfile.close()
