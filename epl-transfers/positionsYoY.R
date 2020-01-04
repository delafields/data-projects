library(dplyr)
library(ggplot2)
library(ggridges)
#install.packages("ggridges")

# merges multiple csvs together
multmerge = function(path){
    filenames = list.files(path=path, full.names=TRUE)
    
    datalist = lapply(filenames, function(x){
        read.csv(file = x, header = T)})
    
    Reduce(function(x, y) {merge(x, y, all = TRUE)}, datalist)
}

# merge the data
data <- multmerge("data/transfer-data")

# only keep these columns
cols <- c("position", "fee_cleaned", "year", "transfer_movement", "season")
data <- data[cols]

# replace na's with 0's
data[is.na(data)] <- 0

# multiply "out" transfers by -1
data <- data %>%
    mutate(correct_fee = ifelse(transfer_movement == "out", fee_cleaned * -1, fee_cleaned))

grouped_data <- data %>%
    group_by(position, year) %>%
    summarise(total_spend = sum(correct_fee)) %>%
    filter(position != "Sweeper") # no data here

# Taking inflation into account
inflation <- read.csv(file = "data/Inflation_Adjustment.csv", fileEncoding="UTF-8-BOM")

grouped_data <- grouped_data %>% 
    left_join(inflation, by="year") %>%
    mutate(inf_adj_spend = total_spend * (1 + .01 * Inflation))

# double checking the spend
QC <- grouped_data %>% group_by(position, year) %>% summarise(sum(inf_adj_spend))


###
# PLOTTING
###

# don't think this is gonna work
ggplot(grouped_data, aes(x = total, y = position)) + 
    geom_density_ridges(scale=1, rel_min_height=0.001)

# clean up the styling
ggplot(grouped_data, aes(x = year, y = total_spend)) +
    geom_line(aes(color = position, linetype = position))

