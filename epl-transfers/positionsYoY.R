library(dplyr)
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
QC <- grouped_data %>% group_by(position) %>% summarise(sum(inf_adj_spend))

# Adding positional grouping
Midfield <- c("Attacking Midfield", "Defensive Midfield", "Midfielder", 
              "Central Midfield", "Right Midfield", "Left Midfield")
Defense <- c("Right-Back", "Centre-Back", "Goalkeeper", "Defender", "Left-Back")
Forward <- c("Centre-Forward", "Left Winger", "Right Winger", "Forward", "Second Striker")

grouped_data <- grouped_data %>%
    mutate(pos_group = case_when(position %in% Midfield ~ "Midfield",
                                 position %in% Defense ~ "Defense",
                                 position %in% Forward ~ "Forward"))

# filter out positions for which there isn't much data
`%notin%` <- Negate(`%in%`)

grouped_data <- grouped_data %>%
    filter(position %notin% c("Midfielder", "Defender", "Forward"))

###
# PLOTTING
###
grouped_data <- rename(grouped_data, Position = position) #For renaming dataframe column


# clean up the styling
ggplot(grouped_data, aes(x = year, y = total_spend)) +
    geom_line(aes(color = position, linetype = position)) +
    facet_wrap(~ pos_group, nrow = 3)

lineplotter <- function(df_group) {
    ggplot(df_group, aes(x = year, y = total_spend)) +
        geom_line(aes(color = Position), linetype = "solid", size=1) + 
        scale_x_continuous(breaks = pretty(df_group$year, n = 10)) +
        labs(x = "\nYear") + 
        theme(plot.title = element_text(face = "bold", color = "#38003c", margin = margin(10, 0, 10, 0)),
              axis.title.x = element_text(face = "bold", color = "#38003c"),
              axis.title.y = element_text(face = "bold", color = "#38003c"),
              axis.text.x = element_text(color = "#38003c"),
              axis.text.y = element_text(color = "#38003c"),
              text = element_text(family = "URWGothic"),
              panel.grid.major = element_line(colour = "#e0e0e0", linetype = "dashed", size=0.1),
              panel.grid.minor = element_blank(),
              panel.border = element_blank(), 
              #axis.line = element_line(),
              axis.line.x = element_line(),
              panel.background = element_blank(),
              legend.title = element_text(face = "bold", color = "#38003c"),
              legend.text = element_text(color = "#38003c"),
              #legend.background = element_rect(linetype="solid", color = "#38003c", size = 1),
              legend.key=element_rect(fill='white')) + 
        ylim(-125, 275) +
        ggtitle("Spend per Position in the Prem (millions £)\n")
        #+ scale_color_manual(values=c("#04f5ff", "#e90052", "#00ff85", "#38003c", "#ebfe05", "#a6004c"))
    }

mf_plot <- lineplotter(grouped_data %>% filter(pos_group == 'Midfield'))
fwd_plot <- lineplotter(grouped_data %>% filter(pos_group == 'Forward'))
def_plot <- lineplotter(grouped_data %>% filter(pos_group == 'Defense'))


plot_grid(fwd_plot + theme(axis.title.x = element_blank(),
                           axis.title.y = element_blank()), 
          mf_plot + theme(axis.title.x = element_blank(),
                          axis.title.y = element_blank(),
                          plot.title = element_blank()), 
          def_plot + theme(axis.title.y = element_blank(),
                           plot.title = element_blank()),  
          ncol = 1, 
          align = "v")



# plotly
mf_pplot <- plot_ly(grouped_data %>% filter(pos_group == 'Midfield'), color = ~position,
        x = ~year, y = ~total_spend) %>%
    add_lines()

fwd_pplot <- plot_ly(grouped_data %>% filter(pos_group == 'Forward'), color = ~position,
                    x = ~year, y = ~total_spend) %>%
    add_lines()

def_pplot <- plot_ly(grouped_data %>% filter(pos_group == 'Defense'), color = ~position,
                    x = ~year, y = ~total_spend) %>%
    add_lines()

subplot(mf_pplot, fwd_pplot, def_pplot, nrows = 3)