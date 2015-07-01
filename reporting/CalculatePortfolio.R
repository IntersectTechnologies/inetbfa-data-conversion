# Copyright (c) 2012: DJ Swart
#

CalculatePortfolio <- function(tsdata, weights, name="portfolio") {
  # Calculate Portfolio time series from the constituents time series data and a vector of weights
  #
  # Args:
  #   data: Portfolio constituents' time series data
  #   weights: Portfolio weights

  # Returns:
  #   Portfolio and its time series - fPortfolio object and timeSeries
  #
  
  library('fPortfolio')
  
  mvSpec <- portfolioSpec()
  setWeights(mvSpec) <- weights
  
  portfolio <- feasiblePortfolio(data=tsdata, spec=mvSpec, constraints="Short")
  
  newts <- timeSeries(data=as.matrix(apply(tsdata%*%weights, 1, sum)), 
                      charvec=time(tsdata), units=name)

  return(list(portfolio = portfolio, timeseries = newts))
}