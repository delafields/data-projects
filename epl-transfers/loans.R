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
    geom_line(size = 1.5) + 
    ggtitle("Premier League loans in & loans out (1992 - 2018)") +
    theme(plot.title = element_text(face = "bold", color = "#38003c", margin = margin(10, 0, 10, 0)), 
          axis.title.x = element_text(face = "bold"),
          axis.title.y = element_text(face = "bold"),
          text = element_text(family = "mono"),
          panel.background = element_rect(fill = 'white'),
          panel.grid.major = element_line(colour = "#e0e0e0", linetype = "dashed", size=0.1),
          panel.grid.minor = element_blank(),
          legend.position = c(0.2, 0.75),
          legend.background = element_rect(linetype="solid", color = "black"),
          legend.key=element_rect(fill='white')) + 
    labs(color = "Transfer Movement", x = "\nYear", y = "# of Loans\n") +
    scale_y_continuous(breaks = pretty(loans_per_year$num_loans, n = 10)) + 
    scale_x_continuous(breaks = pretty(loans_per_year$year, n = 10)) + 
    scale_color_manual(values = c("#00ff85", "#e90052"))


# Loans per team
ggplot(data=loans_per_team, aes(x = reorder(club_name, num_loans), y = num_loans, fill=transfer_movement, label = num_loans)) + 
    geom_bar(stat="identity", color = "#38003c") + 
    coord_flip() + 
    ggtitle("Premier League loans per team (1992 - 2018)") +
    theme(plot.title = element_text(face = "bold", color = "#38003c", margin = margin(10, 0, 10, 0)), 
          axis.title.x = element_text(face = "bold"),
          axis.title.y = element_text(face = "bold"),
          text = element_text(family = "mono"),
          panel.background = element_rect(fill = 'white'),
          panel.grid.major = element_line(colour = "#e0e0e0", linetype = "dashed", size=0.1),
          panel.grid.major.y = element_blank(),
          panel.grid.minor = element_blank(),
          legend.position = c(0.9, 0.2),
          legend.background = element_rect(linetype="solid", color = "black"),
          legend.key=element_rect(fill='white')) + 
    labs(color = "Transfer Movement", x = "\nClub", y = "# of Loans\n") + 
    scale_fill_manual(values = c("#00ff85", "#e90052")) +
    geom_text(size = 3, position = position_stack(vjust = 0.5))