import csv, xl

class RiskSummary(object):
    '''Class for a risk summary of an instrument'''

    # Constructor
    def __init__(self, name, code, ret, sd, sharpe, sortino, beta, var_h, var_g, var_cf):
        self.Name = name
        self.Code = code
        self.Returns = ret
        self.StdDev = sd
        self.SharpeRatio = sharpe
        self.SortinoRatio = sortino
        self.Beta = beta
        self.HistoricVaR = var_h
        self.GaussianVaR = var_g
        self.CornishFisherVaR = var_cf    

def GenerateReport(report, sheet, sourcedata, weights):

    ## Risk Summary - Since Inception
    rsi=[]
    # extract data from csv file
    with open(sourcedata) as file:
        reader = csv.reader(file, delimiter = ',')
        for row in reader:
            if row[0] != '':
                wt = [w for w in weights if w[1] == row[0]]
                if len(wt)>0:
                    rsi.append(RiskSummary(wt[0][0], row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))
                else:
                    rsi.append(RiskSummary(row[0], '', row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))

    report.xlWorkbook.Sheets(sheet).Activate()
    count = 4
    for rs in rsi:
        report.range("A" + str(count)).set(rs.Name)
        report.range("B" + str(count)).set(rs.Code)
        report.range("C" + str(count)).set(rs.Returns)
        report.range("D" + str(count)).set(rs.StdDev)
        report.range("E" + str(count)).set(rs.SharpeRatio)
        report.range("F" + str(count)).set(rs.SortinoRatio)
        report.range("G" + str(count)).set(rs.Beta)
        report.range("H" + str(count)).set(rs.CornishFisherVaR)
        count += 1

    