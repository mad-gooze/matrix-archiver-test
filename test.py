#!/usr/bin/python

import os
import sys
import filecmp
import subprocess
import threading


TMP_FILE = "tmp.txt"
TMP_FILE_ARC = "tmp_arc.txt"
TIMEOUT=20
FNULL = open(os.devnull, 'w')

print "Matrix archiever test script for AESC Summer School Contest"

class Command(object):
	def __init__(self, cmd):
		self.cmd = cmd
		self.process = None

	def run(self, timeout):
		def target():
			self.process = subprocess.Popen(self.cmd, shell=True, stdout = FNULL, stderr = FNULL)
			self.process.communicate()

		thread = threading.Thread(target=target)
		thread.start()

		thread.join(timeout)
		if thread.is_alive():
			self.process.terminate()
			print "timeout exceeded,",
			thread.join()

test_size = 0
arc_size = 0
test_num = 0;
passed_tests = 0;

if len(sys.argv) < 3:
    sys.exit('Usage: %s pack.exe unpack.exe' % sys.argv[0])

pack = sys.argv[1]
unpack = sys.argv[2]

for file in os.listdir("tests"):
	test_num += 1
	testfile = os.path.join("tests", file)
	print "Testing file " + testfile + ".....",
	command = Command(pack + " " + testfile + " " + TMP_FILE_ARC)
	command.run(timeout = TIMEOUT)
	command = Command(unpack + " " + TMP_FILE_ARC + " " + TMP_FILE)
	command.run(timeout = TIMEOUT)
	if not filecmp.cmp(testfile, TMP_FILE):
		print "failed"
	else:
		print "success, ",
		orginal_size = os.stat(testfile).st_size
 		archieved_size = os.stat(TMP_FILE_ARC).st_size
		compression = float(archieved_size) / float(orginal_size) * 100
		print "compression: " + str(round(compression, 3)) + "%"
		test_size += orginal_size
		arc_size += archieved_size
		passed_tests += 1
	os.remove(TMP_FILE)
	os.remove(TMP_FILE_ARC)
print "============================="
print "Passed tests: " + str(passed_tests) + "/" + str(test_num);
print "Original size: ", test_size 
print "Archieved size: ", arc_size
compression = float(arc_size) / float(test_size) * 100
print "Summary compression: " + str(round(compression, 3)) + "%"
