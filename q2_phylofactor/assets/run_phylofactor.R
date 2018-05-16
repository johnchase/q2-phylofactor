#!/usr/bin/env Rscript

# cat(R.version$version.string, "\n")
R.version
args <- commandArgs(TRUE)
# # print(args)
# table.path <- args[[1]]
# # library(MASS)
# # write.table(motors, file=table.path, sep='\t', row.names=TRUE, col.names=TRUE)
#
#
# # tree.path <- args[[2]]
# # out.path <- args[[3]]
# # metadata.path <- args[[4]]
# # taxonomy.path <- args[[5]]
# # formula <- as.formula(args[[6]])
# # choice <- args[[7]]
# # nfactors <- as.integer(args[[8]])
# # ncores <- as.integer(args[[9]])
# print('***********************ARE we getting here!!!!!!!*******')
# print(table.path)
# # Data <- read.csv(table.path)
# # write.csv(pf$factors, file = out.path, sep = '\t', row.names = TRUE, col.names = TRUE)
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
