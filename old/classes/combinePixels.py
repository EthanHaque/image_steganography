from classes.getSigDigs import ReadImage

class CombineSigPixels:
    image1 = None
    image2 = None
    combined = []

    def __init__(self, image1Path, image2Path):
        self.image1 = ReadImage(image1Path)
        self.image2 = ReadImage(image2Path)
        if(self.image1.imWidth != self.image2.imWidth or self.image1.imHeight != self.image2.imHeight):
            print("images not the same size")
            exit()   
        else:
            self.combined = self.combineLists(self.image1.pixelMap, self.image2.pixelMap)     

    def combineLists(self, map1, map2):
        outMap = []
        for y in range(self.image1.imHeight):
            outMap.append([])
            for x in range(self.image1.imWidth):
                outMap[y].append(())
                for z in range(3):
                    outMap[y][x] += (int((map1[x][y][z] + map2[x][y][z]), 2),)
        return(outMap)
        

if __name__ == "__main__":
    image1Path = r"C:\Users\Ethan_H_Laptop\Desktop\programs\python\really random stuff\hiddenImage\images\stitch.png"
    image2Path = r"C:\Users\Ethan_H_Laptop\Desktop\programs\python\really random stuff\hiddenImage\images\hi.png"
    obj = CombineSigPixels(image1Path, image2Path)
