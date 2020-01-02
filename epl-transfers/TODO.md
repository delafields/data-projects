# TODOs

1. Make the call on whether to use RMD or a juypter notebook
2. Do I want to adjust for inflation? Thinking yes. Consider how to do this properly.
3. Create functions to..
    * Aggregate net sales by team
    * Grab number of transfers

## Overarching question and the primary thing being explored
* What teams got an unexpected injection of $? When did this happen? What was the result?

## Additional data points // some anecdotal things
* Who conducts the most loans?
    * This could be as simple as a well designed countplot.
* Who gets the most bang for their buck (spends the least and gets results)
    * Maybe plot little $'s onto how many points they got?
* How many transfers per win/point gained // how much was spent per win/point gained?
    * Can I reliably attribute points gained just to transfers for one year?

## Pure visualization
* Net transfer $ ranking vs. end of season ranking
    * Rankings are already baked into the scraped data, just need to join this to a function that calcs transfer $ rank
    * I'm thinking this can be a dot pair plot
        * I would love for this to be interactive, so the user can select the year and it can populate accordingly
        * Maybe do an "overall" one and average ranking? (Gonna have to rank 0 for relegated teams)
* How have transfer amounts changed per position year over year?
    * I'm thinking this can be a joy-plot in R.
    * Pretty simple to put together, just needs inflation adjustments.