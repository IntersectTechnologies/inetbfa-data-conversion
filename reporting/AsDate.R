# Copyright (c) 2012: DJ Swart
#

AsDate <- function(dates) {
  # Convert date data in integer form to Date object
  #
  # Args:
  #   dates: integer vector representing dates in the form yyyymmdd
  #
  # Returns:
  #   A vector of Date objects
  
  datevec<-sapply(dates, function(date) {
                            return(paste(substr(date, 1, 4), substr(date,5,6), substr(date,7,8), sep="-"))
                        })
  return(as.Date(datevec))
}
