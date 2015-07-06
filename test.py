'''Base test class that all other tests inherit from.  All test subclasses must override the checkResult()
and execute() methods.  These will be the only methods called externally from each test.'''

#Define generic Test class.
class Test(object):
	#Initialize class.
	def __init__(self, name):
		self.name = name
	
	#Check the result of the test after execution
	def checkResult(self):
		return
	
	#Execute the test.
	def execute(self):
		return
	
	#String description of the Test.
	def __str__(self):
		return self.name