#! /usr/bin/env python

import sys, os, subprocess

subprocess.call(["mkdir", "tmp"])


print("Setting up MrBayes...\n\n\n")
os.chdir("./lib/mrbayes")
#subprocess.call("./configure")
subprocess.call("make")
print os.getcwd()
subprocess.call("cp ./src/mb ../../scripts", shell=True)
os.chdir("../..")
print os.getcwd()


print("Zipping Nexus File...\n\n\ns")
subprocess.call("ls")
subprocess.call("tar czf ./tmp/genes.tar.gz ./nexus/*.nexus", shell=True)

print os.getcwd()
print("Running MrBayes...\n\n\n")
os.chdir("./scripts")
subprocess.call("perl mb.pl ../tmp/genes.tar.gz -m ./mb_block.txt -o ../tmp/mb_data", shell=True)
