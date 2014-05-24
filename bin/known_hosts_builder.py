#!/usr/bin/python
"""
This script reads down the hosts files for hostnames matching a given pattern,
it then generates a file containing the host keys for those servers
"""
import sys,os,subprocess

#sets up pathing for lib and log
myName = os.path.basename(__file__)
myPath = os.path.realpath(__file__)
bin_trm = "bin/" + str(myName)
root_dir = str(myPath).replace(bin_trm, "")
log_dir = root_dir + "log/"
lib_dir = root_dir + "lib/"
dat_dir = root_dir + "data/"
logFile = log_dir + "buildsshknownhosts.log"

#sets the library path
sys.path.append(lib_dir)

#import logWrite custom module
from logger import logWrite

def checkNew(cannonicalPatterns,knownHosts="ssh_known_hosts"):
	"""
	checks to see if any of the files in data with a name with
	a match in cannonicalPatterns (a string), are younger than
	ssh_known_hosts.  If it is then it returns True and a list 
	in dat_dir, else False and an empty list
	"""

	workList = []
	fileList = next(os.walk(dat_dir))[2]

	for f in fileList:
		if f in cannonicalPatterns:
			workList.append(f)

	if len(workList):
		logMessage = "no files in " + dat_dir + " found matching " + cannonicalPatterns 
		logWriter(logFile,logMessage,"ERROR")
		return False 

	for w in workList:
		if os.path.getmtime(dat_dir + knownHosts) < os.path.getmtime(dat_dir + w):
			logMessage = "new keys found"
			logWritter(logFIle,logMessage,"INFO")
			return (True, workList)

	return (False, [])

def buildKnownHosts(fileList,knownHostsFile=""):
	"""
	Builds a ssh_known_hosts from the contents of a given file
	if no output file is passed then it returns a string, else
	it writes the list of host keys to the given file.
	"""
	keyList = []

	for f in fileList:
		k = open(f, 'r')
		for l in k:
			keyList.append(l)
		k.close

	keys = '\n'.join(keyList)

	if knownHostsFile == "":
		return (True, keys)
	
	sshKnownHosts = file(knownHostsFile, 'w')

	sshKnownHosts.write(keys)

	sshKnownHosts.close

	return (True, knownHostsFile)
	

if  __name__ == "__main__":
	"""
	where the work is done
	"""


