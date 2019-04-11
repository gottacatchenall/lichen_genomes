#! /usr/bin/env python

import sys, os, subprocess, glob
from multiprocessing import Process


input_dir = 'mito_genes'
dir_name= 'output_mito_genes'
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
    print("Zipping Nexus File...\n\n\ns")
    subprocess.call("ls")
    subprocess.call("tar czf ./" + dir_name + "/genes.tar.gz ./" + input_dir +"/*.nexus", shell=True)

def run_cmd():
    pass

def mrbayes():
    print("Running MrBayes...\n\n\n")
    os.chdir(home)
    os.chdir("./scripts")

    mb_exe = os.path.abspath("./mb")

    # append mb block to bottom of each nexus and run on each nexus
    mbblock = '''
    begin mrbayes;
    	set nowarnings=yes;
    	set autoclose=yes;
    	lset nst=6 rates=gamma;
    	mcmcp ngen=20000 burninfrac=.25 samplefreq=100 printfreq=1000 diagnfreq=1000 nruns=3 nchains=3 temp=0.40 swapfreq=10;
    	mcmc;
    end;
    '''

    os.chdir(home)
    os.chdir(input_dir)
    for file in glob.glob("*.nexus"):

        with open(file, 'a') as f:
            f.write(mbblock)


        cmd = mb_exe + " -i " + file
        p = Process(target=exec, args=cmd)
        p.start()
        p.join()


    # TODO do MB properly
    #subprocess.call("perl mb.pl ../" + dir_name + "/genes.tar.gz -m ./mb_block.txt -o ../" + dir_name + "/mb_data", shell=True)

def mv_mb_output():
    os.chdir("./scripts")
    ## Run mbsum and Bucky
    print("Running mbsum...\n\n\n")
    os.chdir("../" + dir_name + "/mb_data")

    subprocess.call("tar -xvf", shell=True)
    subprocess.call("gunzip ./" + input_dir + "/*.tar.gz", shell=True)

    os.chdir(input_dir)

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
    subprocess.call(bucky_cmd, shell=True)
    return gene_list

def convert_ckp_to_nex():
    os.chdir(home)
    os.chdir(dir_name + "/mb/mb_output/")
    pass

#setup()
mrbayes()
#gene_list = bucky()

# mbsum -n 5000 -o mygene mygene.run?.t
