library(phytools)
library(ape)
library(phangorn)  
library(magrittr)  

mrbayes.tree <- read.nexus("./old_mb_analysis/genes/all/all.nexus.con.tre")
Nnet <- read.nexus.networx("splitstree.fasta.nex")

par(mfrow=c(1,2), mar=c(1,1,1,1))
plot(mrbayes.tree)
nodelabels(mrbayes.tree$node.label, adj = c(1, 0), frame = "none")

plot(Nnet,"2D")
