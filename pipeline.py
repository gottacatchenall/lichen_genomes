#! /usr/bin/env python

import sys, os, subprocess

input_dir = 'mito_genes'
dir_name= 'mito_genes_only'
subprocess.call(["mkdir",  dir_name])


print("Setting up MrBayes...\n\n\n")
os.chdir("./lib/mrbayes")
#subprocess.call("./configure")
subprocess.call("make")
print os.getcwd()
subprocess.call("cp ./src/mb ../../scripts", shell=True)
os.chdir("../..")
print os.getcwd()

print("Setting up Bucky")


print("Zipping Nexus File...\n\n\ns")
subprocess.call("ls")
subprocess.call("tar czf ./" + dir_name + "/genes.tar.gz ./" + input_dir +"/*.nexus", shell=True)

print os.getcwd()
print("Running MrBayes...\n\n\n")
os.chdir("./scripts")
subprocess.call("perl mb.pl ../" + dir_name + "/genes.tar.gz -m ./mb_block.txt -o ../" + dir_name + "/mb_data", shell=True)

print("Running Bucky...\n\n\n\n")
subprocess.call("perl bucky.pl ../" + dir_name + "/mb_data/genes.mb.tar -o ../" + dir_name + "/bucky_output", shell=True)
