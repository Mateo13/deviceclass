'''Base test class that all other tests inherit from.  All test subclasses must override the 
checkResult() and execute() methods.  These will be the only methods called externally from each 
test.'''

#Imports
import time

#Define generic Test class.
class Test(object):
	#Initialize class.
	def __init__(self, name, f):
		self.name = name
		self.log = f

	#Log output.
	def logOutput(self, output, printCLI=True):
		if isinstance(output, list):
			for t in output:
				t = time.strftime('%c') + '   ' + t
				if printCLI:
					print(t)
				t = t + '\r\n'
				self.log.write(t.encode('ascii'))
		else:
			output = time.strftime('%c') + '   ' + output
			if printCLI:
				print(output)
			output = output + '\r\n'
			self.log.write(output.encode('ascii'))

	#Print begin test banner.
	def printBeginBanner(self):
		self.logOutput("===========================================================")
		self.logOutput("Beginning " + self.name)
		self.logOutput("===========================================================")

	#Print begin iteration banner.
	def printBeginIterBanner(self, iter):
		self.logOutput("========================================")
		self.logOutput("Beginning iteration " + str(iter))
		self.logOutput("========================================")

	#Print results banner.
	def printResultBanner(self, text, res):
		self.logOutput("///////////////////////////////////////////////////////////")
		self.logOutput(text)
		if res:
			self.logOutput("Test Result: PASS")
		else:
			self.logOutput("Test Result: FAIL")
		self.logOutput("///////////////////////////////////////////////////////////")

	#Check the result of the test after execution
	def checkResult(self):
		self.logOutput("WARNING: Function checkResult(self) is not implemented!")
	
	#Execute the test.
	def execute(self):
		self.logOutput("WARNING: Function execute(self) is not implemented!")
	
	#String description of the Test.
	def __str__(self):
		return self.name