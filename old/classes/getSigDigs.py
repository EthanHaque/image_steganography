from PIL import Image

class ReadImage:
    pixelMap = []
    reverseMap = []
    im = None
    imHeight = None
    imWidth = None

    def __init__(self, path):
        self.im = Image.open(path)
        self.imHeight = self.im.height
        self.imWidth = self.im.width
        self.pixelMap = self.mapPixles()
        self.reverseMap = self.combineZeros(self.reversePixels())
        

    def mapPixles(self):
        pxMap = []
        for y in range(self.im.height):
            pxMap.append([])
            for x in range(self.im.width):
                pixel = self.im.getpixel((x,y))[0:3]
                pxMap[y].append(self.getSigDigs(pixel))
        return(pxMap)

    def reversePixels(self):
        rvMap = []
        for y in range(self.im.height):
            rvMap.append([])
            for x in range(self.im.width):
                pixel = self.im.getpixel((x,y))[0:3]
                rvMap[y].append(self.reverse(pixel))
        return(rvMap)

    def getSigDigs(self, rgb):
        sigDigs = map(self.binaryConversion, rgb)
        return(tuple(sigDigs))
    
    def binaryConversion(self, num):
        binaryNum = bin(num)[2:]
        eightBit = (8 - len(binaryNum)) * "0" + binaryNum
        return(eightBit[:4])

    def reverseBinaryConversion(self, num):
        binaryNum = bin(num)[2:]
        eightBit = (8 - len(binaryNum)) * "0" + binaryNum
        return(eightBit[4:])

    def reverse(self, rgb):
        sigDigs = map(self.reverseBinaryConversion, rgb)
        return(tuple(sigDigs))

    def combineZeros(self, map1):
        outMap = []
        for y in range(len(map1)):
            outMap.append([])
            for x in range(len(map1[0])):
                outMap[y].append(())
                for z in range(3):
                    #print(y,x,z)
                    outMap[y][x] += (int((map1[x][y][z] + "0000"), 2),)
        return(outMap)


if (__name__ == "__main__"):
    image = ReadImage(r"C:\Users\Ethan_H_Laptop\Desktop\programs\python\really random stuff\hiddenImage\images\hi.png")

    

