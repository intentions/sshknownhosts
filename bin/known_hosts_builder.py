#!/usr/bin/python
"""
This script reads down the hosts files for hostnames matching a given pattern,
it then generates a file containing the host keys for those servers
"""

import sys, os, logging, json

# sets up pathing for lib and log
log_dir = "../log/"
dat_dir = "../data/"
logFile = "buildsshknownhosts.log"

def readJsonConf(jsonFile):
	"""
	reads in the json formatted configuraiton file, and returns that data for parsing
	:param jsonFile:
	"""
	message = "reading {0}".format(jsonFile)
	logger.info(message)

	try:
		with open(jsonFile) as json_data_file:
			configData = json.load(json_data_file)
	except IOError as e:
		message = "I/O Error {0}: {1}".format(jsonFile, e.strerror)
		logger.error(message)
		raise
	except ValueError as e:
		message = "Value Error reading {0}: {1}".format(jsonFile, str(e))
		logger.error(message)
		raise
	except:
		err = sys.exc_info()[0]
		message = "error extracting config data from {0}: {1}".format(jsonFile.err)
		raise

	message = "finished reading configuration file: {0}".format(jsonFile)
	logger.debug(message)

	return configData

def parseConfData(configData):
	"""
	parses the JSON formatted data
	:param configData:
	"""

	message = "parsing configuration data"
	logger.debug(message)



def logConfigure(logFileName=os.path.basename(__file__), debugFlag=False, logPath='../log/'):
	"""
	experimental function to configure logging
	"""

	logFile = '{0}{1}'.format(logPath, logFileName)

	logger = logging.getLogger(logFileName)
	logger.setLevel(logging.DEBUG)

	# create file handler which logs even debug messages
	fh = logging.FileHandler(logFile)
	fh.setLevel(logging.DEBUG)

	# create console handler with a higher log level
	ch = logging.StreamHandler()

	# set logging level
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


# define host matchs
cannonicalPatterns = ["qcd", "farm", "winter"]


def checkNew(cannonicalPatterns, knownHosts):
	"""
	checks to see if any of the files in data with a name with
	a match in cannonicalPatterns (a string), are younger than
	ssh_known_hosts.  If it is then it returns True and a list 
	in dat_dir, else False and an empty list
	"""
	workList = []
	fileList = next(os.walk(dat_dir))[2]

	for f in fileList:
		for p in cannonicalPatterns:
			if p in f:
				workList.append(f)

	if len(workList) == 0:
		logMessage = "no files in {0} found matching {1}".format(dat_dir,str(cannonicalPatterns))
		logger.error(logMessage)
		return (False, [])

	if not os.path.isfile(sshKnownHosts):
		logMessage = "no ssh_known_hosts file found in {0} new file will be generated.".format(dat_dir)
		logger.info(logMessage)
		return (True, workList)

	for w in workList:
		if os.path.getmtime(knownHosts) < os.path.getmtime(dat_dir + w):
			logMessage = "new keys found"
			logger.info(logMessage)
			return (True, workList)

	return (False, [])


def buildKnownHosts(fileList, knownHostsFile=""):
	"""
	Builds a ssh_known_hosts from the contents of a given file
	if no output file is passed then it returns a string, else
	it writes the list of host keys to the given file.
	"""
	keyList = []

	for f in fileList:
		f = "{0}{1}".format(dat_dir, f)
		try:
			with open(f) as keyfile:
				key = keyfile.read()
		except IOError as err:
			logMessage = "I/O error ({0}) reading {1}: {2}".format(err.errno, str(f), err.strerror)
			logger.error(logMessage)
			continue
		keyList.append(key)

	keys = '\n'.join(keyList)

	# if no ssh_known_hosts file is given then return return keys as a string
	if knownHostsFile == "":
		return keys

	sshKnownHosts = file(knownHostsFile, 'w')

	sshKnownHosts.write(keys)

	sshKnownHosts.close

	return knownHostsFile


if __name__ == "__main__":
	"""
	where the work is done
	"""

	logger = logConfigure()

	sshKnownHosts = "{0}ssh_known_hosts".format(dat_dir)

	try:
		keyList = checkNew(cannonicalPatterns, sshKnownHosts)
	except:
		err = sys.exc_info()[0]
		logMessage = "error encountered checking for new host keys: {0}".format(str(err))

	try:
		buildKnownHosts(keyList, sshKnownHosts)
	except:
		err = sys.exc_info()[0]
		logMessage = "error encountered creating known host file: {0}".format(str(err))
		sys.exit(1)

	logMessage = "ssh_known_hosts file updated"
	logger.info(logMessage)
	sys.exit(0)
