import pandas as pd
from os import path, listdir

def data_summary_report(path, title):
    reportdata = {}

    with open(path, 'w') as report_html:
        report_header(report_html, title)
        report_convert(report_html)
        report_merge(report_html)
        
        report_html.write('</body>')
        report_html.write('</html>')

def report_header(htmlreport, title):
    htmlreport.write('<!DOCTYPE html>')
    htmlreport.write('<html>')
    htmlreport.write('<head>')
    htmlreport.write('<title>Data Report</title>')
    htmlreport.write('</head>')
    htmlreport.write('<body>')

def report_convert(htmlreport):
    reportdata = {}
    columns = ['startdate', 'enddate', 'number', 'comments']
    htmlreport.write('<h1>Conversion Report</h1>')
    for f in listdir(CONVERT_PATH):
        file = f
           
        htmlreport.write('<h3>' + f + '</h3>')
        data = load_ts(path.join(CONVERT_PATH, f))
        reportdata['startdate'] = [data[ticker].first_valid_index() for ticker in data.columns]
        reportdata['enddate'] = [data[ticker].last_valid_index() for ticker in data.columns]
        reportdata['number'] = [data[ticker].count() for ticker in data.columns]

        report = pd.DataFrame(reportdata, index = data.columns, columns = columns)
        htmlreport.write('<div>' + report.to_html() + '</div>')

def report_merge(htmlreport):
    reportdata = {}
    columns = ['startdate', 'enddate', 'number', 'comments']
    htmlreport.write('<h1>Merge Report</h1>')
    for f in listdir(MERGED_PATH):
        file = f
           
        htmlreport.write('<h3>' + f + '</h3>')
        data = load_ts(path.join(MERGED_PATH, f))
            
        reportdata['startdate'] = [data[ticker].first_valid_index() for ticker in data.columns]
        reportdata['enddate'] = [data[ticker].last_valid_index() for ticker in data.columns]
        reportdata['number'] = [data[ticker].count() for ticker in data.columns]

        report = pd.DataFrame(reportdata, index = data.columns, columns = columns)
        htmlreport.write('<div>' + report.to_html() + '</div>')