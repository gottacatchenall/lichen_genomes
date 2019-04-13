#! /usr/bin/env python

import sys, os, subprocess, glob
from multiprocessing import Process, Pool


input_dir = 'rDNA'
dir_name= 'output_rDNA'
subprocess.call(["mkdir",  dir_name])

home = os.getcwd()

def pwd():
    print os.getcwd()
    subprocess.call("ls", shell=True)

def setup():
    os.chdir(home)
    print("Setting up MrBayes...\n\n\n")
    os.chdir("./lib/mrbayes")
    subprocess.call("./configure")
    subprocess.call("make")
    print os.getcwd()
    subprocess.call("cp ./src/mb ../../scripts", shell=True)
    os.chdir("../..")
    print os.getcwd()

    #print("Setting up Bucky")
    #os.chdir("./lib/bucky_linux")


def zip_nex():
    print("Zipping Nexus File...\n\n\n")
    subprocess.call("ls")
    subprocess.call("tar czf ./" + dir_name + "/genes.tar.gz ./" + input_dir +"/*.nexus", shell=True)

def copy_nex():
    print("Copying Nexus File...\n\n\n")
    os.chdir(home)
    cmd = 'cp ./' + input_dir + '/*.nexus ./' + dir_name
    subprocess.call(cmd, shell=True)

def start_proc(cmd):
    subprocess.call(cmd , shell=True)


def mrbayes():
    print("Running MrBayes...\n\n\n")
    os.chdir(home)
    os.chdir("./scripts")


    mb_exe = os.path.abspath("./mb")

    # append mb block to bottom of each nexus and run on each nexus
    mbblock ='''
    begin mrbayes;
    	set autoclose=yes;
    	lset nst=6 rates=gamma;
    	mcmcp ngen=200000 burninfrac=.25 samplefreq=100 printfreq=1000 diagnfreq=1000 nruns=3 nchains=3 temp=0.40 swapfreq=10;
        constraint parmo = 45 46 47 48 25 26 27 28 29;
        constraint leca = 43 2;
        prset topologypr = constraints (parmo, leca);
    	mcmc;
        sumt;
    end;
    '''
     #constraint parmo = 45 46 47 48 25 26 27 28 29;
    # constraint leca = 43 2;
    # prset topologypr = constraints (parmo, leca);

    os.chdir(home)
    os.chdir(input_dir)

    cmds = []

    for file in glob.glob("*.nexus"):
        #cmd = mb_exe + " -i " + file
        #subprocess.call(cmd , shell=True)

        print(os.path.abspath(file))
        with open(file, 'ab') as f:
            print 'writing' + file
            f.write(mbblock)
        cmd = mb_exe + "  " + file
        cmds.append(cmd)

    p = Pool(len(cmds))
    p.map(start_proc, cmds)

   # subprocess.call("perl mb.pl ../" + dir_name + "/genes.tar.gz -m ./mb_block.txt -o ../" + dir_name + "/mb_data", shell=True)

def mv_mb_output():
    ## Run mbsum and Bucky
    print("Running mbsum...\n\n\n")
    os.chdir("../" + dir_name + "/mb_data")

    subprocess.call("tar -xvf", shell=True)
    subprocess.call("gunzip ./" + input_dir + "/*.tar.gz", shell=True)

    pwd()
    os.chdir(input_dir)
    pwd()

    for file in glob.glob("*.tar"):
        subprocess.call("tar -xvf ./" + file , shell=True)
    mv_cmd = "mv " + input_dir + " " + home + "/" + dir_name + "/mb_output"
    subprocess.call(mv_cmd , shell=True)

    os.chdir(home)

def get_gene_list():
    pass

def bucky():
    bunnin_ngen = 0
    mbsum_path = os.path.abspath("./scripts/mbsum")
    bucky_path = os.path.abspath("./scripts/bucky")
    os.chdir(dir_name + "/mb_output")
    file_list = sorted(glob.glob("*.nexus.run*.t"))
    gene_list = []
    for file in file_list:
        gene = file.split(".")[0]
        if gene not in gene_list:
            gene_list.append(gene)
    for gene in gene_list:
        this_genes_trees = sorted(glob.glob(gene + ".nexus.run*.t"))
        gene_tree_string = " ".join(this_genes_trees)
        gene_tree_string
        mb_sum_cmd = mbsum_path + " -n "+ str(bunnin_ngen) + " -o ../" + gene + ".in " + gene_tree_string
        print mb_sum_cmd
        subprocess.call(mb_sum_cmd, shell=True)
    os.chdir("..")

    bucky_cmd = bucky_path + " -n 2000000 *.in"
    print bucky_cmd
    subprocess.call(bucky_cmd, shell=True)

    return gene_list

def convert_ckp_to_nex():
    os.chdir(home)
    os.chdir(dir_name + "/mb/mb_output/")
    pass

setup()
copy_nex()
mrbayes()
mv_mb_output()
gene_list = bucky()

# run julia script

# mbsum -n 5000 -o mygene mygene.run?.t
