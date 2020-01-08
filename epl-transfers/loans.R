library(dplyr)
library(ggplot2)
library(stringr)
library(showtext)
library(cowplot)

# merges multiple csvs together
multmerge = function(path){
    filenames = list.files(path=path, full.names=TRUE)
    
    datalist = lapply(filenames, function(x){
        read.csv(file = x, header = T)})
    
    Reduce(function(x, y) {merge(x, y, all = TRUE)}, datalist)
}

# merge all transfer data
transfer_data <- multmerge("data/transfer-data")

# narrow to where fee = `Loan`
loans <- transfer_data %>%
    filter(str_detect(fee, "Loan"))

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

##################
# WAYS TO FILTER #
##################

# see who's been in the league this whole period
tenure <- loans %>% 
    select(club_name, year) %>% 
    distinct() %>% 
    count(club_name) %>% 
    arrange(desc(n)) %>%
    rename("years_of_data" = n)

# narrow to teams with > 40 loans
over_40 <- loans_per_team %>%
    group_by(club_name) %>%
    summarise(total_loans = sum(num_loans)) %>%
    filter(total_loans > 40)

loans_per_team <- loans_per_team %>% right_join(over_40)

# EVEN FURTHER narrow to top 20 loaners
loans_per_team <- loans_per_team %>% 
    arrange(desc(total_loans)) %>%
    .[1:40, ]

############
# PLOTTING #
############

## Loading Google fonts (http://www.google.com/fonts)
font_add_google("Poppins", "poppins")

## Automatically use showtext to render text for future devices
showtext_auto()

## Plotting functions as usual
## Open a graphics device if you want, e.g.
## png("demo.png", 700, 600, res = 96)
## If you want to show the graph in a window device,
## remember to manually open one in RStudio
## See the "Known Issues" section
windows()


# Loans per year plot
ggplot(loans_per_year, aes(year, num_loans, group=transfer_movement, color=transfer_movement)) + 
    geom_line(size = 1.5) + 
    ggtitle("Out on loan", subtitle="Premier League loans in & loans out (1992 - 2018)") +
    labs(color = "Transfer Movement", x = "\nYear", y = "# of Loans\n") +
    scale_y_continuous(breaks = pretty(loans_per_year$num_loans, n = 10)) + 
    scale_x_continuous(breaks = pretty(loans_per_year$year, n = 10)) + 
    scale_color_manual(values = c("#00ff85", "#e90052")) + 
    theme(text = element_text(family = "poppins"), 
          plot.title = element_text(face = "bold", color = "#38003c", margin = margin(10, 0, 10, 0)), 
          axis.title.x = element_text(face = "bold"),
          axis.title.y = element_text(face = "bold"),,
          panel.background = element_rect(fill = 'white'),
          panel.grid.major = element_line(colour = "#e0e0e0", linetype = "dashed", size=0.1),
          panel.grid.minor = element_blank(),
          legend.position = c(0.2, 0.75),
          legend.background = element_rect(linetype="solid", color = "black"),
          legend.key=element_rect(fill='white'))


# Loans per team plot
ggplot(data=loans_per_team, aes(x = reorder(club_name, num_loans), y = num_loans, fill=transfer_movement, label = num_loans)) + 
    geom_bar(stat="identity", color = "#38003c") + 
    coord_flip() + 
    geom_text(size = 3, position = position_stack(vjust = 0.5)) +
    ggtitle("Chelsea leads the way", subtitle="Premier League loans per team (1992 - 2018)") +
    labs(x = "Club\n", y = "\n# of Loans", fill="Transfer Movement") +
    scale_fill_manual(values = c("#00ff85", "#e90052")) + 
    theme(plot.title = element_text(face = "bold", color = "#38003c", margin = margin(10, 0, 10, 0)), 
          axis.title.x = element_text(face = "bold"),
          axis.title.y = element_text(face = "bold"),
          text = element_text(family = "poppins"),
          panel.background = element_rect(fill = 'white'),
          panel.grid.major = element_line(colour = "#e0e0e0", linetype = "dashed", size=0.1),
          panel.grid.major.y = element_blank(),
          panel.grid.minor = element_blank(),
          legend.position = c(0.9, 0.2),
          legend.background = element_rect(linetype="solid", color = "black"),
          legend.key=element_rect(fill='white'))


# Loans per team by transfer movement
loans_in <- loans_per_team %>% filter(transfer_movement == "in")
loans_out <- loans_per_team %>% filter(transfer_movement == "out")

outp <- ggplot(data=loans_out, aes(x = reorder(club_name, num_loans), y = num_loans, label = num_loans)) + 
    geom_bar(stat="identity", color = "#38003c", fill="#e90052") + 
    coord_flip() + 
    ggtitle("Chelsea (and the Big 6) sends them out", subtitle="Premier League loans out per team (1992 - 2018)") +
    labs(color = "Transfer Movement", x = "\nClub", y = "\n# of Loans Out") +
    geom_text(size = 3, position = position_stack(vjust = 0.5)) + 
    theme(plot.title = element_text(face = "bold", color = "#38003c", margin = margin(10, 0, 10, 0)), 
          axis.title.x = element_text(face = "bold"),
          axis.title.y = element_text(face = "bold"),
          text = element_text(family = "poppins"),
          panel.background = element_rect(fill = 'white'),
          panel.grid.major = element_line(colour = "#e0e0e0", linetype = "dashed", size=0.1),
          panel.grid.major.y = element_blank(),
          panel.grid.minor = element_blank(),
          legend.position = c(0.9, 0.2),
          legend.background = element_rect(linetype="solid", color = "black"),
          legend.key=element_rect(fill='white'))

inp <- ggplot(data=loans_in, aes(x = reorder(club_name, num_loans), y = num_loans, label = num_loans)) + 
    geom_bar(stat="identity", color = "#38003c", fill="#00ff85") + 
    coord_flip() + 
    ggtitle("West Ham brings them in", subtitle=" ") +
    labs(color = "Transfer Movement", x = "\nClub", y = "\n# of Loans In") + 
    geom_text(size = 3, position = position_stack(vjust = 0.5)) + 
    theme(plot.title = element_text(face = "bold", color = "#38003c", margin = margin(10, 0, 10, 0)), 
          axis.title.x = element_text(face = "bold"),
          axis.title.y = element_text(face = "bold"),
          text = element_text(family = "poppins"),
          panel.background = element_rect(fill = 'white'),
          panel.grid.major = element_line(colour = "#e0e0e0", linetype = "dashed", size=0.1),
          panel.grid.major.y = element_blank(),
          panel.grid.minor = element_blank(),
          legend.position = c(0.9, 0.2),
          legend.background = element_rect(linetype="solid", color = "black"),
          legend.key=element_rect(fill='white'))

plot_grid(outp, inp + theme(axis.title.y = element_blank()),
          ncol=2)