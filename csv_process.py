import pandas as pd

'''
Update date: 2023.03.13
'''

class CsvProcess:
    def getDataFrame(self, csvData):
        data = pd.read_csv(csvData)
        return data