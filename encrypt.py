from dataclasses import dataclass
import random

DEBUG = 1 #None

@dataclass
class encInData:
    data: bytearray
    key: bytearray
    privateKey: bytearray

    def __init__(self, data: bytearray, key: bytearray, privateKey: bytearray):
        self.data = data
        self.key = key
        self.privateKey = privateKey
        return

@dataclass
class encOutData:
    data: bytearray
    key: bytearray

    def __init__(self, data: bytearray, key: bytearray):
        self.data = data
        self.key = key

class RlrpEncrypt():
    def __init__(self):
        return

    def encrypt(self, encrypt: encInData):
        TAG="RlrpEncrypt.encrypt"
        if DEBUG: print(TAG, "Starting encryption")

        outputData = RlrpEncrypt.createPackageRandom(self, encrypt.key, encrypt.data)

        return outputData
    
    
    def createPackageRandom(self, key, data):
        TAG="RlrpEncrypt.createPackageRandom"
        if DEBUG: print(TAG)
        randVal, outData, counter, lastRandom = 0, 0, 0, 0
        bitmapSize = 32
        random.seed(key)

        #While loop iterating through each byte of data
        for i in range(len(data)):
            randVal = RlrpEncrypt.createRandomWithBitsSet(self, 8, bitmapSize)
            if DEBUG: print(TAG, "randVal", randVal)
            buffer, counterBuffer, lastRandom = RlrpEncrypt.distributeDataAccordingToBitmap(self, randVal, data[i])
            if DEBUG: print(TAG, "buffer, counterBuffer", hex(buffer), f'{buffer:0>42b}', counterBuffer)
            outData |= (buffer << counter)
            if DEBUG: print(TAG, "outData", hex(outData), f'{outData:0>42b}')
            counter += counterBuffer

        #fill leftover byte with random values
        leftoverCounter  = 0
        while (counter) % 8 > 0:
            lastRandom = int.from_bytes(random.randbytes(32),"big")
            outData |= ((lastRandom % 2) << counter)
            counter += 1 
            leftoverCounter += 1
        if DEBUG: print(TAG, "outData, counter", hex(outData), f'{outData:0>42b}', counter)

        #return last used random value to show in gui. Will be used for next transmission in the session
        outputData = encOutData(outData, lastRandom)         
        return outputData
    

    def createRandomWithBitsSet(self, bitsSet, bitmapSize):
        TAG="RlrpEncrypt.createRandomWithBitsSet"
        bitsSet, i = 0, 0
        #Create pseudorandom bitmap until condition (-bitsSet- bits at least set to 1) is fulfilled
        while(bitsSet < 8):
            #Create pseudorandom value
            randomBitMap = int.from_bytes(random.randbytes(bitmapSize), "big")
            bitsSet, i = 0, 0
            while(i < bitmapSize*8):
                #Check if >= 8 bits are set to 1 in whole randval
                if((randomBitMap >> i) & 0x01 == 0x01):
                    bitsSet+=1
                i+=1
                
        if DEBUG: print(TAG, "randomBitMap, i", randomBitMap, i)
        return randomBitMap
    
    def distributeDataAccordingToBitmap(self, distributionMap, data):
        TAG="RlrpEncrypt.distributeDataAccordingToBitmap"
        #Distribute data according to bitmap. Start with last used random
        dataCounter, dataIndex, j, bitmap, lastRandom = 0, 0, 0, 0, 0
        while(dataCounter < 8):
            if((distributionMap >> j) & 0x01 == 0x01):
                #distribute data
                bitmap |= ((ord(data[dataIndex]) >> dataCounter) & 0x01) << j
                dataCounter+=1
            else:
                #distribute random value
                lastRandom = int.from_bytes(random.randbytes(32), "big")
                bitmap |= ((lastRandom % 2) << j)
            j+=1

        if DEBUG: print(TAG, "bitmap, j", bitmap, j)
        return bitmap, j-1, lastRandom