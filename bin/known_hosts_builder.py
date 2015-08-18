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

def readJsonConf(jsonFile, debugFlag=False):
	"""
	reads in the json formatted configuraiton file, and returns that data for parsing
	:param jsonFile:
	"""
	message = "reading {0}".format(jsonFile)
	print message

	print str(debugFlag)
	
	if not os.path.isfile(jsonFile):
		message = "Error, config file {0} does not exist.".format(jsonFile)
		print message
	try:
		with open(jsonFile) as json_data_file:
			configData = json.load(json_data_file)
			if debugFlag: print "config dump:\n {0}".format(str(configData))
	except IOError as e:
		print "IOError ({0}) reading {1}:\n {2}".format(e.errno, jsonFile, e.strerror)
		raise
	except:
		print "unexpected error encoutered reading configuration file: {0}".format(sys.exc_info()[0])
		raise
	
	if debugFlag: print "finished reading configuration file: {0}".format(jsonFile)
	return configData

def parseConfData(configData, debugFlag=False):
	"""
	parses the JSON formatted data
	:param configData:
	"""
	
	if debugFlag: print "parsing configuration data"

	configuration = {
		"debug_flag": False,
		"cannonical_patterns": [],
		"path_to_key_file": "",
		"log_path": "",
		"log_file": ""
	}

	if debugFlag: print "default config dictionary:\n {0}".format(str(configuration))

	for confKey in configData.keys():
		if debugFlag: print "processing {0}".format(str(confKey))
		configuration["debug_flag"] = bool(configData[confKey]["debug_flag"])
		if debugFlag: print "debug flag set"
		for p in configData[confKey]["cannonical_patterns"]:
			if debugFlag: "adding {0} to cannonical patters".format(p)
			configuration["cannonical_patterns"].append(p)
		if debugFlag: print "key file path: {0}".format(configData[confKey]["path_to_key_file"])
		configuration["path_to_key_file"] = configData[confKey]["path_to_key_file"]
		if debugFlag: print "log path: {0}".format(configData[confKey]['log_path'])
		configuration["log_path"] = configData[confKey]['log_path']
		if debugFlag: print "log file: {0}".format(configData[confKey]["log_file"])
		configuration["log_file"] = configData[confKey]["log_file"]

	return configuration

def logConfigure(LogFileName, LogPath, debugFlag):
	"""
	configure logging
	"""
	if debugFlag: print "entering log configuraiton"

	logFile = '{0}{1}'.format(LogPath, LogFileName)
	if debugFlag: print "log file: {0}".format(logFile)

	logger = logging.getLogger(LogFileName)
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

	message = "debugging enabled"
	logger.debug(message)
	return logger


# define host matchs
cannonicalPatterns = ["qcd", "farm", "winter", "box"]


def checkNew(cannonicalPatterns, knownHosts):
	"""
	checks to see if any of the files in data with a name with
	a match in cannonicalPatterns (a string), are younger than
	ssh_known_hosts.  If it is then it returns True and a list 
	in dat_dir, else False and an empty list
	"""
	message = "checking for new ssh key files"
	logger.debug(message)
	
	workList = []
	fileList = next(os.walk(dat_dir))[2]

	for f in fileList:
		message = "found file {0}".format(f)
		logger.debug(message)
		for p in cannonicalPatterns:
			if p in f:
				message = "found that {0} matched {1}".format(f, p)
				logger.debug(message)
				workList.append(f)

	if len(workList) == 0:
		message = "no files in {0} found matching {1}".format(dat_dir,str(cannonicalPatterns))
		logger.error(message)
		raise ValueError(message)

	if not os.path.isfile(knownHosts):
		logMessage = "no ssh_known_hosts file found in {0} new file will be generated.".format(dat_dir)
		logger.info(logMessage)
		return workList

	for w in workList:
		if os.path.getmtime(knownHosts) < os.path.getmtime(dat_dir + w):
			logMessage = "new keys found"
			logger.info(logMessage)
			return workList

	message = "all ssh key files older then the known host file"
	logger.info(message)
	return True


def buildKnownHosts(fileList, knownHostsFile=""):
	"""
	Builds a ssh_known_hosts from the contents of a given file
	if no output file is passed then it returns a string, else
	it writes the list of host keys to the given file.
	"""
	message = "starting to build known hosts file"
	logger.debug(message)
	
	keyList = []

	for f in fileList:
		f = "{0}{1}".format(dat_dir, f)
		message = "checking {0}".format(f)
		logger.debug(message)
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

	debugFlag = True
	
	configuration_file = "known_hosts_builder.json"
	
	try:
		if debugFlag: print "reading configuration file {0}".format(configuration_file)
		rawConfig = readJsonConf(configuration_file, debugFlag)
	except:
		print "exiting"
		sys.exit(1)
	
	try:
		if debugFlag: print "processing configuration data"
		configuration = parseConfData(rawConfig, debugFlag)
	except:
		print "error, exiting:\n {0}".format(sys.exc_info()[0])
		sys.exit(1)
	
	if debugFlag: "configuring logging"

	print "log file: {0}".format(configuration['log_file'])


	logger = logConfigure(configuration['log_file'], configuration['log_path'], configuration['debug_flag'])

	sshKnownHosts = "{0}ssh_known_hosts".format(dat_dir)
	message = "known hosts file will be written to {0}".format(dat_dir)
	logger.debug(message)
	
	try:
		keyList = checkNew(cannonicalPatterns, sshKnownHosts)
	except:
		err = sys.exc_info()[0]
		message = "error encountered checking for new host keys: {0}".format(str(err))
		logger.error(message)
		sys.exit(1)

	try:
		buildKnownHosts(keyList, sshKnownHosts)
	except:
		err = sys.exc_info()[0]
		message = "error encountered creating known host file: {0}".format(str(err))
		logger.error(message)
		sys.exit(1)

	logMessage = "ssh_known_hosts file updated"
	logger.info(logMessage)
	sys.exit(0)

