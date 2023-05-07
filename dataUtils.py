
def parseArduinoData(inputData):
    inputData = inputData.decode("utf-8")
    inputData = inputData.strip()
    outputData = inputData.split(",")
    return outputData

def parseDatabaseData(inputData):
    x = []
    temperature = []
    humidity = []
    chars_to_remove = r'[]{}" '

    translation_table = str.maketrans("", "", chars_to_remove)

    data = inputData.translate(translation_table)
    
    data = data.split(",")
    
    for element in data:
        element = element.split(":")
        if element[0] == "x":
            x.append(float(element[1]))
        elif element[0] == "humidity":
            humidity.append(float(element[1]))
        elif element[0] == "temperature":
            temperature.append(float(element[1]))
    
    return [x, humidity, temperature]
