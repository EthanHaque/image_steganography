from classes.combinePixels import CombineSigPixels
from PIL import Image


image1Path = r"C:\Users\Ethan_H_Laptop\Desktop\programs\python\really random stuff\hiddenImage\images\stitch.png"
image2Path = r"C:\Users\Ethan_H_Laptop\Desktop\programs\python\really random stuff\hiddenImage\images\hi.png"
obj = CombineSigPixels(image1Path, image2Path)

im = Image.new(mode = "RGB", size = (obj.image1.imWidth, obj.image1.imHeight))
for x in range(im.height):
        for y in range(im.width):
                im.putpixel((x,y), obj.combined[x][y])

im.save("test.png")