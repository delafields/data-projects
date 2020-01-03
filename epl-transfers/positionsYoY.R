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
cols <- c('position', 'fee_cleaned', 'year', 'transfer_movement')
data <- data[cols]

# replace na's with 0's
data[is.na(data)] <- 0

# multiply "out" transfers by -1
data <- data %>%
    mutate(correct_fee = ifelse(transfer_movement == 'out', fee_cleaned * -1, fee_cleaned))

grouped_data <- data %>%
    group_by(position, year) %>%
    summarise(total_spend = sum(correct_fee))

# TODO - Taking inflation into account


###
# PLOTTING
###

# don't think this is gonna work
ggplot(grouped_data, aes(x = total, y = position)) + 
    geom_density_ridges(scale=1, rel_min_height=0.001)

# clean up the styling
ggplot(grouped_data, aes(x = year, y = total_spend)) +
    geom_line(aes(color = position, linetype = position))
