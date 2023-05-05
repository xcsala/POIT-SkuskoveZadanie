
def parseArduinoData(inputData):
    inputData = inputData.decode("utf-8")
    inputData = inputData.strip()
    outputData = inputData.split(",")
    return outputData
