# read data data

root <- "E:/"
riskdata <- read.csv(paste(root, 'riskanalysis/data/riskdata_.csv', sep='/'))

dates <- riskdata['Date']
dates <- apply(dates,1, FUN = function(d) { substr(d,1,12) })
substr(dates, 5,5) <- '-'
substr(dates, 8, 8) <- '-'

benchmark <- riskdata['J203T']
benchmark.ts <- timeSeries(data=benchmark, charvec=dates)
portfolio.tr.ts <- timeSeries(data=riskdata['BQCGF_TR_Ret'], charvec=dates)

data <- riskdata[-1]
fints <- timeSeries(data=data, charvec=dates)

# Analysis - March excluded
startdate <- '2011-03-01'
enddate <- '2014-02-28'
inception <- '2011-05-30'
lastyear <- '2013-03-01'

rf <- 5.2/12

# 3 years
new.ts <- window(x=fints, start=startdate, end=enddate)
bench.ts <- window(x=benchmark.ts, start=startdate, end=enddate)

returns <- t(Return.annualized(new.ts, 12, geometric=FALSE))
alpha <- t(CAPM.alpha(new.ts, bench.ts, rf/100))
activeprem <- t(ActivePremium(Ra=new.ts, Rb=bench.ts, scale=12))

sd <- t(sd.annualized(x=new.ts, scale=12))
beta <- t(CAPM.beta(new.ts, bench.ts, rf/100))
trackerr <- t(TrackingError(Ra=new.ts, Rb=bench.ts, scale=12)) 
var <- t(VaR(R=new.ts, p=0.95, method='modified'))

sharpe <- t(SharpeRatio.annualized(R=new.ts, Rf=rf/100, scale=12, geometric=FALSE))
inforatio <- t(InformationRatio(Ra=new.ts, Rb=bench.ts, scale=12))

results <- data.frame(list(returns, alpha, activeprem, sd, beta, trackerr, var, sharpe, inforatio))
write.csv(results, file=paste(root, 'riskanalysis/results/20-03-2014_l3y.csv', sep='/'))

# Last 12 Months
new.ts <- window(x=fints, start=lastyear, end=enddate)
bench.ts <- window(x=benchmark.ts, start=startdate, end=enddate)

returns <- t(Return.annualized(new.ts, 12, geometric=FALSE))
alpha <- t(CAPM.alpha(new.ts, bench.ts, rf/100))
activeprem <- t(ActivePremium(Ra=new.ts, Rb=bench.ts, scale=12))

sd <- t(sd.annualized(x=new.ts, scale=12))
beta <- t(CAPM.beta(new.ts, bench.ts, rf/100))
trackerr <- t(TrackingError(Ra=new.ts, Rb=bench.ts, scale=12)) 
var <- t(VaR(R=new.ts, p=0.95, method='modified'))

sharpe <- t(SharpeRatio.annualized(R=new.ts, Rf=rf/100, scale=12, geometric=FALSE))
inforatio <- t(InformationRatio(Ra=new.ts, Rb=bench.ts, scale=12))

results <- data.frame(list(returns, alpha, activeprem, sd, beta, trackerr, var, sharpe, inforatio))
write.csv(results, file=paste(root, 'riskanalysis/results/20-03-2014_l12m.csv', sep='/'))

# Since inception
new.ts <- window(x=fints, start=inception, end=enddate)
bench.ts <- window(x=benchmark.ts, start=startdate, end=enddate)

returns <- t(Return.annualized(new.ts, 12, geometric=FALSE))
alpha <- t(CAPM.alpha(new.ts, bench.ts, rf/100))
activeprem <- t(ActivePremium(Ra=new.ts, Rb=bench.ts, scale=12))

sd <- t(sd.annualized(x=new.ts, scale=12))

beta <- t(CAPM.beta(new.ts, bench.ts, rf/100))
trackerr <- t(TrackingError(Ra=new.ts, Rb=bench.ts, scale=12)) 
var <- t(VaR(R=new.ts, p=0.95, method='modified'))

sharpe <- t(SharpeRatio.annualized(R=new.ts, Rf=rf/100, scale=12, geometric=FALSE))
inforatio <- t(InformationRatio(Ra=new.ts, Rb=bench.ts, scale=12))

results <- data.frame(list(returns, alpha, activeprem, sd, beta, trackerr, var, sharpe, inforatio))
write.csv(results, file=paste(root, 'riskanalysis/results/20-03-2014_si.csv', sep='/'))

# Correlation Matrix
write.csv(cor(new.ts,use='na.or.complete'), file=paste(root, 'riskanalysis/results/correlation.csv', sep='/'))
