# Copyright (c) 2012: DJ Swart
#

GenerateResults <- function(filename, dataset, portfolioname="Portfolio") {
  
  analysis <- read.csv('InputData/Analysis_selection.csv', TRUE, sep=',', dec='.')
  
  symb_select <- as.character(analysis$Symbol)
  weight_select <- analysis$Weight
  
  pf <- CalculatePortfolio(tsdata=monthlyreturns.ts[-37, symb_select], weights=weight_select, name="BQCPortfolio" )
  
}

write.csv(pf$portfolio@portfolio@portfolio$covRiskBudgets, file='Results/RiskAttribution.csv')
write.csv(cbind(pf$portfolio@data@statistics$mean, pf$portfolio@portfolio@portfolio$weights), file='Results/ReturnAttribution.csv')


#############################################################################
# 
#

write.csv(table.Correlation(monthlyreturns.ts[,symb_select], monthlyreturns.ts[,'J200']), file='Results/correlations.csv')

# Calculate CAPM values
write.csv(table.CAPM(monthlyreturns.ts[,symb_select], monthlyreturns.ts[,'J200'], scale=12, Rf=rfrate.monthly/100, digits=3), file='Results/CAPM.csv')

write.csv(CAPM.beta(monthlyreturns.missing.ts, monthlyreturns.ts[,'J200'], Rf=rfrate.monthly/100), file='Results/CAPM_missing.csv')


# Get Calendar returns
table.CalendarReturns(monthlyreturns.ts[,symb_select], digits=3, as.perc=TRUE, geometric=FALSE)

# Portfolio Realized return
table.AnnualizedReturns(portfolioreturns.ts, scale=12, Rf=rfrate.monthly/100, geometric=FALSE, digits=3)

# Benchmark realized return
table.AnnualizedReturns(monthlyreturns.ts[, 'J200'], scale=12, Rf=rfrate.monthly/100, geometric=FALSE, digits=3)

# Missing data
write.csv(table.AnnualizedReturns(monthlyreturns.missing.ts, scale=12, Rf=rfrate.monthly/100, geometric=FALSE, digits=3), file='Results/AnnualizedRet_missing.csv')


# Portfolio Beta
CAPM.beta(portfolioreturns.ts, Rb=monthlyreturns.ts[,'J200'],  Rf=rfrate.monthly/100)

# Instrument Level Analysis
###########################################################################

# Calculate Annualized Return
write.csv(table.AnnualizedReturns(monthlyreturns.ts[,symb_select], scale=12, Rf=rfrate.monthly/100, digits=3, geometric=FALSE), file='Results/summary.csv')

# Calculate Betas
write.csv(CAPM.beta(monthlyreturns.ts[,symb_select], Rb=monthlyreturns.ts[,'J200'],  Rf=rfrate.monthly/100), file='Results/beta.csv')