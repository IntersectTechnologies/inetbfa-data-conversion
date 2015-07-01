# Copyright (c) 2012: DJ Swart
#
#

RiskSummary <- function(timeseries, Rb, Rf=0, scale=12, geometric=FALSE, p=0.95) {
  #
  #
  #
  #
  
  
  # Calculate Annualized Returns
  ann.ret <- t(Return.annualized(timeseries, scale=scale, geometric=geometric));
  
  # Calculate Annualized standard deviation
  ann.stddev <- t(StdDev.annualized(timeseries, scale=scale))
               
  # Calculate Sharpe Ratio
  ann.sharpe <- t(SharpeRatio.annualized(timeseries, Rf=Rf, scale=scale, geometric=geometric))
  
  # Calculate Sortino Ratio
  sortino <- t(SortinoRatio(timeseries, Rb))
  
  # Calculate beta
  beta <- t(CAPM.beta(timeseries, Rb=Rb, Rf=Rf))
  
  # Calculate historic VaR
  var.hist <- t(VaR(timeseries, p=p, method="historical"))
  
  # Calculate gaussian VaR
  var.gauss <- t(VaR(timeseries, p=p, method="gaussian"))

  # Calculate Cornish-Fisher VaR
  var.cf <- t(VaR(timeseries, p=p, method="modified"))
  
  df <- data.frame(ann.ret, ann.stddev, ann.sharpe, sortino, beta, var.hist, var.gauss, var.cf)
  
  return(df)
}