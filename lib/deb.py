#!/usr/bin/python

"""
Debug modules for use with python
"""

import os, datetime, inspect

def dprint(flag, message, ts=False):
	"""
	This function prints out the debug message if the debug flag has been set to true.
	pass true to ts to enable timestamps
	"""

	if not flag:
		return False

	if ts:
		#set timestamp
		timestamp = ' ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ': '

	else:
		timestamp = ": "

	#logic go get name of calling module
	frm = inspect.stack()[1]
	mod = inspect.getmodule(frm[0])

	print mod.__name__ + timestamp + message

	return True

def testDPrint():
	"""
	Testing function for debug modules
	"""

	print "testing deb modules:\n\n"

	print "testing dprint (printing debug messages):\n"

	msg = "test debug message"

	print "testing with debug flag set to false:"
	flag = False
	retur = dprint(flag,msg)
	print "return from dprint: " + str(retur)
	print "\n"

	print "testing with debug flag set to true:"
	flag = True
	retur = dprint(flag,msg)
	if not retur:
		assert False
		return False
	print "return from dprint: " + str(retur)
	print "\n"

	print "test timestamp toggling"
	print "testing with timestap flag set to true"
	retur = dprint(flag,msg,True)
	if not retur:
		assert False
		return False
	print "return from dprint: " + str(retur) + "\n"
	return True


#run as standalone to run tests of modules
if __name__ == "__main__":
	"""
	for standalone run of debug modules, contains call to test funciton
	"""

	testDPrint()
