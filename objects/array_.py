"""Array class for creating array type"""


class Array:
    data_type=None
    __length=None

    @property
    def length(self):
        return self.__length

    @length.setter
    def length(self, length):
        self.__length = length
