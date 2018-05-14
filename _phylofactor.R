Data <- read.csv('')
tree <- read.tree('')
MetaData <- read.csv('')
taxonomy <- read.csv('')
formula <- read.csv('')
response.variable.class <- read.csv('')
formula <- as.formula(formula)
nfactors <- read.csv('')
ncores <- read.csv('')

pf <- PhyloFactor(Data,tree,MetaData,formula,choice='F',nfactors=nfactors,ncores=ncores)
  
'yo'