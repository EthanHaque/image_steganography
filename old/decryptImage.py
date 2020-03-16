from classes.getSigDigs import ReadImage
from PIL import Image

image1Path = r"C:\Users\Ethan_H_Laptop\Desktop\programs\python\really random stuff\hiddenImage\science.png"
obj = ReadImage(image1Path)

im = Image.new(mode = "RGB", size = (obj.imWidth, obj.imWidth))
for x in range(im.height):
        for y in range(im.width):
                im.putpixel((x,y), obj.reverseMap[x][y])

im.save("output.png")