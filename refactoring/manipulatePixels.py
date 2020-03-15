from readImage import ReadImage

class ManipulatePixels:
    
    def __init__(self):
        pass

    def binarize3D(self, array3D, rows, cols, channels):
        binArray = []
        for y in range(cols):
            binArray.append([])
            for x in range(rows):
                binArray.append(())
                for z in range(channels):
                    decimal = array3D[x][y][z]
                    binaryNum = bin(decimal)[2:]


if __name__ == "__main__":
    manipulatePixels = ManipulatePixels()
    manipulatePixels.binarize3D([], 10, 10, 3)