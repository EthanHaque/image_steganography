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
    print(manipulatePixels.binarizePixelArray(readImage.getPixelArray()))