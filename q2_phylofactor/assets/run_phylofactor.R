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


table <- read.csv(
    file = table.path,
    check.names = FALSE,
    header = TRUE,
    comment.char = "",
    sep="\t",
    skip=1,
    )

tree <- read.tree(tree.path)

metadata <- read.csv(
    file = metadata.path,
    sep = '\t',
    comment.char = "",
    header = TRUE,
    check.names = FALSE,
    stringsAsFactors = FALSE
   )

if (startsWith(metadata[1, 1], '#')) {
    metadata <- metadata[-c(1), ]
 }

taxonomy <- read.csv(
    file = taxonomy.path,
    check.names = FALSE,
    header = TRUE,
    comment.char = "",
    sep="\t",
    )
taxonomy <- taxonomy[, c('Feature ID', 'Taxon')]


rownames(table) <- table$'#OTU ID'
table$'#OTU ID' <- NULL
table = data.matrix(table)
table = table[, metadata$'#SampleID']

# TODO: This is a placeholder for testing only
colnames(table) = metadata$BodySite

pf <- PhyloFactor(
    table, 
    tree,
    metadata$BodySite,
    nfactors = 3)

#pf <- PhyloFactor(
#  table,
#  tree,
#  metadata,
#  BodySite~Data,
#  choice,
#  nfactors,
#  ncores)

 ## semantic type 1 - artifact (table)
#write.csv(pf$factors, 
#          file = out.path,
#          sep = '\t',
#          row.names = TRUE,
#          col.names = TRUE)

print('is this printing*************************************************************')
write.csv(pf$factors, 
          file = '/home/john/dev/q2-phylofactor/phylo_result.tsv',
          sep = '\t',
          row.names = TRUE,
          col.names = TRUE
          )
## write.table(otu_table, out.path, sep = '\t')
#
##
## tr <- pf.tree(pf,factors=factors)
# ##semantic type 2 - visualization
# tr$ggplot
