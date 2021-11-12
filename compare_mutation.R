library(dplyr)
library(purrr)
library(tidyverse)

setwd('.')

#table with pangolin and nextclade information by sample
nextstrain <- read.csv('nextclade_pangolin_data.csv', sep = '\t')

#data present on data/mutation_lineage_table.tsv, should be replaced by a table with user defined lineages
mutations <- read.csv('mutation_lineage_table.tsv', sep ='\t')

nextstrain_sub <- nextstrain %>%
  rename(mutation.sample = aaSubstitutions) %>%
  select(seqName, mutation.sample, lineage)

nextstrain_sub_mutations <- reduce(list(nextstrain_sub, mutations),full_join, by="lineage")

nextstrain_sub_mutations <- nextstrain_sub_mutations %>% 
  mutate(mutation = strsplit(as.character(mutation), ","),
         mutation.sample = strsplit(as.character(mutation.sample), ","),
         sample.mutation.extra =  map2(mutation.sample,mutation,setdiff),
         sample.mutation.extra.number =  lengths(sample.mutation.extra),
         lineage.mutation.lack = map2(mutation,mutation.sample,setdiff),
         lineage.mutation.lack.number =  lengths(lineage.mutation.lack))

output <- reduce(list(nextstrain, nextstrain_sub_mutations), full_join, by="seqName")
output$mutation.sample <- sapply(output$mutation.sample, paste, collapse=",")
output$mutation <- sapply(output$mutation, paste, collapse=",")
output$sample.mutation.extra <- sapply(output$sample.mutation.extra, paste, collapse=",")
output$lineage.mutation.lack <- sapply(output$lineage.mutation.lack , paste, collapse=",")
write.table(output, './teste_up.tsv', sep='\t')
