# Copyright (c) 2012: DJ Swart
#
#

AdjustForStockSplits <- function(pricedata) {
  #
  
  # 
  
  numcols <- length(pricedata[1,])
  numrows <- length(pricedata[,1])
  splitidx <- matrix(NA, 1, 2)
  a <- 1
  
  for (i in 1:numcols) {
    for (k in 1:(numrows-1)) {
      ratio <- round(as.numeric(pricedata[k+1, i])/as.numeric(pricedata[k, i]), 1)
      if (ratio < 0.5  & !is.na(ratio)) {
        
        splitidx <- rbind(splitidx, c(k, i))
        a <- a+1
        
        for (q in 1:splitidx[2]) {
          pricedata[q, i] <- pricedata[q, i]*ratio;
        }
        
      }
    }
  }
  return(list(data=pricedata, splits=splitidx))
  
}