parseJsonPortfolio <- function(portfdata) {
  
  docid <- portfdata$id
  docrev <- portfdata$value$'_rev'
  portfolio <- portfdata$value
  
  # basic info
  name <- portfolio$name
  benchmark$ticker <- portfolio$benchmark_id
  benchmark$exchange <- portfolio$benchmark_exchange
  
  # portfolio timeseries
  pfmat <- t(sapply(portfolio$timeseries$data, function(ts) { 
    return(list(as.character(ts['date']), as.numeric(ts['value'])))
  }));
  
  pfts <- timeSeries(sapply(pfmat[,2], function(d) { return(d)}), charvec=pfmat[,1])
  names(pfts) <- portfolio$timeseries$header[[2]]
  
  # portfolio investments
  investments <- portfolio$investments
  inv <- sapply(investments, function(i) { return(list(i$asset$name, i$asset$ticker, i$asset$exchange, i$asset$currency, as.numeric(i$exposure), i$weight)) })
  invdata <- as.data.frame(t(inv))
  names(invdata) <- c("name", "ticker", "exchange", "currency", "exposure", "weight")
  
  return(id=docid, rev=docrev, name=name, ts=pfts, investments=invdata, benchmark=benchmark)
}