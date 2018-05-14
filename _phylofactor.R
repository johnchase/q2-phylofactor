Data <- read.csv('')
tree <- read.tree('')
MetaData <- read.csv('')
taxonomy <- read.csv('')

formula <- as.formula(formula)

# LHS <- as.character(formula[[2]]) ## will need to check LHS and family.

pf <- PhyloFactor(Data,tree,MetaData,formula,choice='F',nfactors=nfactors,ncores=ncores)
  
## semantic type 1 - artifact (table)
write.csv(pf$factors,sep='\t',row.names = TRUE,col.names = TRUE)


tr <- pf.tree(pf,factors=factors)
##semantic type 2 - visualization
tr$ggplot
