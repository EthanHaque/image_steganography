from PIL import Image

class ReadImage:
    pixelArray = []
    im = None
    height = None
    width = None

    def __init__(self, path):
        try:
            self.im = Image.open(path)
        except:
            print("could not find image")
            exit()
        self.height = self.im.height
        self.width = self.im.width
        self.pixelArray = self.createPixelArray()

    def createPixelArray(self):
        pxMap = []
        for y in range(self.height):
            pxMap.append([])
            for x in range(self.width):
                pixel = self.im.getpixel((x,y))
                pxMap.append(pixel)
        return(pxMap)
    
    def getPixelArray(self):
        return(self.pixelArray)
    
    def getImage(self):
        return(self.im)
    
    def getHeight(self):
        return(self.height)
    
    def getWidth(self):
        return(self.width)

if __name__ == "__main__":
    image = r"C:\Users\Ethan_H_Laptop\Desktop\programs\python\really random stuff\hiddenImage\images\stitch.png"
    readImage = ReadImage(image)
    print(readImage.pixelArray)