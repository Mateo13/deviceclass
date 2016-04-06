import D
import time
import logging

#set up some logging.
logfile = 'x670i2cerror.log'
log = logging.getLogger()
log.setLevel(logging.DEBUG)
fh = logging.FileHandler(logfile)
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
fmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(fmt)
ch.setFormatter(fmt)
log.addHandler(fh)
log.addHandler(ch)

log.info('**** Starting script! ****')

DUT = D.EXOSDevice('10.52.2.222', 10018)
time.sleep(2)

counter = 0
founderror = False
while(founderror == False):
	counter = counter + 1
	log.info('**** Iteration %d ****' % counter)
	if DUT.login() is False:
		# login failed for some reason...we should try again in a min. 
		sleep(30)
		DUT.login()
	log.info('Logged in.')
	time.sleep(4)
	x = DUT.showportconfig('1-18')
	log.info('Issued show port conf command.')
	for port in x:
		if '#' in port['media']:
			# Found an bad type.
			log.warning('Found an error in the port type in port # %s' % port['portnum'] )
			log.warning(port)
			founderror = True
		if 'R' in port['linkstate']:
			# link is down and it should be up.
			log.error('%s is down.' % port['portnum'])
			founderror = True
		if 'NONE' in port['media']:
			log.error('Media not detected in port %s' % port['portnum'])
			founderror = True
	if founderror is False:
		log.info('Nothing found.  Rebooting.')
	DUT.reset()
	log.info('Reboot command issued.  Waiting for DUT to boot.')
	time.sleep(180)
	log.info('Done waiting for DUT.')




