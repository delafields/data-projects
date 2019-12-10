# load dependencies
if (!require('openxlsx')) install.packages('openxlsx')
library('openxlsx')
if (!require('rvest')) install.packages('rvest')
library('rvest')

# base url of the data
base_url <- "https://www.nflpenalties.com/penalty/"

# url param
url_param <- "?year="

# penalty to be examined
current_penalty <- "neutral-zone-infraction"
current_penalty_yardage = 5


# create a list of the years we can get data for
#years = seq(2009, 2018)
years = c('2009','2010','2011','2012','2013',
          '2014','2015','2016','2017','2018')



scrape_penalties <- function (penalty, year, penalty_outcome) {
    
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
    
    penalty_df <- cbind(penalty_df, Penalty_Outcome=penalty_outcome)
    
    penalty_df <- as.data.frame(penalty_df)
    
    return(penalty_df)
}

#test <- scrape_penalties(current_penalty, 2018, 5)


create_workbook <- function(penalty, penalty_yardage) {
    
    file=paste(current_penalty, '.xlsx')
    
    # create a blank workbook
    wb <- createWorkbook()
    
    for (year in years){
        addWorksheet(wb, year)
    }
    
    for (year in years) {

        # scrape the table for this year
        temp <- scrape_penalties(penalty, year, penalty_yardage)
        
        # write to workbook
        writeData(wb, sheet=year, x=temp)
    }
    
    file_name = paste(penalty, '.xlsx')
    
    #saveWorkbook(wb, file=file_name)
    
    return(wb)
    
}

saveWorkbook(create_workbook(penalty = current_penalty, 
                             penalty_yardage = current_penalty_yardage),
             file=paste(current_penalty, '.xlsx'),
             overwrite = TRUE)
