#!/usr/bin/python
"""
This module reads a given host file and rips out entries that match a given pattern
"""

import os, sys

def hostRip(pattern,dotExtent="",hostFile="/etc/hosts"):
	"""
	this function searches a given file for a string that starts with a given pattern
	and returns a list of those entries
	that matches that pattern.  For example:
	a search for HOSTNAME in a hosts file mapped as follows...
	111.11.111.11 HOSTNAME1 HOSTNAME1.something.com
	returns:
	HOSTNAME1
	"""

	hostList = []

	#checks to see if given hostFile exists
	if os.path.isfile(hostFile):
		try:
			h = open(hostFile, 'r')
		except OSError:
			errorMessage =  "error reading " + hostFile + ": " + str(OSError)
			sys.stderr.write(errorMessage)
			return False

	for line in h:
		if pattern in line:
			entries = line.split()
			for e in entries:
				if e.startswith(pattern):
					hostList.insert(e)
	h.close

	if len(hostList) == 0:
		errorMessage = "warning, no matches for " + pattern + " found in " + hostFile
		sys.stderr.write(errorMessage
		return False
			

