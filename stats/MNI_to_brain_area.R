install.packages("devtools")
library("devtools")
install_github("yunshiuan/label4MRI")
library(label4MRI)
library(readxl)

m <- read_excel("Z:/proj/free_speech/results/ISCs_comp_against_0/MNI_table.xlsx", sheet = "coord_only")
View(m)
Result <- t(mapply(FUN = mni_to_region_name, x = m$x, y = m$y, z = m$z))
View(Result)
write.csv(Result,"Z:/proj/free_speech/results/ISCs_comp_against_0/MNI_brain_areas.csv")

#windows
#m <- read_excel("I:/results/dys_con_contrast/2019_05_t_test+cluster_correction/MNI_table.xlsx", sheet = "coord_only")
#linux
m <- read_excel("/media/cbru/SMEDY/results/dys_con_contrast/2019_05_t_test+cluster_correction/mni_corrdinates_out.xlsx",
                col_names=FALSE)
View(m)
names(m)[names(m)=="...4"] <- "x"
names(m)[names(m)=="...5"] <- "y"
names(m)[names(m)=="...6"] <- "z"
Result <- t(mapply(FUN = mni_to_region_name, x = m$x, y = m$y, z = m$z))
View(Result)
write.csv(Result,"E:/results/dys_con_contrast/2019_05_t_test+cluster_correction/MNI_brain_areas.csv")
write.csv(Result,"/media/cbru/SMEDY/results/dys_con_contrast/2019_05_t_test+cluster_correction/MNI_brain_areas.csv")

  #windows
# m <- read_excel("I:/results/mantel_correlations/2019_05_simple_model/mni_corrdinates_out.xlsx", 
#                 col_names=FALSE)
#linux
m <- read_excel("/media/cbru/SMEDY/results/mantel_correlations/2019_05_simple_model/mni_corrdinates_out.xlsx",
                col_names=FALSE)
View(m)
names(m)[names(m)=="...4"] <- "x"
names(m)[names(m)=="...5"] <- "y"
names(m)[names(m)=="...6"] <- "z"

Result <- t(mapply(FUN = mni_to_region_name, x = m$x, y = m$y, z = m$z))
View(Result)
write.csv(Result,"I:/results/mantel_correlations/2019_05_simple_model/MNI_brain_areas.csv")

mni_to_region_name(65,	-26,	-13)