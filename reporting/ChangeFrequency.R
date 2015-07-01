# Copyright (c) 2012: DJ Swart
#

ChangeFrequency <- function(tsdata, frequency="monthly", agg.fun=last) {
  # 
  # 
  # Args:
  #   tsdata: time series data that needs to be resampled
  #   frequency: the new data sampling frequency - sub sampling frequency
  #   agg.fun: The aggregation functio to use - default to last for price data
  #
  #
  # Returns:
  #
  #
  
  if (frequency=='monthly') {
    # Get the last day in the month
    by <- unique(timeLastDayInMonth(time(tsdata)))
    
  }
  else if (frequency=='quarterly') {
    # Get the last day in the month
    by <- unique(timeLastDayInQuarter(time(tsdata)))
  }
  
  # Aggregate returns between
  resampled <- aggregate(tsdata, by, FUN = agg.fun)
  
}