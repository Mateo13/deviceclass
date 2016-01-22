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


DUT = D.EXOSDevice('10.52.2.222', 10018)
time.sleep(2)

founderror = False
while(founderror == False):
	output = DUT.login()
	log.debug(output)
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
	if founderror is False:
		log.info('Nothing found.  Rebooting.')
	DUT.reset()
	log.info('Reboot command issued.  Waiting for DUT to boot.')
	time.sleep(180)
	log.info('Done waiting for DUT.')




