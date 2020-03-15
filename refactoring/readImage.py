from PIL import Image

class ReadImage:
    pixelArray = []
    im = None
    height = 0
    width = 0
    channels = 0

    def __init__(self, path):
        try:
            self.im = Image.open(path)
        except:
            print("could not find image")
            exit()
        self.height = self.im.height
        self.width = self.im.width
        self.pixelArray = self.createPixelArray()
        self.channels = len(self.getPixelArray()[0][0])

    def createPixelArray(self):
        pxMap = []
        for y in range(self.getHeight()):
            pxMap.append([])
            for x in range(self.getWidth()):
                pixel = self.getImage().getpixel((x,y))
                pxMap[y].append(pixel)
        return(pxMap)
    
    def getPixelArray(self):
        return(self.pixelArray)
    
    def getImage(self):
        return(self.im)
    
    def getHeight(self):
        return(self.height)
    
    def getWidth(self):
        return(self.width)

    def getChannels(self):
        return(self.channels)

if __name__ == "__main__":
    image = r"C:\Users\ebaba\Desktop\Python\Image_Steganography\images\stitch.png"
    readImage = ReadImage(image)
    print(readImage.getChannels())