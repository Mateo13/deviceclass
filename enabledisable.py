import time

from device import Device


TOR = Device('EOS', '10.52.2.222', 10031)
print(TOR.login())
print(TOR.write('set force enable'))


while True:
	print(TOR.write('set port disable ge.1.48'))
	time.sleep(5)
	print(TOR.write('set port enable ge.1.48'))
	time.sleep(5)


