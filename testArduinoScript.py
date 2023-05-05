import serial

ser=serial.Serial("/dev/tty.usbmodem11201", 9600)

def parseData(inputData):
    inputData = inputData.decode("utf-8")
    inputData = inputData.strip()
    outputData = inputData.split(",")
    return outputData
    

while True:
    read_ser=ser.readline()
    print(read_ser)
    print(parseData(read_ser))

    