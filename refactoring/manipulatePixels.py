from readImage import ReadImage

class MainpulatePixels:

    def binaryize(self, readImageObj):
        for y in readImageObj.getHeight():
            for x in readImageObj.getWidth():
                for z in range(readImageObj.getChannels()):
