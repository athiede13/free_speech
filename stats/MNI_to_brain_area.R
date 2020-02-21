#----------------------------------------------------------------
#----------------------------------------------------------------#
# Find AAL brain areas from MNI coordinates
# 
# Author: Anja Thiede <anja.thiede@helsinki.fi>
#----------------------------------------------------------------#

# import packages ---------------
install.packages("devtools")
library("devtools")
install_github("yunshiuan/label4MRI")
library(label4MRI)
library(readxl)
install.packages("splitstackshape")
library(splitstackshape)

# ISC significance-----------
m <- read_excel("Z:/proj/free_speech/results/ISCs_comp_against_0/MNI_table.xlsx", sheet = "coord_only")
View(m)
Result <- t(mapply(FUN = mni_to_region_name, x = m$x, y = m$y, z = m$z))
View(Result)
write.csv(Result,"Z:/proj/free_speech/results/ISCs_comp_against_0/MNI_brain_areas.csv")

# ISC contrast------------------
#windows
#m <- read_excel("I:/results/dys_con_contrast/2019_05_t_test+cluster_correction/MNI_table.xlsx", sheet = "coord_only")
#linux
m <- read.csv("/media/cbru/SMEDY/results/dys_con_contrast/2020_02_redo_subject_perm/mni_corrdinates_out.csv",
                header=FALSE)
# split concatenated column by `_`
m <- concat.split(data = m, split.col = "V3", sep = " ", drop = TRUE)

# remove extra stuff
m$V3_1 <- gsub(pattern="['", replacement="", m$V3_1, fixed = TRUE)
m$V3_1 <- gsub(pattern="'", replacement="", m$V3_1, fixed = TRUE)
m$V3_2 <- gsub(pattern="'", replacement="", m$V3_2, fixed = TRUE)
m$V3_3 <- gsub(pattern="']", replacement="", m$V3_3, fixed = TRUE)
m$V3_3 <- gsub(pattern="'", replacement="", m$V3_3, fixed = TRUE)

View(m)
# rename MNI coordinate columns
names(m)[names(m)=="V3_1"] <- "x"
names(m)[names(m)=="V3_2"] <- "y"
names(m)[names(m)=="V3_3"] <- "z"

# convert to numbers
m$x <- as.numeric(m$x)
m$y <- as.numeric(m$y)
m$z <- as.numeric(m$z)

Result <- t(mapply(FUN = mni_to_region_name, x = m$x, y = m$y, z = m$z))
View(Result)
#write.csv(Result,"E:/results/dys_con_contrast/2019_05_t_test+cluster_correction/MNI_brain_areas.csv")
write.csv(Result,"/media/cbru/SMEDY/results/dys_con_contrast/2020_02_redo_subject_perm/MNI_brain_areas.csv")

# mantel correlations----------------
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