import csv, xl

class CAPM(object):
    ''' Class for '''

    def __init__(self, name, code, alpha, beta, beta_plus, beta_min, ann_alpha, trackerr, activeprem, informratio, treynor):
        self.Name = name
        self.Code = code
        self.Alpha = alpha
        self.Beta = beta
        self.Beta_Plus = beta_plus
        self.Beta_Min = beta_min
        self.AnnAlpha = ann_alpha
        self.TrackingError = trackerr
        self.ActivePremium = activeprem
        self.InformationRatio = informratio
        self.TreynorRatio = treynor

def GenerateReport(report, sheet, sourcedata, weights):

    ## CAPM Summary 
    capm=[]
    # extract data from csv file
    with open(sourcedata) as file:
        reader = csv.reader(file, delimiter = ',')
        for row in reader:
            if row[0] != '':
                code = row[0].split(" ")[0]
                wt = [w for w in weights if w[1] == code]
                if len(wt)>0:
                    capm.append(CAPM(wt[0][0], code, row[1], row[2], row[3], row[4], row[6], row[9], row[10], row[11], row[12]))
                else:
                    capm.append(CAPM(code, '', row[1], row[2], row[3], row[4], row[6], row[9], row[10], row[11], row[12]))
    
    report.xlWorkbook.Sheets(sheet).Activate()
    count = 3
    for m in capm:
        report.range("A" + str(count)).set(m.Name)
        report.range("B" + str(count)).set(m.Code)
        report.range("C" + str(count)).set(m.Alpha)
        report.range("D" + str(count)).set(m.Beta)
        report.range("E" + str(count)).set(m.Beta_Plus)
        report.range("F" + str(count)).set(m.Beta_Min)
        report.range("G" + str(count)).set(m.AnnAlpha)
        report.range("H" + str(count)).set(m.TrackingError)
        report.range("I" + str(count)).set(m.ActivePremium)
        report.range("J" + str(count)).set(m.InformationRatio)
        report.range("K" + str(count)).set(m.TreynorRatio)
        count += 1