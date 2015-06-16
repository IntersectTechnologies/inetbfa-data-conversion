# Copyright (c) 2012: DJ Swart
#


# Portfolio constituents
##############################

##############################
# SETTINGS:
#
# Benchmark:
benchmark <- 'J200'  # ALSI TOP 40 Index


# Load from file (csv)
filename <- 'Portfolio_20121002.csv'
pdata <- read.csv(filename, TRUE, sep=',', dec='.')

##############################################################################################
# Calculate Weights
long <- sum(pdata$Weight[pdata$InstrumentType=='Common Stock' | 
                    pdata$InstrumentType=='CASH' | pdata$InstrumentType=='ETF' & 
                    pdata$Weight >= 0])

short <- sum(pdata$Weight[pdata$Weight < 0])

longderiv <- sum(pdata$Weight[(pdata$InstrumentType=='CFD' | 
                                pdata$InstrumentType=='SSF') & pdata$Weight >= 0])

shortderiv <- sum(pdata$Weight[(pdata$InstrumentType=='CFD' | pdata$InstrumentType=='SSF')
                                  & pdata$Weight < 0] )

##############################################################################################
# Load instrument data from SQL database
fields <- c('Datestamp', 'Symbol', 'LogReturn')

# Instrument symbols
symbols <- pdata$Symbol[-52]
exchange <- pdata$Exchange[-52]
startdate <- 20090930
enddate <- 20121001

filter <- list(Symbols = symbols, exchange=exchange, StartDate = startdate, EndDate = enddate)

table <- "DailyReturns"

# Get data
retdata <- LoadFromSql(fields, table, filter)

# Convert to timeseries
library("reshape")

# reshape data.frame -- ooh-eh-eh!!!
instrumentdata.melt <- melt(retdata, id=c('Datestamp', 'Symbol'), measured=c('LogReturn'))
instrumentdata.cast <- cast(retdata.melt, ... ~ Symbol)[,-2]

# Convert datestamps to Date objects
instrumentdata.cast$Datestamp <- AsDate(instrumentdata.cast$Datestamp)

# select data from data.frame and add to timeSeries/zoo/xts object
instrument.matrix <- as.matrix(as.matrix(instrumentdata.cast[,-1]))
time <- instrumentdata.cast[,1]
instrument.ts <- timeSeries(data=instrument.matrix, charvec=time, units=names(instrumentdata.cast)[-1]) 

#############################################################################################
# Get benchmark data
symbols <- c(benchmark)
exchange <- c('JSE')
startdate <- 20090930
enddate <- 20121001

filter <- list(Symbols = symbols, exchange=exchange, StartDate = startdate, EndDate = enddate)
table <- "DailyReturns"

# Get data
benchmarkdata <- LoadFromSql(fields, table, filter)

benchmarkdata.melt <- melt(benchmarkdata, id=c('Datestamp', 'Symbol'), measured=c('LogReturn'))
benchmarkdata.cast <- cast(benchmarkdata.melt, ... ~ Symbol)[,-2]

# select data from data.frame and add to timeSeries/zoo/xts object
benchmark.matrix <- as.matrix(as.matrix(benchmarkdata.cast[,-1]))

# Convert datestamps to Date objects
benchmarkdata.cast$Datestamp <- AsDate(benchmarkdata.cast$Datestamp)
time <- benchmarkdata.cast[,1]

benchmark.ts <- timeSeries(data=benchmark.matrix, charvec=time, units=names(benchmarkdata.cast)[-1])

#####################################################################################################
# Clean data - Replace missing values (NA) with 0
benchmark.ts[is.na(benchmark.ts)] <- 0
instrument.ts[is.na(instrument.ts)] <- 0

combined.ts <- cbind(instrument.ts, benchmark.ts)
combined.ts[is.na(combined.ts)] <- 0

# Change sampling frequency


# Calculate Portfolio
pf <- CalculatePortfolio(tsdata=ts, weights=pdata$weight,name="BQCPortfolio" )

# Calculate correlations with Benchmark
correlationtable <- table.Correlation(instrument.ts, benchmark.ts)


