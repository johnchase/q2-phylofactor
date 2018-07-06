#!/usr/bin/env Rscript

library(phylofactor)

args <- commandArgs(TRUE)
table.path <- args[[1]]
tree.path <- args[[2]]
metadata.path <- args[[3]]
family <- get(args[[4]])
formula <- as.formula(args[[5]])
choice <- args[[6]]
nfactors <- as.integer(args[[7]])
ncores <- as.integer(args[[8]])
basis.path <- args[[9]]
out_tree.path <- args[[10]]
group.path <- args[[11]]
factor.path <- args[[12]]

table <- read.csv(
    file = table.path,
    check.names = FALSE,
    header = TRUE,
    comment.char = "",
    sep = "\t",
    skip = 1
    )

tree <- read.tree(tree.path)

metadata <- read.csv(
    file = metadata.path,
    sep = "\t",
    comment.char = "",
    header = TRUE,
    check.names = FALSE,
    stringsAsFactors = FALSE
   )

metatdata.type <- function(metadata) {
  metadata.types <- metadata[1, ]
  metadata <- metadata[-c(1), ]
  categorical.columns <- colnames(metadata)[metadata.types == "categorical"]
  metadata[categorical.columns] <- lapply(metadata[categorical.columns], factor)
  numeric.columns <- colnames(metadata)[metadata.types == "numeric"]
  metadata[numeric.columns] <- lapply(metadata[numeric.columns], as.numeric)
  return(metadata)
}

metadata <- metatdata.type(metadata)

rownames(table) <- table$"#OTU ID"
table$"#OTU ID" <- NULL
table <- data.matrix(table)
table <- table[, unlist(metadata[1], use.names = FALSE)]

pf <- PhyloFactor(
  Data = table,
  tree = tree,
  X = metadata,
  family = family,
  frmla = formula,
  choice = choice,
  nfactors = nfactors,
  ncores = ncores)

basis <- pf$basis
colnames(basis) <- sapply(1:nfactors,
                          FUN = function(x) paste("Factor_", x, sep = ""))
write.table(basis,
            file = basis.path,
            sep = "\t",
            row.names = TRUE,
            col.names = TRUE,
            quote = FALSE)


## write groups as data frame
groups_to_df <- function(g){
  DF <- NULL
  for (i in 1:length(g)){
    DF <- rbind(DF, data.frame("factor" = rep(i, length(unlist(g[[i]]))),
                              "group" = c(rep(1, length(g[[i]][[1]])),
                              rep(2, length(g[[i]][[2]]))),
                              "featureid" = unlist(g[[i]]),
                              stringsAsFactors = F))
  }
  return(DF)
}

group.df <- groups_to_df(pf.groupsTospecies(pf))
write.table(group.df,
            file = group.path,
            row.names = FALSE,
            col.names = TRUE,
            quote = FALSE,
            sep = "\t")

write.table(pf$factors,
            file = factor.path,
            row.names = TRUE,
            col.names = TRUE,
            quote = FALSE,
            sep = "\t")

## write tree
write.tree(pf$tree,
           file = out_tree.path)
