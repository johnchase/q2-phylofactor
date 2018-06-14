#!/usr/bin/env Rscript

library(phylofactor)

# The following line ensures that distuils does not try to compile this as
# python. It can likly be removed once script is completed
.this <- "this"

args <- commandArgs(TRUE)
table.path <- args[[1]]
tree.path <- args[[2]]
metadata.path <- args[[3]]
family <- get(args[[4]])
formula <- as.formula(args[[5]])
choice <- args[[6]]
nfactors <- as.integer(args[[7]])
ncores <- as.integer(args[[8]])
out_table.path <- args[[9]]
out_tree.path <- args[[10]]
# out_group.path <- args[[11]]

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

#Convert the data to types that R can understand
metadata.types <- metadata[1, ]
metadata <- metadata[-c(1), ]

rownames(table) <- table$"#OTU ID"
table$"#OTU ID" <- NULL
table <- data.matrix(table)
table <- table[, unlist(metadata[1], use.names = FALSE)]
rownames(metadata) <- unlist(metadata[1], use.names = FALSE)

metadata <- lapply(metadata, factor)
print(typeof(metadata$Subject))

pf <- PhyloFactor(
  Data = table,
  tree = tree,
  X = metadata,
  family = family,
  frmla = formula,
  choice = choice,
  nfactors = nfactors,
  ncores = ncores)

Y <- t(pf$basis) %*% log(pf$Data) %>% t
Y <- as.data.frame(Y)
names(Y) <- sapply(1:nfactors, FUN = function(x) paste("Factor_", x, sep = ""))
Y <- cbind("#OTU ID" = rownames(Y), Y)


## write table
write.table(Y,
          file = out_table.path,
          sep = "\t",
          row.names = FALSE,
          col.names = TRUE,
          quote = FALSE)


## write groups as data frame
groups_to_df <- function(g){
  DF <- NULL
  for (i in 1:length(g)){
    DF <- rbind(DF, data.frame("factor" = rep(i, length(unlist(g[[i]]))),
                              "group" = c(rep(1, length(g[[i]][[1]])),
                              rep(2, length(g[[i]][[2]]))),
                              "index" = unlist(g[[i]]),
                              stringsAsFactors = F))
  }
  return(DF)
}

group.df <- groups_to_df(pf.groupsTospecies(pf))
# write.table(group.df,
#             file = out_group.path,
#             row.names = FALSE,
#             col.names = TRUE,
#             quote = FALSE,
#             sep = "\t")

## write tree
write.tree(pf$tree,
           file = out_tree.path)
