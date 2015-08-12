#!/usr/bin/python
"""
This program runs on build, getting the host key for the server on which it is running
then placing that key in the data directory.

"""

import os, sys, subprocess, platform, logging

#import setup logging
def logConfigure(logFileName, debugFlag=False, logPath='../log/'):
	"""
	experimental function to configure logging
	"""

	logFile = '{0}{1}'.format(logPath, logFileName)

	logger = logging.getLogger(__name__)
	logger.setLevel(logging.DEBUG)

	# create file handler which logs even debug messages
	fh = logging.FileHandler(logFile)
	fh.setLevel(logging.DEBUG)

	# create console handler with a higher log level
	ch = logging.StreamHandler()
	
	#set logging level
	if debugFlag:
		fh.setLevel(logging.DEBUG)
		ch.setLevel(logging.DEBUG)
	else:
		fh.setLevel(logging.INFO)
		ch.setLevel(logging.INFO)

	# create formatter and add it to the handlers
	formatOptions = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
	formatter = logging.Formatter(formatOptions)
	ch.setFormatter(formatter)
	fh.setFormatter(formatter)

	# add the handlers to logger
	logger.addHandler(ch)
	logger.addHandler(fh)

	return logger


def getHostKey(hostName, ipOption="-4", typeOption="rsa"):
	"""
	runs ssh-keyscan on a given host
	options are hostname, ip (either -4 or -6, defults to -4, and key type (defaults to rsa)
	"""
	
	#command
	sshkeyscan = '/usr/bin/ssh-keyscan'

	#check to ensure that command is present, raise exception if not (experimental)
	if not os.path.isfile(sshkeyscan):
		errorMessage = "{0} not present, aborting".format(sshkeyscan)
		raise Exception(errorMessage)
	
	p = subprocess.Popen([sshkeyscan, ipOption, '-t', typeOption, hostName],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	out, err = p.communicate()

	if err and ( '#' not in err):
		errorMessage =  "could not gather host key for {0} due to error:\n {1}".format(hostName, str(err))
		raise Exception(errorMessage)

	if not out:
		errorMessage = "empty host key returned for {0}".format(hostName) 
		raise Exception(errorMessage)	

	return out

def writeHostKeyFile(host, key, path):
	"""
	Writes the host key into a file named after the hostname
	"""
	
	fileName = path + host

	if os.path.isfile(fileName):
		try:
			os.remove(fileName)
			logMessage = "prior host key file for: " + host + " found, file removed."
			logger.info(logMessage)
		except:
			raise 

	try:
		f = file(fileName, "w")
	except:
		raise

	try:
		f.write(key)
	except:
		raise

	logMessage = "host key file {0} written".format(fileName)
	logger.info(logMessage)

	try:
		f.close()
	except:
		raise
		
	return True

if __name__ == "__main__":
	"""
	if run as a standalone it gets the host key for the server it is run on
	"""

	logFileName = "get_host_keys.log"
	logger = logConfigure(logFileName)
	
	#gets hostname
	hostName = platform.node()

	try:
		key = getHostKey(hostName)
	except Exception as Exc:
		logMessage = "excption raised from getHostKey: {0}".format(Exc)
		logger.error(logMessage)
		sys.exit(1)
		
	try:
		writeHostKeyFile(hostName, key, dat_dir)
	except IOError as e:
		logMessage = "I/O Error({0}) writting host key file: {1}".format(e.errno, e.strerror)
		logger.error(logMessage)
		sys.exit(1)
	except:
		logMessage = "unexpected error encoutered writting host key file: {0}".format(sys.exc_info()[0])
		logger.error(logMessage)
		sys.exit(1)
	
	logMessage = "host key for {0} written to {1}".format(hostName, dat_dir)
	logger.info(logMessage)
	sys.exit(0)