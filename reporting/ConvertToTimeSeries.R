# Copyright (c) 2012: DJ Swart
#
#

ConvertToTimeSeries <- function(data, symbols,  type="timeSeries") {
  # Converts the input data to a time series object, either xts, zoo or timeSeries
  #
  # Args:
  #
  #
  # Returns:
  #
  
  if (length(fields) > 3) stop("Too many data fields specified - requires
                               Datestamp, Symbol and a 'data' field - in that order")
  
  source('AsDate.R')
  if (type=="timeSeries") {
    library('timeSeries')
  }
  else if (type=="xts") {
    library('xts')
  }
  else if (type=="zoo") {
    library('zoo')
  }
  
  library("reshape")
  
  num <- length(symbols)
  
  # reshape data.frame
  rdata <- cast(data, Datestamp~Symbol, value="LogReturn")[,-(2:(2+num-1))]
  
  # Convert datestmaps to Date objects
  rdata$Datestamp <- AsDate(rdata$Datestamp)
    
  # select data from data.frame and add to timeSeries/zoo/xts object
  if (type=="timeSeries") {
  
    tsdata <- as.matrix(as.matrix(rdata[,-1]))
    time <- rdata[,1]

    ts <- timeSeries(data=tsdata, charvec=time, units=symbols) 
  }
  else if (type=="xts") {
    
  }
  else if (type=="zoo") {
    
  }
  else {
    stop("Unsopperted time series object format")
  }
  
  return(sort(ts))
}