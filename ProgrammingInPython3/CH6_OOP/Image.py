#! python3
import pickle
import os

# Exceptions #
# =========================================================================== #
class ImageError(Exception):        pass
class CoordinateError(ImageError):  pass
class LoadError(ImageError):        pass
class SaveError(ImageError):        pass
class ExportError(ImageError):      pass
class NoFilenameError(ImageError):  pass
# =========================================================================== #


# Image class #
# =========================================================================== #
class Image:

    def __init__(self, width, height, filename="", background="#FFFFFF"):
        self.filename = filename
        self._background = background
        self._data = {}
        self._width = width
        self._height = height
        self._colors = {self._background}

    @property
    def background(self):
        return self._background
    
    @property
    def width(self):
        return self._width
    
    @property
    def height(self):
        return self._height
    
    @property
    def colors(self):
        return set(self._colors)

    def __getitem__(self, coordinate):
        assert len(coordinate) == 2, "coordinate should be a 2-tuple"
        if( not(0 <= coordinate[0] < self.width) or
            not(0 <= coordinate[1] < self.height) ):
            raise CoordinateError(str(coordinate))

        return self._data.get(tuple(coordinate), self._background)

    def __setitem__(self, coordinate, color):
        assert len(coordinate) == 2, "coordinate should be a 2-tuple"
        if( not(0 <= coordinate[0] < self.width) or
            not(0 <= coordinate[1] < self.height) ):
            raise CoordinateError(str(coordinate))
        if color == self._background:
            self._data.pop(tuple(coordinate), None)
        else:
            self._data[tuple(coordinate)] = color
            self._colors.add(color)

    def __delitem__(self, coordinate):
        assert len(coordinate) == 2, "coordinate should be a 2-tuple"
        if( not(0 <= coordinate[0] < self.width) or
            not(0 <= coordinate[1] < self.height)):
            raise CoordinateError(str(coordinate))
        self._data.pop(tuple(coordinate), None)

    def save(self, filename=None):
        if filename is not None:
            self.filename = filename
        if not self.filename:
            raise NoFilenameError()

        fh = None
        try:
            data = [self.width, self.height, self._background, self._data]
            fh = open(self.filename, 'wb')
            pickle.dump(data, fh, pickle.HIGHEST_PROTOCOL)
        except (EnvironmentError, pickle.PicklingError) as err:
            raise SaveError(str(err))
        finally:
            if fh is not None:
                fh.close()

    def load(self, filename=None):
        if filename is not None:
            self.filename = filename
        if not self.filename:
            raise NoFilenameError()

        fh = None
        try:
            fh = open(self.filename, 'rb')
            data = pickle.load(fh)
            (self._width, self._height, self._background, self._data) = data
            self._colors = (set(self._data.values()) | {self._background})
        except (EnvironmentError, pickle.UnpicklingError) as err:
            raise LoadError(str(err))
        finally:
            if fh is not None:
                fh.close()

    def export(self, filename):
        if filename.lower().endswith(".xpm"):
            self._export_xpm(filename)
        else:
            raise ExportError("unsupported export format: " +
                                os.path.splittext(filename)[1])
# =========================================================================== #
