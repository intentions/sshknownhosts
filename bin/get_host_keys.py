#!/usr/bin/python
"""
This program runs on build, getting the host key for the server on which it is running
then placing that key in the data directory.

"""

import os, sys, subprocess, platform, logging

#sets lib and log paths
#ain_dir = "/home/strosahl/Testbed/python/host_key_harvester/"
myName = os.path.basename(__file__)
myPath = os.path.realpath(__file__)
bin_trm = "bin/" + str(myName)
root_dir = str(myPath).replace(bin_trm, "")
dat_dir = root_dir + "data/"

#puts library dir into the python path
sys.path.append(lib_dir)

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
		logMessage = "{0} not present, aborting".format(sshkeyscan)
		logger.error(logMessage)
		raise Exception(logMessage)
	
	p = subprocess.Popen([sshkeyscan, ipOption, '-t', typeOption, hostName],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	out, err = p.communicate()

	if err and ( '#' not in err):
		logMessage =  "could not gather host key for {0} due to error:\n {1}".format(hostName, str(err))
		logger.error(logMessage)
		raise Exception("error", err)

	if not out:
		logMessage = "empty host key returned for {0}".format(hostName) 
		logger.error(logMessage)
		return ("error", logMessage)	

	return (out, "")

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
		except OSError as err:
			logMessage = "could not remove pre-existing host key file for {0} due to error({1}: {2}".format(fileName, err.errno, err.strerror)
			logger.error(logMessage)
			return False

	try:
		f = file(fileName, "w")
	except IOError as err:
		logMessage = "could not open {0} for writting due to error({1}): {2}".format(fileName, err.errno, err.strerror)
		logger.error(logMessage)
		return False

	try:
		f.write(key)
	except IOError as err:
		logMessage = "could not write to {0} due to error({1}: {2}".format(fileName, err.errno, e.strerror)
		logger.error(logMessage)
		return False

	logMessage = "host key file {0} written".format(fileName)
	logger.info(logMessage)

	f.close()
	return True


if __name__ == "__main__":
	"""
	if run as a standalone it gets the host key for the server it is run on
	"""

	logFileName = "get_host_keys.log"
	logger = logConfigure(logFileName)
	
	#gets hostname
	hostName = platform.node()

	key, err = getHostKey(hostName)

	if err:
		logMessage = "encountered error getting key for {0}, exiting.".format(hostName)
		logger.error(logMessage)
		sys.exit()
	
	writeHostKeyFile(hostName, key, dat_dir)
	logMessage = "host key for {0} written to {1}".format(hostName, dat_dir)
	logger.info(logMessage)	