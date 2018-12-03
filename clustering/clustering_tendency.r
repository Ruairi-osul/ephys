library(tidyverse)
library(readr)
library(factoextra)
library(clustertend)

df <- read_csv('recordings_excluded.csv')
setwd(file.path('E:', 'db'))


df1 <- select(df, mfr, 'cv isi')
df1 <- scale(df1)

random_df <- apply(df1, 2,
                   function(x){runif(length(x), min(x), (max(x)))})
random_df <- as.data.frame(random_df)

km_res1 <- kmeans(df1, 3)
fviz_cluster(list(data=df1, cluster= km_res1$cluster),
             ellipse.type='norm', geom='point', stand=FALSE,
             palette='jco', ggtheme= theme_classic())


#fviz_dend(hclust(dist(df1)), k=5, as.ggplot=TRUE)
#hopkins(random_df, n=nrow(random_df)-1)
#hopkins(df1, n=nrow(df1)-1)

#fviz_dist(dist(df1), show_labels = FALSE)+
#  labs(title = "DRN Data")

#fviz_dist(dist(random_df), show_labels = FALSE)+
#  labs(title = "Random data")




