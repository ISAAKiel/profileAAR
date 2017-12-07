class TransformationLists:
    """
    Iterable object for storing the different kind of lists
    """
    def __init__(self, x_list, y_list, z_list):
        """
        constructor
        :param x_list: float[]
        :param y_list: float[]
        :param z_list: float[]
        """
        self.i = 0
        self.x_list = x_list
        self.y_list = y_list
        self.z_list = z_list
        self.minYZ = None

    def __iter__(self):
        """
        iterator implementation
        :return: self
        """
        return self

    def getMinYZ(self):
        """
        Calculates the minimum value of the sum of y_list and x_list if not all ready set
        :return: float
        """
        if self.minYZ == None:
            self.minYZ = min(self.y_list + self.x_list)
        return self.minYZ

    def next(self):
        """
        get next item in lists
        :return: float[]
        """
        if self.i < len(self.x_list):
            list = [self.x_list[self.i], self.y_list[self.i], self.z_list[self.i]]
        else:
            raise StopIteration()
        self.i += 1
        return list

    def emptyX(self):
        """
        clears the x values
        :return: void
        """
        self.x_list = []

    def emptyY(self):
        """
        clears the y value
        :return: void
        """
        self.y_list = []

    def emptyZ(self):
        """
        clears the z value
        :return: void
        """
        self.z_list = []

class SlopeVarLists:
    """
    DataObject for slope calculation
    """
    def __init__(self):
        """
        constructor
        """
        self.x = []
        self.y = []