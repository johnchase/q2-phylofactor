#!/usr/bin/env Rscript

library(phylofactor)

# The following line ensures that distuils does not try to compile this as
# python. It can likly be removed once script is completed
.this <- "this"

args <- commandArgs(TRUE)
table.path <- args[[1]]
out.path <- args[[2]]
tree.path <- args[[3]]
taxonomy.str <- args[[4]]
metadata.path <- args[[5]]
formula <- as.formula(args[[6]])
choice <- args[[7]]
nfactors <- as.integer(args[[8]])
ncores <- as.integer(args[[9]])

table <- read.table(
    file = table.path,
    check.names = FALSE)

metadata <- read.table(
    metadata.path,
    sep = '\t',
    comment.char = "",
    header = TRUE,
    check.names = FALSE,
    stringsAsFactors = FALSE
    )
# The second row of qiime dataframes is often defining the datatype for a give
# column. I am ingnoring this for the time being but it should be added back
# in at somepoint
if (startsWith(metadata[1, 1], '#')) {
      metadata <- metadata[-c(1), ]
 }

tree <- read.tree(tree.path)

table
pf <- PhyloFactor(
  table,
  tree,
  metadata,
  formula,
  choice,
  nfactors,
  ncores)

# ## semantic type 1 - artifact (table)
write.csv(pf$factors, sep='\t', row.names=TRUE, col.names=TRUE)
### write.table(otu_table, out.path, sep = '\t')
##
###
### tr <- pf.tree(pf,factors=factors)
## ##semantic type 2 - visualization
## tr$ggplot
