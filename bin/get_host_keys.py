#!/usr/bin/python
"""
This program runs on build, getting the host key for the server on which it is running
then placing that key in the data directory.
"""

import os, sys, subprocess, platform

#sets lib and log paths
log_dir = "../log/"
lib_dir = "../lib/"
dat_dir = "../data/"
logFile = log_dir + "gethostkey.log"

#puts library dir into the python path
sys.path.append(lib_dir)

#import custom moduels
import logWrite from logger


def getHostKey(host, ipOption="-4", typeOption="rsa"):
	"""
	runs ssh-keyscan on a given host
	"""
	
	#command
	ssh-keyscan = "/usr/bin/ssh-keyscan"

	p = subprocess.Popen([ssh-keyscan, ipOption, '-t', typeOption, host],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	out, err = p.communicate()

	if err:
		logMessage =  "could not gather host key for " + host + " error follows \n    " + str(err)
		logWrite(logFile, logMessage, "ERROR")
		return ("error", err)

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
			logWrite(logFile, logMessage, "INFO")
		except OSError:
			logMessage = "warning - could not remove pre-existing host key for " + host + " - process aborted"
			logWrite(logFile, logMessage, "ERROR")
			return False

	try:
		f = file(fileName, "w")
	except: IOError:
		logMessage = "could not open " + fileName + " for writting due to error:  \n    " + str(IOError)
		return false

	try:
		f.write(key)
	except IOError:
		logMessage = "could not write to " + fileName + " due to error:   \n   " +


if __name__ = "__main__":
	"""
	if run as a standalone it gets the host key for the server it is run on
	"""

	#gets hostname
	hostName = platform.node()

	key, err = getHostKey(hostName)

	if not err:
		writeHostKeyFile(hostName, key, dat_dir)

	else:
		sys.stderr.write(str(err))
