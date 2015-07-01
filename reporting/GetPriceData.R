# Copyright (c) 2012: DJ Swart
#

# Get Price Data

##############################################################################################
# INPUT:
#

# DATA:
# filename
# tablename
# fields
# startdate
# enddate
# benchmark
# risk-free rate
# outputfrequency
# filename for portfolio historical returns

input <- list(filename='InputData/Portfolio_20121002.csv', fields=c('Datestamp', 'Symbol', 'PriceClose'), 
              table="DailyReturns", startdate=20090930, enddate=20121001 )

GetInstrumentData <- function(input) {
  #
  #
  #
  #
  
  # Convert to timeseries
  library("reshape")
  
  pdata <- read.csv(input$filename, TRUE, sep=',', dec='.')
  
  # Instrument symbols
  symbols <- pdata[pdata$Symbol!='KAAP.AGRI' & pdata$Symbol!='KWV' & pdata$Market!='FOREX' & 
    !(pdata$InstrumentType=='Call Option' | pdata$InstrumentType=='Put Option' | pdata$InstrumentType=='Warrant'),]$Symbol
  
  exchange <- pdata[pdata$Symbol!='KAAP.AGRI' & pdata$Symbol!='KWV' & pdata$Market!='FOREX' & 
    !(pdata$InstrumentType=='Call Option' | pdata$InstrumentType=='Put Option' | 
    pdata$InstrumentType=='Warrant'),]$Exchange
  
  filter <- list(Symbols = symbols, exchange=exchange, StartDate = input$startdate, EndDate = input$enddate)
    
  # Get data
  pricedata <- LoadFromSql(input$fields, input$table, filter)
  
  # reshape data.frame 
  instrumentdata.melt <- melt(pricedata, id=c('Datestamp', 'Symbol'), measured=c('PriceClose'))
  instrumentdata.cast <- cast(instrumentdata.melt, ... ~ Symbol)[,-2]
  
  # Convert datestamps to Date objects
  instrumentdata.cast$Datestamp <- AsDate(instrumentdata.cast$Datestamp)
  
  instrument.matrix <- as.matrix(as.matrix(instrumentdata.cast[,-1]))
  time <- instrumentdata.cast[,1]
  instrument.ts <- timeSeries(data=instrument.matrix, charvec=time, units=names(instrumentdata.cast)[-1])
}

#############################################################################################

GetBenchmarkData <- function() {
  # Get benchmark data
  symbols <- c(benchmark)
  exchange <- c('JSE')
  startdate <- 20090930
  enddate <- 20121001
  
  filter <- list(Symbols = symbols, exchange=exchange, StartDate = startdate, EndDate = enddate)
  table <- "DailyReturns"
  
  # Get data
  benchmarkdata <- LoadFromSql(fields, table, filter)
  
  benchmarkdata.melt <- melt(benchmarkdata, id=c('Datestamp', 'Symbol'), measured=c('PriceClose'))
  benchmarkdata.cast <- cast(benchmarkdata.melt, ... ~ Symbol)[,-2]
  
  benchmark.matrix <- as.matrix(as.matrix(benchmarkdata.cast[,-1]))
  
  # Convert datestamps to Date objects
  benchmarkdata.cast$Datestamp <- AsDate(benchmarkdata.cast$Datestamp)
  time <- benchmarkdata.cast[,1]
  
  benchmark.ts <- timeSeries(data=benchmark.matrix, charvec=time, units=names(benchmarkdata.cast)[-1])
}


##########################################################################################
# Get ZARUSD rates

GetForexData <- function() {
  #
  #
  #
  
  filter <- list(Symbols = 'ZARUSD', exchange='OTC', StartDate = startdate, EndDate = enddate)
  
  fields <- c('Datestamp', 'Symbol', 'IndexClose')
  forex <- LoadFromSql(fields, "DailyPrice", filter)
  
  forex.melt <- melt(forex, id=c('Datestamp', 'Symbol'), measured=c('PriceClose'))
  forex.cast <- cast(forex.melt, ... ~ Symbol)[,-2]
  
  forex.matrix <- as.matrix(as.matrix(forex.cast[,-1]))
  
  # Convert datestamps to Date objects
  forex.cast$Datestamp <- AsDate(forex.cast$Datestamp)
  time <- forex.cast[,1]
  
  forex.ts <- timeSeries(data=forex.matrix, charvec=time, units=names(forex.cast)[-1])
  forexmonthly.ts <- ChangeFrequency(forex.ts, frequency='monthly', agg.fun=last)
}

###########################################################################################
# Clean data - Replace missing values (NA) with 0
# benchmark.ts[is.na(benchmark.ts)] <- 0
# instrument.ts[is.na(instrument.ts)] <- 0

CleanData <- function() {
  #
  #
  #
  
  combined.ts <- cbind(instrument.ts, benchmark.ts)
  # combined.ts[is.na(combined.ts)] <- 0
  
  result <- ApplyZOH(combined.ts)
  dailyprice.ts <- result$data
  missingData <- result$NACols;
  
  # Adjust for stock splits
  dailyprice.ts <- AdjustForStockSplits(dailyprice.ts)$data
  
  monthlyprice.ts <- ChangeFrequency(dailyprice.ts, frequency='monthly', agg.fun=last)
}



# Get the risk-free rate
############################################################################################

GetRiskfreeData <- function() {
  #
  #
  #
  
  tbill <- read.csv('InputData/TBILL_3Month.csv')
  ttime <- charvec.AsDate(as.character(tbill$Time.Period))
  TBill.ts <- timeSeries(data=tbill$RIFSGFSM03_N.B, charvec=ttime, units='TBILL.3Month')
  rfrate.monthly <- as.numeric(mean.geometric(window(TBill.ts, start='2009-09-30', end='2012-10-01'))/12)
  rfrate.ann <- as.numeric(mean.geometric(window(TBill.ts, start='2009-09-30', end='2012-10-01')))
}



# Load Historic Portfolio Returns
############################################################################################

GetPortfolioData <- function() {
  #
  portfoliodata <- read.csv('InputData/BQCG_Growth_returns.csv', sep=",", dec='.')
  
  ptime <- charvec.AsDate(as.character(portfoliodata$Date))
  portfolionav.ts <- timeSeries(data=portfoliodata$NAV, charvec=ptime, units='BQCGrowth')
  portfolioreturns.ts <- returns(portfolionav.ts)
}

