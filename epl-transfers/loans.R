library(dplyr)
library(ggplot2)
library(stringr)

# merges multiple csvs together
multmerge = function(path){
    filenames = list.files(path=path, full.names=TRUE)
    
    datalist = lapply(filenames, function(x){
        read.csv(file = x, header = T)})
    
    Reduce(function(x, y) {merge(x, y, all = TRUE)}, datalist)
}

# merge the transfer data
transfer_data <- multmerge("data/transfer-data")

# narrow to where fee = 'Loan'
loans <- transfer_data %>%
    filter(str_detect(fee, "Loan"))

# see who's been in the league this whole period
temp <- loans %>% 
    select(club_name, year) %>% 
    distinct() %>% 
    count(club_name) %>% 
    arrange(desc(n)) %>%
    rename("years_of_data" = n)

# get counts of loans in/out per team
loans_per_team <- loans %>%
    group_by(club_name) %>%
    count(transfer_movement) %>%
    rename("num_loans" = n)

# get loans per year
loans_per_year <- loans %>%
    group_by(year) %>%
    count(transfer_movement) %>%
    rename("num_loans" = n)

#####################
# PLOTTING
#####################

# Loans per year
ggplot(loans_per_year, aes(year, num_loans, group=transfer_movement, color=transfer_movement)) + 
    geom_line()


# Loans per team
ggplot(data=loans_per_team, aes(x = reorder(club_name, num_loans), y = num_loans, fill=transfer_movement)) + 
    geom_bar(stat="identity") + 
    coord_flip()

# Loans per team split by transfer_movement
p <- ggplot(data=loans_per_team, aes(x = reorder(club_name, num_loans), y = num_loans, order = num_loans)) + 
    geom_bar(stat="identity") + 
    coord_flip()

p + facet_wrap(vars(transfer_movement))