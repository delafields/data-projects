library(dplyr)
library(ggplot2)
library(stringr)
library(ggalt)
library(plotly)
library(gganimate)

# merges multiple csvs together
multmerge = function(path){
    filenames = list.files(path=path, full.names=TRUE)
    
    datalist = lapply(filenames, function(x){
        read.csv(file = x, header = T)})
    
    Reduce(function(x, y) {merge(x, y, all = TRUE)}, datalist)
}

# merge the transfer data
transfer_data <- multmerge("data/transfer-data")
# merge results data
results_data <- multmerge("data/epl-results")

# only keep these columns
cols <- c("club_name", "fee_cleaned", "year", "transfer_movement", "season")
transfer_data <- transfer_data[cols]

# replace na's with 0's
transfer_data[is.na(transfer_data)] <- 0

# multiply "out" transfers by -1
transfer_data <- transfer_data %>%
    mutate(correct_fee = ifelse(transfer_movement == 'out', fee_cleaned * -1, fee_cleaned))

# rank transfer amount ranking for each year
grouped_transfer_data <- transfer_data %>%
    group_by(club_name, year) %>%
    summarise(total_spend = sum(correct_fee))

grouped_transfer_data <- grouped_transfer_data %>%
    arrange(year) %>%
    mutate(spend_rank = dense_rank(desc(total_spend)))

# rename `club_name` to `Team` for later join
grouped_transfer_data <- rename(grouped_transfer_data, Team = club_name)

#temp <- grouped_transfer_data %>% filter(year == 2018)

# some regex work before joining
# trim year in the results df
# remove the (C) for Champion and (R) for relegated from Team name
results_data <- results_data %>% 
    mutate(season = year) %>%
    mutate(year = substr(year, start = 1, stop = 4)) %>%
    mutate(Team = str_replace_all(Team, " \\(\\S\\)", ""))


# rename transfer data team names to match results data
# remove FC and AFC from names then strip strings
grouped_transfer_data <- grouped_transfer_data %>%
    ungroup(Team) %>%
    mutate(Team = str_replace_all(Team, " FC", "")) %>%
    mutate(Team = str_replace_all(Team, "AFC", "")) %>%
    mutate(Team = trimws(Team))

# convert results_data `year` to numeric for later joining
results_data <- results_data %>%
    mutate(year = as.numeric(year))

# join transfers to results
data <- results_data %>% left_join(grouped_transfer_data, by = c("Team", "year"))




############
# PLOTTING #
############

# this works for one year. this is how it should look.
temp <- data %>% filter(year == 2012)

ptemp <- ggplot(temp, aes(x=Pos, xend=spend_rank, y=Team)) + 
    geom_segment(aes(x=Pos, 
                     xend=spend_rank, 
                     y=Team, 
                     yend=Team), 
                 color="black", size=1)+
    geom_dumbbell(color=NA,
                  size_x=6, 
                  size_xend = 6,
                  #Note: there is no US:'color' for UK:'colour' 
                  # in geom_dumbbel unlike standard geoms in ggplot()
                  colour_x="#38003c", 
                  colour_xend = "#00ff85")+
    labs(x="Position", y=NULL, 
         title="Spend vs. End of Season Rank", 
         subtitle="1992-2018")+
    geom_text(color="white", size=3, #hjust=-0.5,
              aes(x=Pos, label=Pos, fontface="bold"))+
    geom_text(aes(x=spend_rank, label=spend_rank, fontface="bold"), 
              color="black", size=3) + #, hjust=1.5)
    theme(plot.title = element_text(face = "bold", color = "#38003c"),
          plot.subtitle = element_text(color = "#38003c"),
          axis.title.x = element_text(face = "bold", color = "#38003c"),
          axis.text.x = element_text(color = "#38003c"),
          axis.text.y = element_text(color = "#38003c"),
          panel.background = element_blank(),
          panel.grid.major = element_line(colour = "#e0e0e0", linetype = "dashed", size=0.1))

ptemp

## temp using ggplot dumbell
# see link below for moving labels and changing them
# https://stackoverflow.com/questions/58507077/gganimate-change-axes-between-frames
# the answer is probably in the below thread
# https://stackoverflow.com/questions/53162821/animated-sorted-bar-chart-with-bars-overtaking-each-other/53163549#53163549


p <- ggplot(data, aes(x=Pos, xend=spend_rank, y=Team)) + 
    geom_segment(aes(x=Pos, 
                     xend=spend_rank, 
                     y=Team, 
                     yend=Team), 
                 color="black", size=1)+
    geom_dumbbell(color=NA,
                  size_x=6, 
                  size_xend = 6,
                  #Note: there is no US:'color' for UK:'colour' 
                  # in geom_dumbbel unlike standard geoms in ggplot()
                  colour_x="#38003c", 
                  colour_xend = "#00ff85")+
    labs(x="Position", y=NULL, 
         title="Spend vs. End of Season Rank", 
         subtitle="1992-2018")+
    geom_text(color="white", size=3, #hjust=-0.5,
              aes(x=Pos, label=Pos, fontface="bold"))+
    geom_text(aes(x=spend_rank, label=spend_rank, fontface="bold"), 
              color="black", size=3) + #, hjust=1.5)
    theme(plot.title = element_text(face = "bold", color = "#38003c"),
          plot.subtitle = element_text(color = "#38003c"),
          axis.title.x = element_text(face = "bold", color = "#38003c"),
          axis.text.x = element_text(color = "#38003c"),
          axis.text.y = element_text(color = "#38003c"),
          panel.background = element_blank(),
          panel.grid.major = element_line(colour = "#e0e0e0", linetype = "dashed", size=0.1))

animation <- p +  
    labs(title = 'Spend vs. End of Season Rank: {closest_state}', y = 'Position') +
    transition_states(year) +
    ease_aes('linear')

animate(animation, renderer = gifski_renderer("gganim.gif"))

anim_save("filenamehere.gif", anim)


# This plotly works for one year but I can't sort out the year filter
# p <- plot_ly(temp, color = I("gray80")) %>%
#     add_segments(x = ~Pos, xend = ~spend_rank, y = ~Team, yend = ~Team, showlegend = FALSE) %>%
#     add_markers(x = ~Pos, y = ~Team, name = "Pos", color = I("pink")) %>%
#     add_markers(x = ~spend_rank, y = ~Team, name = "spend_rank", color = I("blue")) %>%
#     layout(
#         title = "Gender earnings disparity",
#         xaxis = list(title = "Annual Salary (in thousands)"),
#         margin = list(l = 65)
#     )


## This changes the data each year, but doesn't change axis labels
# gg <- ggplot(data, aes(x=Pos, xend=spend_rank, y=Team, frame=year)) + 
#     geom_segment(aes(x=Pos, 
#                      xend=spend_rank, 
#                      y=Team, 
#                      yend=Team), 
#                  color="#b2b2b2", size=1.5)+
#     geom_dumbbell(color="red", 
#                   size_x=3.5, 
#                   size_xend = 3.5,
#                   #Note: there is no US:'color' for UK:'colour' 
#                   # in geom_dumbbel unlike standard geoms in ggplot()
#                   colour_x="#edae52", 
#                   colour_xend = "#9fb059")+
#     labs(x=NULL, y=NULL, 
#          title="Dumbbell Chart", 
#          subtitle="Spend vs. End of Season Rank")+
#     geom_text(color="black", size=2, hjust=-0.5,
#               aes(x=Pos, label=Pos))+
#     geom_text(aes(x=spend_rank, label=spend_rank), 
#               color="black", size=2, hjust=1.5)
# 
# ggplotly(gg)
