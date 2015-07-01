import csv, xl

class Correlation(object):

    def __init__(self, code, correlations):
        self.Code = code
        self.Correlation = correlations

def GenerateReport(report, sheet, source):
    cor=[]
    # extract data from csv file
    with open(source) as file:
        reader = csv.reader(file, delimiter = ',')
        for row in reader:
            correlations = {}
            if row[0] == '':
                keys = row[1:]
            else:
                i=1
                # fill dictionary
                for k in keys:
                    correlations[k] = row[i]
                    i+=1
                cor.append(Correlation(row[0],correlations))

    report.xlWorkbook.Sheets(sheet).Activate()
    row = 2
    col = 1
    for c in cor:
        if row == 2:
            for k in keys:
                report.range(xlcol(col)  + str(2)).set(k)
                col += 1
            row += 1
            col = 1
        for k in keys:
            report.range("A" + str(row)).set(c.Code)
            report.range(xlcol(col) + str(row)).set(c.Correlation[k])
            col += 1
        row += 1
        col = 1
       

def xlcol(colnum):
    if colnum <= 25:
        if colnum == 0:
            return chr(65)
        else:
            return chr(65+colnum)
    else:
        mult = colnum/26
        return xlcol(mult-1) + xlcol(colnum%26)
