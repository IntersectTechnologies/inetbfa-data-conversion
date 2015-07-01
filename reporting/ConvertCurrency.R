# Copyright (c) 2012: DJ Swart
#
#

ConvertCurrency <- function(pricedata, forexdata) {
  #
  #
  #
  #
  
  if (length(pricedata[,1])!=length(forexdata[,1])) {
    stop("Column vectors not of same length")
  }
  
  numcols <- length(pricedata[1,])
  
  returndata <- pricedata[,1]*forexdata[,1]
  
  if (numcols > 1) {
    for (i in 2:numcols) {
      returndata <- cbind(returndata, pricedata[,i]*forexdata[,1])
      
    }
  }
  
  names(returndata) <- sapply(names(returndata),FUN=paste, 'ZAR', sep='.')
  
  return(returndata)
}