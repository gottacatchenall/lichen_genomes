## load phytools
library(phytools)
tree <- read.tree(file.choose())
tree <- chronos(tree)
data <- read.table(file.choose(), header = F)

taxa <- data$V1
trait <- data$V3

names(trait) <- taxa
trait

plotTree(tree,type="fan",fsize=0.8,ftype="i")

cols<-setNames(palette()[1:length(unique(trait))],sort(unique(trait)))
tiplabels(pie=to.matrix(trait,sort(unique(trait))),piecol=cols,cex=0.3)
add.simmap.legend(colors=cols,prompt=FALSE,x=0.9*par()$usr[1],
                  y=-max(nodeHeights(tree)),fsize=0.8)

## estimate ancestral states under a ER model
fitER<-ace(trait,tree,model="ER",type="discrete")
fitER
round(fitER$lik.anc,3)


plotTree(tree,type="fan",fsize=0.8,ftype="i")
nodelabels(node=1:tree$Nnode+Ntip(tree),
           pie=fitER$lik.anc,piecol=cols,cex=0.5)
tiplabels(pie=to.matrix(trait,sort(unique(trait))),piecol=cols,cex=0.3)
add.simmap.legend(colors=cols,prompt=FALSE,x=0.9*par()$usr[1],
                  y=-max(nodeHeights(tree)),fsize=0.8)



mtree<-make.simmap(tree,trait,model="ER")
mtree

plot(mtree,cols,type="fan",fsize=0.8,ftype="i")
add.simmap.legend(colors=cols,prompt=FALSE,x=0.9*par()$usr[1],
                  y=-max(nodeHeights(tree)),fsize=0.8)

mtrees<-make.simmap(tree,trait,model="ER",nsim=100)
mtrees
par(mfrow=c(10,10))
null<-sapply(mtrees,plot,colors=cols,lwd=1,ftype="off")

pd<-summary(mtrees,plot=FALSE)
pd

plot(pd,fsize=0.6,ftype="i")

plot(mtrees[[1]],cols,type="fan",fsize=0.8,ftype="i")
nodelabels(pie=pd$ace,piecol=cols,cex=0.5)
add.simmap.legend(colors=cols,prompt=FALSE,x=0.9*par()$usr[1],
                  y=-max(nodeHeights(tree)),fsize=0.8)

plot(fitER$lik.anc,pd$ace,xlab="marginal ancestral states",
     ylab="posterior probabilities from stochastic mapping")
lines(c(0,1),c(0,1),lty="dashed",col="red",lwd=2)
