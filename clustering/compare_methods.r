library(tidyverse)
library(clValid)

setwd(file.path('E:', 'db'))

df <- read_csv('recordings_excluded.csv')
setwd(file.path('E:', 'db'))


df1 <- select(df, mfr, 'cv isi')
df1 <- scale(df1)


clmethods <- c("hierarchical","kmeans")
#clmethods <- c("hierarchical","kmeans","pam")
intern <- clValid(df1, nClust = 3:6,
                clMethods = clmethods, validation = "internal",
                maxitems = 1000000)

sink("comp.csv")
print(summary(intern))
sink()