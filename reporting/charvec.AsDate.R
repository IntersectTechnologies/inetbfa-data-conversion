# Copyright (c) 2012: DJ Swart
#
#
# Extract date

charvec.AsDate <- function (chardates) {
  
  datevec <- sapply(chardates, function(date) {
    return(paste(substr(date, 1, 4), substr(date,6,7), substr(date,9,10), sep="-"))
  })
return(as.Date(datevec))
}