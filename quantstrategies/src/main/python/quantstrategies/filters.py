import pandas as pd

def less_than_filter(data, threshold):
    return data[data < threshold].index
    
def greater_than_filter(data, threshold):
    return data[data >= threshold].index

def top_filter(data, n):
    data.sort(ascending = False)
    return data[0:n].index    
