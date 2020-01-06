library(dplyr)
library(ggplot2)
library(stringr)
library(ggalt)
library(plotly)

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
    mutate(Team = str_replace_all(Team, " FC", "")) %>%
    mutate(Team = str_replace_all(Team, "AFC", "")) %>%
    mutate(Team = trimws(Team))

# convert results_data `year` to numeric for later joining
results_data <- results_data %>%
    mutate(year = as.numeric(year))

# join transfers to results
data <- results_data %>% left_join(grouped_transfer_data, by = c("Team", "year"))




###
# PLOTTING
###
temp <- data %>% filter(year == 2001)


p <- ggplot(data, aes(x=Pos, xend=spend_rank, y=Team)) + 
    geom_segment(aes(x=Pos, 
                     xend=spend_rank, 
                     y=Team, 
                     yend=Team), 
                 color="#b2b2b2", size=1.5)+
    geom_dumbbell(color="red", 
                  size_x=3.5, 
                  size_xend = 3.5,
                  #Note: there is no US:'color' for UK:'colour' 
                  # in geom_dumbbel unlike standard geoms in ggplot()
                  colour_x="#edae52", 
                  colour_xend = "#9fb059")+
    labs(x=NULL, y=NULL, 
         title="Dumbbell Chart", 
         subtitle="Spend vs. End of Season Rank")+
    geom_text(color="black", size=2, hjust=-0.5,
              aes(x=Pos, label=Pos))+
    geom_text(aes(x=spend_rank, label=spend_rank), 
              color="black", size=2, hjust=1.5)
p


p <- plot_ly(data, color = I("gray80")) %>%
    add_segments(x = ~Pos, xend = ~spend_rank, y = ~Team, yend = ~Team, showlegend = FALSE) %>%
    add_markers(x = ~Pos, y = ~Team, name = "Pos", color = I("pink")) %>%
    add_markers(x = ~spend_rank, y = ~Team, name = "spend_rank", color = I("blue")) %>%
    layout(
        title = "Gender earnings disparity",
        xaxis = list(title = "Annual Salary (in thousands)"),
        margin = list(l = 65)
    ) 

p


## temp
gg <- ggplot(data, aes(x=Pos, xend=spend_rank, y=Team, frame=year)) + 
    geom_segment(aes(x=Pos, 
                     xend=spend_rank, 
                     y=Team, 
                     yend=Team), 
                 color="#b2b2b2", size=1.5)+
    geom_dumbbell(color="red", 
                  size_x=3.5, 
                  size_xend = 3.5,
                  #Note: there is no US:'color' for UK:'colour' 
                  # in geom_dumbbel unlike standard geoms in ggplot()
                  colour_x="#edae52", 
                  colour_xend = "#9fb059")+
    labs(x=NULL, y=NULL, 
         title="Dumbbell Chart", 
         subtitle="Spend vs. End of Season Rank")+
    geom_text(color="black", size=2, hjust=-0.5,
              aes(x=Pos, label=Pos))+
    geom_text(aes(x=spend_rank, label=spend_rank), 
              color="black", size=2, hjust=1.5)

options(warn=1)
ggplotly(gg)

## temp not wokring
library("crosstalk")

newdata <- SharedData$new(data)

widgets <- bscols(
    #filter_select("year", "Year", newdata, ~year)
    #filter_slider("sales", "Sales", newdata, ~sales),
    filter_checkbox("year", "Years", newdata, ~year, inline = TRUE)
)
widgets

bscols(
    widths = c(4, 8), widgets, 
    plot_ly(data, color = I("gray80")) %>%
        add_segments(x = ~Pos, xend = ~spend_rank, y = ~Team, yend = ~Team, showlegend = FALSE) %>%
        add_markers(x = ~Pos, y = ~Team, name = "Pos", color = I("pink")) %>%
        add_markers(x = ~spend_rank, y = ~Team, name = "spend_rank", color = I("blue")) %>%
        layout(
            title = "Gender earnings disparity",
            xaxis = list(title = "Annual Salary (in thousands)"),
            margin = list(l = 65)
        ) 
)

## temp

tx <- highlight_key(data, ~year, "Select a city")

gg <- p
select <- highlight(
    ggplotly(gg, tooltip = "year"), 
    selectize = TRUE, persistent = TRUE
)

bscols(select)

## temp using ggplot dumbell
# see link below for moving labels and changing them
# https://stackoverflow.com/questions/58507077/gganimate-change-axes-between-frames
# this p is the first ggplot dumbell
p + transition_time(year) +
    labs(title = "Year: {frame_time}")

animation <- p +  
    labs(title = 'Year: {closest_state}', x = 'Top 5', y = 'Bottom 5') +
    transition_states(year) +
    ease_aes('linear')

animate(animation, renderer = gifski_renderer("gganim.gif"))

anim_save("filenamehere.gif", anim)
