from manipulatePixels import ManipulatePixels
from readImage import ReadImage
from PIL import Image

class ManipulateImages:

    def __init__(self):
        pass

    def combineSigBits(self, path1, path2):
        manipulatePixels = ManipulatePixels()
        mainImage = ReadImage(path1)
        hiddenImage = ReadImage(path2)
        mainImageSigBits = manipulatePixels.getSigDigs(mainImage.getPixelArray())
        hiddenImageSigBits = manipulatePixels.getSigDigs(hiddenImage.getPixelArray())
        return(manipulatePixels.combinePixelArray(mainImageSigBits, hiddenImageSigBits))

    def combineImages(self, path1, path2, name):
        manipulatePixels = ManipulatePixels()
        binArray3D = self.combineSigBits(path1, path2)
        array3D = manipulatePixels.decimalizePixelArray(binArray3D)
        im = Image.new(mode = "RGB", size = (len(array3D[0]), len(array3D)))
        for y in range(len(array3D)):
            for x in range(len(array3D[0])):
                im.putpixel((x,y), array3D[y][x])
        im.save(name)

    def seperateSigBits(self, path):
        manipulatePixels = ManipulatePixels()
        image = ReadImage(path)
        bits = manipulatePixels.binarize3DDigits(image.getPixelArray())
        paddedBits = manipulatePixels.pad4DSigBitArray(bits)
        return(paddedBits)

    def seperateImages(self, path, hiddenName, mainName):
        manipulatePixles = ManipulatePixels()
        binArray4D = self.seperateSigBits(path)
        mainImageBin3DArray = binArray4D[1]
        hiddenImageBin3DArray = binArray4D[0]
        mainImage3DArray = manipulatePixles.decimalizePixelArray(mainImageBin3DArray)
        hiddenImage3DArray = manipulatePixles.decimalizePixelArray(hiddenImageBin3DArray)
        mainIm = Image.new(mode = "RGB", size = (len(mainImage3DArray[0]), len(mainImage3DArray)))
        for y in range(len(mainImage3DArray)):
            for x in range(len(mainImage3DArray[0])):
                mainIm.putpixel((x,y), mainImage3DArray[y][x])
        mainIm.save(mainName)
        hiddenIm = Image.new(mode = "RGB", size = (len(hiddenImage3DArray[0]), len(hiddenImage3DArray)))
        for y in range(len(hiddenImage3DArray)):
            for x in range(len(hiddenImage3DArray[0])):
                hiddenIm.putpixel((x,y), hiddenImage3DArray[y][x])
        hiddenIm.save(hiddenName)
        
        

if __name__ == "__main__":
    path1 = r"C:\Users\ebaba\Desktop\Python\Image_Steganography\images\cat.png"
    path2 = r"C:\Users\ebaba\Desktop\Python\Image_Steganography\images\poem.png"
    path = r"C:\Users\ebaba\Desktop\Python\Image_Steganography\test.png"
    manipulateImages = ManipulateImages()
    manipulateImages.combineImages(path1, path2, "test.png")
    #manipulateImages.seperateImages(path, "main.png", "hidden.png")