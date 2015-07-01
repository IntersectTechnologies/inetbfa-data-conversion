import os.path
import xl
import csv

def ExtractPrice(date, sourcepath, destpath, range):
    data = xl.Workbook(sourcepath)
    data.xlWorkbook.Sheets('PriceData').Activate()
    price = data.range(range).get()

    # Write price data to csv file for processing with R
    with open(destpath,'wb') as file:
        pricewriter = csv.writer(file, delimiter = ',')
        # Format heading
        heading = [p.replace("/", "").split(" ")[0] for p in price[0] if p!= None]
        heading.insert(0, "Date")
        pricewriter.writerow(heading)
        # skip a line and
        for p in price[2:]:
            pricewriter.writerow(p)

def ExtractPortfolio(date, sourcepath, destpath, range):
    data = xl.Workbook(sourcepath)
    data.xlWorkbook.Sheets('PortfolioData').Activate()
    portf = data.range(range).get()

    # Write price data to csv file for processing with R
    with open(destpath,'wb') as file:
        pricewriter = csv.writer(file, delimiter = ',')
        for p in portf:
            pricewriter.writerow(p)

def ExtractWeights(date, sourcepath, destpath, range):
    weights = GetWeights(sourcepath, range)  

    # Write weights data to csv for processing with R
    with open(destpath,'wb') as file:
        weightswriter = csv.writer(file, delimiter = ',')
        weightswriter.writerow(['Name','Code','Exchange', 'Currency', 'Proxy', 'Weight', 'Position'])
        for w in weights:
            if (w[4]!=0 and w[6]!=0):
                weightswriter.writerow([w[0], w[7], w[2], w[3], w[5], w[4]*w[6], w[6]])
            else:
                weightswriter.writerow([w[0], w[7], w[2], w[3], w[5], 0, w[6]])

# Helper function
def GetWeights(path, range):
    ''' 
    '''
    data = xl.Workbook(path)
    
    # Get data
    data.xlWorkbook.Sheets('Weights.Data').Activate()
    weights = data.range(range).get()  
    return weights