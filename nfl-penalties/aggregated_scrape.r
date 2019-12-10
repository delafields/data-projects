# load dependencies
if (!require('openxlsx')) install.packages('openxlsx')
library('openxlsx')
if (!require('rvest')) install.packages('rvest')
library('rvest')


scrape_penalties_aggregated <- function (penalty, year, penalty_outcome) {
    
    # full url
    full_url = paste(base_url, penalty, url_param, year, sep="")
    
    # get the html
    data <- read_html(full_url)
    
    # get the table data
    table <- data %>%
        html_node("table") %>%
        html_table()
    
    temp <- as.matrix(table)
    
    colnames(temp) = temp[1, ] # the first row will be the header
    penalty_df = temp[-1, ]          # removing the first row.
    penalty_df <- penalty_df[, 1:7]        # select only 'Against' columns
    
    penalty_df <- cbind(penalty_df, Penalty_Outcome=penalty_outcome, Year=year)
    
    return(penalty_df)
}

# check if it works
#test <- scrape_penalties(current_penalty, 2018, 5)


create_workbook_aggregated <- function(penalty, penalty_yardage) {
    
    file=paste(current_penalty, '.xlsx')
    
    # create a blank workbook
    wb <- createWorkbook()
    
    addWorksheet(wb, penalty)
    
    agg_matrix <- matrix(, nrow = 0, ncol = 9)
    
    for (year in years) {
        
        # scrape the table for this year
        temp <- scrape_penalties_aggregated(penalty, year, penalty_yardage)
        
        agg_matrix <- rbind(agg_matrix, temp)

    }
    
    # write to workbook
    writeData(wb, sheet=penalty, x=agg_matrix)
    
    file_name = paste(penalty, '.xlsx')
    
    return(wb)
    
}

get_penalty_yardage <- function(penalty) {
    if (penalty) {
        return('')
    }
}

# base url of the penalty data
base_url <- "https://www.nflpenalties.com/penalty/"

# url param
url_param <- "?year="

# penalty to be examined
current_penalty <- "neutral-zone-infraction"
current_penalty_yardage = 5


# create a list of the years we can get data for
years = c('2009','2010','2011','2012','2013',
          '2014','2015','2016','2017','2018')



saveWorkbook(create_workbook_aggregated(penalty = current_penalty, 
                             penalty_yardage = current_penalty_yardage),
             file=paste(current_penalty, '.xlsx'),
             overwrite = TRUE)