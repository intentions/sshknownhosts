#!/usr/bin/python

"""
log writting module, run as standalone to test
"""

import os, datetime, sys

def logWrite(logFile, message, head=''):
	"""
	logWrite writes a given message to a logfile, led by a timestamp.
	A header for the line can be added (like INFO or ERROR).
	If the given filename does not exist then it will create the file,
	if it does exist then it appends the file
	"""

        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if os.path.isfile(logFile):
		try:
	                log = file(logFile, "a")
		except IOError:
			print "cannot open " + logFile + " for appending!"
			return False
        else:
		try:
	                log = file(logFile, "w")
		except IOError:
			print "cannot open " + logFile + " for writting!"
			return False

        logMessage = head + ' ' + timestamp + ' ' + message + '\n' 

	try:
	        log.write(logMessage)

	except IOError:
		print "error when writting to log " + logFile
		return False

        log.close

	#log write successful
        return True

def testLogWrite():
	"""
	Runs a test of the logwrite function
	First it tests creating and writting the logfile
	Then it tests appending the logfile.
	Logs are written into the same directory as logger.py
	"""

	logfile = 'testwrite.log'

	print "tesing logger modules\n"

	#checks to see if there are any lingering testlogs and removes them
	if os.path.isfile(logfile): 
		try:
			print "old test log found, trying to remove"
			os.remove(logfile)
		except OSError:
			assert False
			return False

	#tests creation and initial write of the logfile
	print "testing write of a logfile (will overwrite existing test logwrite)..."
	retur = logWrite(logfile, "this is a test write")
	print "return from test write: " + str(retur)
	if not retur:
		print "write failed, exiting test"
		assert False
		return False		

	#verifies that the file can be appended
	print "testing log file append (appends to prior created log file)..."
	retur = logWrite(logfile, "this is a test append")
	print "return from test append: " + str(retur)
	if not retur:
		print "append failed, exiting test"
		assert False
		return False		

	#verifies that the file was created
	print "\nVerifying creation files..."
	if os.path.isfile(logfile):
		print "log file found: " + logfile
	else:
		print "log file not found: " + logfile
		assert False
		return False		

	#for visual inspection
	print "\nVerifying file contents..."
	print "expected contents:"
	print "<timestamp> this is a test write"
	print "<timestamp> this is a test append"

	#print contents of temp logfile and calculate number of lines
	f = open(logfile, 'r')
	count = 0
	for line in f:
		print line
		count = count + 1
	f.close

	#check to ensure that only two lines were writting to the log
	if count != 2:
		assert False
		return False

	#remove temporary log file
	try:
		os.remove(logfile)
	except OSError:
                print "OSError found: " + str(OSError)
		assert False
		return False

	assert True
	return True	

if __name__ == "__main__":
	"""
	If run as a standalone it runs the logwrite test
	"""
	testLogWrite()
