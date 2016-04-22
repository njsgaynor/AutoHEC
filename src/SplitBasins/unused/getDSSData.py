from src.SplitBasins.unused.DSSDataDict_class import DSSDataDict

def getDSSData(pathNames, dssFile):
    dataDict = DSSDataDict()
    for item in range(len(pathNames)):
        dataFromFile = dssFile.get(pathNames[item], True)
        dataDict.add({pathNames[item], dataFromFile.values})
    return dataDict