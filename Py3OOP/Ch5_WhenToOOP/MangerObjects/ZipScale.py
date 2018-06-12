from ZipProcessor import ZipProcessor
import sys
from PIL import Image


class ZipScale(ZipProcessor):

    def process_files(self):
        '''Scale each image in the directory to 640x480'''
        for filename in self.temp_directory.iterdir():
            im = Image.open(str(filename))
            scaled = im.resize((640,480))
            scaled.save(str(filename))


if __name__ == '__main__':
    ZipScale(*sys.argv[1:4]).process_zip()
