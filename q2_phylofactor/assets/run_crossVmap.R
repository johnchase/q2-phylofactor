#!/usr/bin/env Rscript

library(phylofactor)

# The following line ensures that distuils does not try to compile this as
# python. It can likly be removed once script is completed
.this <- "this"

### This code assumes the newData are ready to project onto
### the contrast basis vectors (i.e. for ILR, the newData are log-relative-abundances)

#### Functions we'll need #############
groups.to.df <- function(g){
  DF <- NULL
  for (i in 1:length(g)){
    DF <- rbind(DF,data.frame('factor'=rep(i,length(unlist(g[[i]]))),
                              'group'=c(rep(1,length(g[[i]][[1]])),rep(2,length(g[[i]][[2]]))),
                              'index'=unlist(g[[i]]),
                              stringsAsFactors = F))
  }
  return(DF)
}
df.to.groups <- function(DF){
  nfactors <- max(DF$factor)
  L <- vector(mode='list',length=nfactors)
  names(L) <- paste('factor',1:nfactors)
  for (i in 1:nfactors){
    L[[i]] <- list('Group1'=DF$featureid[DF$group==1 & DF$factor==i],
                   'Group2'=DF$featureid[DF$group==2 & DF$factor==i])
  }
  return(L)
}
########################################

args <- commandArgs(TRUE)
old.tree.path <- args[[1]]
old.groups.path <- args[[2]]
newData.path <- args[[3]]
bigtree.path <- args[[4]]
out.table.path <- args[[5]]
out.group.path <- args[[6]]


tr <- read.tree(
  file = old.tree.path
)

old.groups <- read.csv(
  file=old.groups.path,
  sep='\t',
  header=T,
  stringsAsFactors = F
)

table <- read.csv(
  file = newData.path,
  check.names = FALSE,
  header = TRUE,
  comment.char = "",
  sep = "\t",
  skip = 1,
)

new.community <- as.character(table$'#OTU ID')

bigtree <- read.tree(bigtree.path)


### convert data frame to groups
Grps <- df.to.groups(old.groups)

## convert species-index groups to tree-tiplabel index groups
Grps <- lapply(Grps,FUN=function(g,tr) lapply(g,FUN=function(g,tr) match(g,tr$tip.label),tr=tr),tr=tr)


obj <- NULL
obj$tree <- tr

obj$groups <- Grps
obj$nfactors <- length(Grps)

cv.groups <- pf.crossValidateMap(pf=obj,universal.tree = bigtree
                                 ,new.community = new.community,
                                 fill.empty = F)

cv.DF <- groups.to.df(cv.groups)

### make table
cv.grps <- lapply(cv.groups,FUN=function(g,nm) lapply(g,FUN=function(g,nm) match(g,nm),nm),nm=new.community)

### make ILR projections
n=length(new.community)
V <- t(sapply(cv.grps,ilrvec,n))
print(V)
Y <- as.matrix(V) %*% table

## output cross-validated groups ##
write.table(x=cv.DF,file=out.group.path,
            sep='\t',
            row.names = F,
            col.names = T)
###################################

## output new table ##
write.table(Y,
            file = out.table.path,
            sep = "\t",
            row.names = FALSE,
            col.names = TRUE,
            quote = FALSE)
