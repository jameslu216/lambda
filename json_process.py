import json
from pathlib import Path

import pandas as pd

'''
Update date: 2023.05.03
'''

class JsonProcess:
    def __init__(self, vector2Regex = r"X:|Y:|,Z:.*", vector3Regex = r"X:|Y:|Z:", vector4Regex = r"X:|Y:|Z:|W:") -> None:
        self.jsonRegex = r"[\{\}\' ]"
        self.vector2Regex = vector2Regex
        self.vector3Regex = vector3Regex
        self.vector4Regex = vector4Regex

        return

    def findDataPath(self, folder, dataName):
        fd = Path(folder)
        if fd.exists():
            dataPath = list(fd.rglob(f'*{dataName}.json'))[0]
        else:
            print(f"ERROR: folder {folder} not exist")
            dataPath = ""
        return dataPath

    def readJson(self, dataPath):
        jsonFile = open(dataPath, encoding="utf-8")
        jsonData = json.load(jsonFile)    
        jsonFile.close()
        return jsonData

    def getDataFrame(self, jsonData, dataListName):
        data = pd.DataFrame.from_dict(jsonData[dataListName])
        return data

    def readJsonDataFrame(self, data_folder, dataName):
        dataPath = self.findDataPath(data_folder, dataName)
        jsonData = self.readJson(dataPath)
        data = self.getDataFrame(jsonData, dataName)
        return data    

    def removeChar(self, seriesData, regex):
        seriesData = seriesData.astype("string")    
        seriesData = seriesData.str.replace(regex, "", regex=True)   

        return seriesData    

    def splitToVector2(self, vector2Series):
        vector2Series = self.removeChar(vector2Series, self.jsonRegex)
        vector2Series = self.removeChar(vector2Series, self.vector2Regex)
        df = vector2Series.str.split(",", expand=True)
        df.columns = [f"{vector2Series.name}_X", f"{vector2Series.name}_Y"]
        df = df.astype("float")
        return df

    def splitToVector3(self, vector3Series):
        vector3Series = self.removeChar(vector3Series, self.jsonRegex)
        vector3Series = self.removeChar(vector3Series, self.vector3Regex)
        df = vector3Series.str.split(",", expand=True)
        df.columns = [f"{vector3Series.name}_X", f"{vector3Series.name}_Y", f"{vector3Series.name}_Z"]
        df = df.astype("float")
        return df

    def splitToVector4(self, vector4Series):
        vector4Series = self.removeChar(vector4Series, self.jsonRegex)
        vector4Series = self.removeChar(vector4Series, self.vector4Regex)
        df = vector4Series.str.split(",", expand=True)
        df.columns = [f"{vector4Series.name}_X", f"{vector4Series.name}_Y", f"{vector4Series.name}_Z", f"{vector4Series.name}_W"]
        df = df.astype("float")
        return df

    def getStage(self, globalDataSeries):
        stageRegex = r"\\'_stage': +"
        globalDataSeries = self.removeChar(globalDataSeries, self.jsonRegex)
        cleanStageData = globalDataSeries.str.extract(r"(?P<drop>_stage:)(?P<stage>[A-Za-z]+)")
        cleanStageData.drop(["drop"], axis=1, inplace=True)
        return cleanStageData