args <- commandArgs(TRUE)

Data <- args[[1]]
tree <- args[[2]]
out.path <- args[[3]]
metadata <- args[[4]]
taxonomy <- args[[5]]
formula <- as.formula(args[[6]])
choice <- args[[7]]
nfactors <- as.integer(args[[8]])
ncores <- as.integer(args[[9]])


# Data <- read.csv('')
# tree <- read.tree('')
# MetaData <- read.csv('')
# taxonomy <- read.csv('')
#
# formula <- as.formula(formula)
#
# # LHS <- as.character(formula[[2]]) ## will need to check LHS and family.
#
# pf <- PhyloFactor(
#   Data,
#   tree,
#   MetaData,
#   formula,
#   choice,
#   nfactors,
#   ncores)
#
# ## semantic type 1 - artifact (table)
# write.csv(pf$factors, sep='\t', row.names=TRUE, col.names=TRUE)
#
#
# tr <- pf.tree(pf,factors=factors)
# ##semantic type 2 - visualization
# tr$ggplot
