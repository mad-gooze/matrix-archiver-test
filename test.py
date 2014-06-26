#!/usr/bin/python
from __future__ import print_function
from __future__ import division

import os
import sys
import filecmp
import subprocess
import threading

TMP_FILE = "tmp.txt"
TMP_FILE_ARC = "tmp_arc.txt"
TIMEOUT = 10
FNULL = open(os.devnull, 'w')

print("Matrix archiver test script for AESC Summer School Contest")

class Command(object):
    def __init__(self, cmd):
        self.cmd = cmd
        self.process = None

    def run(self, timeout):
        def target():
            self.process = subprocess.Popen(self.cmd, shell=True, stdout=FNULL, stderr=FNULL)
            self.process.communicate()

        thread = threading.Thread(target=target)
        thread.start()

        thread.join(timeout)
        if thread.is_alive():
            self.process.terminate()
            thread.join()
            return False
        else:
            return True

test_size = 0
arc_size = 0
test_num = 0;
passed_tests = 0;

if len(sys.argv) < 3:
    sys.exit('Usage: {} pack.exe unpack.exe'.format(sys.argv[0]))

pack = sys.argv[1]
unpack = sys.argv[2]
show_file_names = False

if len(sys.argv) > 3:
    show_file_names = sys.argv[3] == "-s"

for file in os.listdir("tests"):
    test_num += 1
    testfile = os.path.join("tests", file)

    if show_file_names:
        print("Testing file {}...".format(testfile if show_file_names else test_num))

    archive = Command(pack + " " + testfile + " " + TMP_FILE_ARC)
    dearchive = Command(unpack + " " + TMP_FILE_ARC + " " + TMP_FILE)

    if not archive.run(timeout = TIMEOUT):
        print("[FAIL] Compression time exceeded!")
    elif not dearchive.run(timeout = TIMEOUT):
        print("[FAIL] Decompression time exceeded!")
    else:
        if not os.path.isfile(TMP_FILE_ARC):
            print("[FAIL] Archived file does not exist!")
        elif not os.path.isfile(TMP_FILE):
            print("[FAIL] Decompressed file does not exist!")
        elif not filecmp.cmp(testfile, TMP_FILE):
            print("[FAIL] Original and decompressed files do not match")
        else:
            original_size = os.stat(testfile).st_size
            archived_size = os.stat(TMP_FILE_ARC).st_size
            compression = archived_size / original_size * 100
            print("[PASS] Compression: {:.3}%".format(compression))
            test_size += orginal_size
            arc_size += archived_size
            passed_tests += 1

    if os.path.isfile(TMP_FILE_ARC):
        os.remove(TMP_FILE_ARC)
    
    if os.path.isfile(TMP_FILE):
        os.remove(TMP_FILE)
                
print("=============================")
print("Passed tests: {} / {}".format(passed_tests, test_num));
if passed_tests != 0:
    print("Original size: ", test_size) 
    print("Archived size: ", arc_size)
    compression = arc_size / test_size * 100
    print("Summary compression: {:.3}%".format(compression))
