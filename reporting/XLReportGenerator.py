import os.path
import os
import xl
import csv
import XLData
import RiskSummary
import CAPMSummary
import Correlation

reportdate = '2013-06-30'
startdate = '2010-06-01'
enddate = '2013-06-30'
lastyear = '2012-07-01'
inception = '2011-05-31'
rf = 5.15
 
dir = "D:\\Repos\\R\BlueQuadrantCapital"
report_path = os.path.join(dir, reportdate, 'Blue Quadrant Capital Risk Report ' + reportdate + '.xlsx')

weightsdata_source_path = os.path.join(dir, reportdate, "Portfolio.Weights.xlsx")
weightsdata_dest_path = os.path.join("D:\\Repos\\R\BlueQuadrantCapital", reportdate, 'weights.csv')

pricedata_source_path = os.path.join(dir, "PriceData.xlsx")
pricedata_dest_path = os.path.join(dir, reportdate, 'price.data.csv')

portfoliodata_source_path = "D:\\Repos\\R\BlueQuadrantCapital\\PortfolioData.xlsx"
portfoliodata_dest_path = os.path.join(dir, reportdate, 'portfolio.data.csv')

def main():
    report = xl.Workbook(report_path)
    
    weights_range = "A2:H74"
    weights = XLData.GetWeights(weightsdata_source_path, weights_range)
    XLData.ExtractWeights(reportdate, weightsdata_source_path, weightsdata_dest_path, weights_range)
    
    price_range = "A1:BX39"
    XLData.ExtractPrice(reportdate, pricedata_source_path, pricedata_dest_path, price_range)

    portf_range = "A1:C28"
    XLData.ExtractPortfolio(reportdate, portfoliodata_source_path, portfoliodata_dest_path, portf_range)

    # Run R Scripts with arguments
    os.system('Rscript.exe bin/main.R ' + reportdate + ' ' + startdate + ' ' + enddate + ' ' + lastyear + ' ' + inception + ' ' + str(rf))

    # Now Generate Excel report
    # #######################
    # Risk summary - since inception
    sheet = "Summary Since Inception"
    sourcedata = os.path.join(dir, reportdate, 'risksummary_si.csv')
    RiskSummary.GenerateReport(report, sheet, sourcedata, weights)

    # Risk summary - last 3 years
    sheet = "Summary Last 3 Years"
    sourcedata = os.path.join("D:\\Repos\\R\BlueQuadrantCapital", reportdate, 'risksummary_l3y.csv')
    RiskSummary.GenerateReport(report, sheet, sourcedata, weights)

    # Risk summary - last 12 months
    sheet = "Summary Last 12 Months"
    sourcedata = os.path.join(dir, reportdate, 'risksummary_l12m.csv')
    RiskSummary.GenerateReport(report, sheet, sourcedata, weights)

    # CAPM Metrics - since inception
    sheet = "CAPM Metrics Since Inception"
    sourcedata = os.path.join(dir, reportdate, 'CAPMMetrics_si.csv')
    CAPMSummary.GenerateReport(report, sheet, sourcedata, weights)

    # CAPM Metrics - Last 3 years
    sheet = "CAPM Metrics Last 3 Years"
    sourcedata = os.path.join(dir, reportdate, 'CAPMMetrics_l3y.csv')
    CAPMSummary.GenerateReport(report, sheet, sourcedata, weights)

    # Correlation Matrix
    sheet = "Correlation Matrix"
    source = os.path.join(dir, reportdate, 'correlation.csv')
    Correlation.GenerateReport(report, sheet, source)

    # Write Weights to report
    sheet = "WeightsData"
    source = os.path.join(dir, reportdate, 'weights.csv')
    #Correlation.GenerateReport(report, sheet, source)

if __name__ == '__main__': 
	main()
	input('Press any key to continue...')