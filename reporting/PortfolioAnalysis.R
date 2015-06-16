# Copyright (c) 2012: DJ Swart
#
# 
########################################
# Portfolio Analysis
########################################

# Calculate returns in Rand
dollar.denom <- as.character(pdata[pdata$Exchange!='JSE' & pdata$Market!='FOREX' & 
                  !(pdata$InstrumentType=='Call Option' | pdata$InstrumentType=='Put Option'),]$Symbol)
 
dollar.denom <- dollar.denom[-which(dollar.denom=='DNO' | dollar.denom=='NLR')]
monthlyprice.zar.ts <- ConvertCurrency(monthlyprice.ts[, dollar.denom], forexmonthly.ts)

# Combine
monthlyprice.ts <- cbind(monthlyprice.ts, monthlyprice.zar.ts, forexmonthly.ts)

# leave instruments with incomplete data out
missingData <- as.integer(levels(as.factor(which(is.na(monthlyprice.ts), arr.ind=TRUE)[,2])))
monthlyreturns.ts <- returns(monthlyprice.ts[, -missingData])

monthlyreturns.missing.ts <- cbind(returns(monthlyprice.ts[, 'STNG.ZAR']), returns(monthlyprice.ts[, 'CLR']), 
                                   returns(monthlyprice.ts[, 'GM.ZAR']), returns(monthlyprice.ts[, 'MPC.ZAR']), 
                                   returns(monthlyprice.ts[, 'PSX.ZAR']), returns(monthlyprice.ts[, 'TCP']))

KAB <- monthlyreturns.ts[,'AFR']
names(KAB) <- 'KAAP.AGRI'
monthlyreturns.ts <- cbind(monthlyreturns.ts, KAB)


