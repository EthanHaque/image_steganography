from readImage import ReadImage

class ManipulatePixels:
    
    def __init__(self):
        pass

    def binarize3DDigits(self, array3D):
        binArray = []
        for i in range(2):
            binArray.append([])
            for y in range(len(array3D)):
                binArray[i].append([])
                for x in range(len(array3D[0])):
                    binArray[i][y].append(())
                    for z in range(len(array3D[0][0])):
                        decimal = array3D[y][x][z]
                        binaryNum = bin(decimal)[2:]
                        paddedBinaryNum = (8 - len(binaryNum)) * "0" + binaryNum
                        if(i == 0):
                            binArray[i][y][x] += (paddedBinaryNum[:4],)
                        else:
                            binArray[i][y][x] += (paddedBinaryNum[4:],)
        return(binArray)

    def binarizePixelArray(self, array3D):
        sigInsigPixelArray = self.binarize3DDigits(array3D)
        combinedPixelArray = []
        for y in range(len(sigInsigPixelArray[0])):
            combinedPixelArray.append([])
            for x in range(len(sigInsigPixelArray[0][0])):
                combinedPixelArray[y].append(())
                for z in range(len(sigInsigPixelArray[0][0][0])):
                        combinedPixelArray[y][x] += (sigInsigPixelArray[0][y][x][z] + sigInsigPixelArray[1][y][x][z], )
        return(combinedPixelArray)

    def pad4DSigBitArray(self, array4D):
        paddedArray = []
        for i in range(2):
            paddedArray.append([])
            for y in range(len(array4D[0])):
                paddedArray[i].append([])
                for x in range(len(array4D[0][0])):
                    paddedArray[i][y].append(())
                    for z in range(len(array4D[0][0][0])):
                        paddedArray[i][y][x] += (array4D[i][y][x][z] + "0" * (8 - len(array4D[i][y][x][z])), )
        return(paddedArray)

    def decimalizePixelArray(self, array3D):
        decimalPixelArray = []
        for y in range(len(array3D)):
            decimalPixelArray.append([])
            for x in range(len(array3D[0])):
                decimalPixelArray[y].append(())
                for z in range(len(array3D[0][0])):
                    decimalPixelArray[y][x] += (int(array3D[y][x][z], 2), )
        return(decimalPixelArray)

    def addNullChannel(self, array3D):
        addedChannel = []
        for y in range(len(array3D)):
            addedChannel.append([])
            for x in range(len(array3D[0])):
                addedChannel[y].append(array3D[y][x] + ("0", ))
        return(addedChannel)
                
    def combinePixelArray(self, array3D1, array3D2):
        if(len(array3D1[0][0]) > len(array3D2[0][0])):
            for i in range(len(array3D1[0][0]) - len(array3D2[0][0])):
                array3D2 = self.addNullChannel(array3D2)
        elif(len(array3D2[0][0]) > len(array3D1[0][0])):
            for i in range(len(array3D2[0][0]) - len(array3D1[0][0])):
                array3D1 = self.addNullChannel(array3D1)
        combinedPixelArray = []
        for y in range(len(array3D1)):
            combinedPixelArray.append([])
            for x in range(len(array3D1[0])):
                combinedPixelArray[y].append(())
                for z in range(len(array3D1[0][0])):
                    combinedPixelArray[y][x] += (array3D1[y][x][z] + array3D2[y][x][z],)
        return(combinedPixelArray)
        
    def getSigDigs(self, array3D):
        sigInsigPixelArray = self.binarize3DDigits(array3D)
        return(sigInsigPixelArray[0])

    def getInsigDigs(self, array3D):
        sigInsigPixelArray = self.binarize3DDigits(array3D)
        return(sigInsigPixelArray[1])
                    

if __name__ == "__main__":
    image = r"C:\Users\ebaba\Desktop\Python\Image_Steganography\images\stitch.png"
    readImage = ReadImage(image)
    manipulatePixels = ManipulatePixels()
    arr = manipulatePixels.binarizePixelArray(readImage.getPixelArray())
    print(manipulatePixels.addNullChannel(arr))