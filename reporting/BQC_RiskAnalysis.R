# Copyright (c) 2012: DJ Swart
#
# 
########################################
# BQC - Portfolio Risk Analysis
########################################

library("PerformanceAnalytics")
library("timeSeries")

# Get Data from file
return.data <- read.csv(file="Data/2012-11-30/returns.csv")

# Convert to timeseries
return.data[,"Date"] <- charvec.AsDate(return.data$Date)
return.matrix <- as.matrix(as.matrix(return.data[,-1]))
time <- return.data[,1]
return.ts <- timeSeries(data=return.matrix, charvec=time, units=names(return.data)[-1]) 

# Get weights
w <- read.csv(file="Data/2012-11-30/weights.csv")

# Create Portfolio
pw <- c(w$KAAP.AGRI.BEDRYF, 
        w$KWV.HOLDINGS, 
        w$SENWES, 
        w$GRANDPARADE, 
        w$YORK.TIMBER, 
        w$DIGICORE, 
        w$SOV.FOODS, 
        w$COUNTRY.BIRD, 
        w$KELLY.GROUP, 
        w$GREAT.BASIN, 
        w$AFGRI, 
        w$CLOVER, 
        w$ILLOVO, 
        w$ASTRAL, 
        w$GOLDFIELDS, 
        w$ANGLOGOLD, 
        w$CMH, 
        w$TONGAAT, 
        w$BLUE.LABEL, 
        w$HCI, 
        w$SATRIX.40, 
        w$ZGOVI, 
        w$RESILIENT, 
        w$TRANS.CAP, 
        w$ARM, 
        w$ABL,
        w$WHL, 
        w$CAPITEC, 
        w$ASSORE, 
        w$USD.ZAR,
        w$SCORPIO.TANKERS, 
        w$CONTANGO, 
        w$FUSION.IO, 
        w$UNIVERSAL.FOREST, 
        w$GREENBRIER.COMPANIES,
        w$PHILLIPS.66,
        w$HESS, 
        w$ETE, 
        w$NRG, 
        w$NATIONAL.FUEL.GAS.CO, 
        w$FORD, 
        w$FORD.1, 
        w$GENERAL.MOTORS, 
        w$GENERAL.MOTORS.1,
        w$SOUTHWEST, 
        w$REGIONS.FINANCIAL,
        w$EPV, 
        w$PIN)

tsv <- c("AFR",
         "DST", 
         "Sen",
         "GPL", 
         "YRK", 
         "DGC", 
         "SOV", 
         "CBH", 
         "KEL", 
         "GBG", 
         "AFR", 
         "CLR", 
         "ILV", 
         "ARL", 
         "GFI", 
         "ANG", 
         "CMH", 
         "TON", 
         "BLU", 
         "HCI", 
         "STX40",
         "ZGOVI", 
         "RES", 
         "TCP", 
         "ARI", 
         "ABL", 
         "WHL", 
         "CPI", 
         "ASR",
         "ZAR.USD",
         "STNG.ZAR", 
         "MCF.ZAR", 
         "FIO.ZAR", 
         "UFPI.ZAR", 
         "GBX.ZAR",
         "PSX.ZAR", 
         "HES.ZAR", 
         "ETE.ZAR", 
         "NRG.ZAR", 
         "NFG.ZAR", 
         "F.ZAR", 
         "F.ZAR", 
         "GM.ZAR", 
         "GM.ZAR", 
         "LUV.ZAR",
         "RF.ZAR",
         "EPV.ZAR",  
         "PIN.ZAR") 

p <- CalculatePortfolio(tsdata=return.ts[,tsv], weights=pw, name="Portfolio.Hist")
write.csv(p$timeseries, file="Data/2012-11-30/weightedreturns.csv")
analysis.ts <- cbind(return.ts[,c("Portfolio..BQCGF.", "Benchmark.J203T.", tsv)], p$timeseries)

# Get data sets
sinceinception.ts <- window(analysis.ts, start="2011-05-31", end="2012-11-30")
last12months.ts <- window(analysis.ts, start="2011-12-01", end="2012-11-30")
last3years.ts <- analysis.ts[,-1]

# Get risk-free rate
# tbill <- read.csv('InputData/TBILL_3M_monthly.csv')
# l <- length(tbill[,1])
# sinceinception.rf <- as.numeric(mean.geometric(tbill[(l-16):l,2]))/12
# last12months.rf <- as.numeric(mean.geometric(tbill[(l-11):l,2]))/12
# last3years.rf <- as.numeric(mean.geometric(tbill[(l-35):l,2]))/12 

# Use JIBAR as at 30 Nov 2012
rf <- 5.125/12

#################################################################################
# Calculate Portfolio Metrics
#################################################################################

# Last 3 years
write.csv(t(table.CAPM(last3years.ts[, -1], last3years.ts[,"Benchmark.J203T."], scale=12, Rf=rf/100, digits=3)), 
          file="Results/2012-11-30/CAPMMetrics_l3y.csv")

write.csv(RiskSummary(last3years.ts, Rb=last3years.ts[,"Benchmark.J203T."], Rf=rf/100, scale=12, geometric=FALSE, p=0.95),
          file="Results/2012-11-30/risksummary_l3y.csv")

write.csv(cor(last3years.ts), file="Results/2012-11-30/correlation_l3y.csv")

# Last 12 Months
write.csv(t(table.CAPM(last12months.ts[, -2], last12months.ts[,"Benchmark.J203T."], scale=12, Rf=rf/100, digits=3)), 
          file="Results/2012-11-30/CAPMMetrics_l12m.csv")

write.csv(RiskSummary(last12months.ts, Rb=last12months.ts[,"Benchmark.J203T."], Rf=rf/100, scale=12, geometric=FALSE, p=0.95),
          file="Results/2012-11-30/risksummary_l12m.csv")

write.csv(cor(last12months.ts), file="Results/2012-11-30/correlation_L12M.csv")

# Since Inception
write.csv(t(table.CAPM(sinceinception.ts[, -2], sinceinception.ts[,"Benchmark.J203T."], scale=12, Rf=rf/100, digits=3)), 
          file="Results/2012-11-30/CAPMMetrics_si.csv")

write.csv(RiskSummary(sinceinception.ts, Rb=sinceinception.ts[,"Benchmark.J203T."], Rf=rf/100, scale=12, geometric=FALSE, p=0.95),
          file="Results/2012-11-30/risksummary_si.csv")

write.csv(cor(sinceinception.ts), file="Results/2012-11-30/correlation_si.csv")


