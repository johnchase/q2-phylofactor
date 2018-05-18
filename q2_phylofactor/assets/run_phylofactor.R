#!/usr/bin/env Rscript

library(phylofactor)

# The following line ensures that distuils does not try to compile this as
# python. It can likly be removed once script is completed
.this <- "this"

args <- commandArgs(TRUE)
table.path <- args[[1]]
out.path <- args[[2]]
tree.path <- args[[3]]
taxonomy.path <- args[[4]]
metadata.path <- args[[5]]
formula <- as.formula(args[[6]])
choice <- args[[7]]
nfactors <- as.integer(args[[8]])
ncores <- as.integer(args[[9]])

table <- read.table(file = table.path)
tree <- read.tree(tree.path)
# taxonomy <- read.csv(taxonomy.path, row.names = 1)
metadata <- read.csv(metadata.path, row.names = 1)

pf <- PhyloFactor(
  table,
  tree,
  metadata,
  formula,
  choice,
  nfactors,
  ncores)

print(pf$factors)
# ## semantic type 1 - artifact (table)
# write.csv(pf$factors, sep='\t', row.names=TRUE, col.names=TRUE)
# write.table(otu_table, out.path, sep = '\t')

#
# tr <- pf.tree(pf,factors=factors)
# ##semantic type 2 - visualization
# tr$ggplot
