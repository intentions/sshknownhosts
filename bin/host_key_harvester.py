#!/usr/bin/python
"""
This script reads down the hosts files for hostnames matching a given pattern,
it then generates a file containing the host keys for those servers
"""
import sys,os,subprocess

log_dir = "../log"
lib_dir = "../lib"

sys.path.append(lib_dir)


