library(dplyr)
library(showtext)
library(ggplot2)
library(cowplot)
library(plotly)

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

# multiply "out" transfers by -1 and sum by transfer movement
grouped_data <- data %>%
    mutate(correct_fee = ifelse(transfer_movement == "out", fee_cleaned * -1, fee_cleaned)) %>%
    group_by(position, year) %>%
    summarise(total_spend = sum(correct_fee))

# Taking inflation into account
inflation <- read.csv(file = "data/Inflation_Adjustment.csv", fileEncoding="UTF-8-BOM")

grouped_data <- grouped_data %>% 
    left_join(inflation, by="year") %>%
    mutate(inf_adj_spend = total_spend * (1 + .01 * Inflation))

# double checking the spend
QC <- grouped_data %>% group_by(position) %>% summarise(sum(inf_adj_spend))

# Adding positional grouping
Midfield <- c("Attacking Midfield", "Defensive Midfield", "Midfielder", 
              "Central Midfield", "Right Midfield", "Left Midfield")
Defense <- c("Right-Back", "Centre-Back", "Goalkeeper", "Defender", "Left-Back", "Sweeper")
Forward <- c("Centre-Forward", "Left Winger", "Right Winger", "Forward", "Second Striker")

grouped_data <- grouped_data %>%
    mutate(pos_group = case_when(position %in% Midfield ~ "Midfield",
                                 position %in% Defense ~ "Defense",
                                 position %in% Forward ~ "Forward"))

# filter out positions for which there isn't much data
`%notin%` <- Negate(`%in%`)

grouped_data <- grouped_data %>%
    filter(position %notin% c("Midfielder", "Defender", "Forward", "Sweeper"))

# Rename for plotting
grouped_data <- rename(grouped_data, Position = position)

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

# function for creating multiple plots
lineplotter <- function(df_group) {
    ggplot(df_group, aes(x = year, y = total_spend)) +
        geom_line(aes(color = Position), linetype = "solid", size=1) +
        ggtitle("People in the Center are getting PAID",
                subtitle = "Spend per position in the Prem (millions £)\n") +
        labs(x = "\nYear") + 
        scale_color_manual(values=c("#04f5ff", "#e90052", "#00ff85", "#ebfe05", "#38003c", "#500057")) + 
        scale_x_continuous(breaks = pretty(df_group$year, n = 10)) +
        ylim(-125, 275) +
        theme(text = element_text(family = "poppins"),
              plot.title = element_text(face = "bold", color = "#38003c", margin = margin(10, 0, 10, 0)),
              axis.title.x = element_text(face = "bold"),
              axis.title.y = element_text(face = "bold"),
              axis.line.x = element_line(),
              panel.grid.major = element_line(colour = "#e0e0e0", linetype = "dashed", size=0.1),
              panel.grid.major.x = element_blank(),
              panel.grid.minor = element_blank(),
              panel.border = element_blank(), 
              panel.background = element_blank(),
              legend.title = element_text(face = "bold"),
              legend.key=element_rect(fill='white')) 
}

mf_plot <- lineplotter(grouped_data %>% filter(pos_group == 'Midfield'))
fwd_plot <- lineplotter(grouped_data %>% filter(pos_group == 'Forward'))
def_plot <- lineplotter(grouped_data %>% filter(pos_group == 'Defense'))


plot_grid(fwd_plot + labs(color="Attack") +
              theme(axis.title.x = element_blank(),
                    axis.title.y = element_blank()), 
          mf_plot + labs(color="Midfield") +
              theme(axis.title.x = element_blank(),
                    axis.title.y = element_blank(),
                    plot.title = element_blank(),
                    plot.subtitle = element_blank()), 
          def_plot + labs(color="Defense") +
              theme(axis.title.y = element_blank(),
                    plot.title = element_blank(),
                    plot.subtitle = element_blank()),  
          ncol = 1, 
          align = "v")