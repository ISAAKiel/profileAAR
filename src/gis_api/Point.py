class Point:
    """
    A wrapper for the point information
    """
    def __init__(self, qgsPoint, z):
        """
        constructor
        :param qgsPoint:
        :param z: Number
        """
        self.point = qgsPoint
        self.z = z

    def getXVal(self):
        """
        returns the x value of that point
        :return: float
        """
        return float(self.point.x())

    def getYVal(self):
        """
        returns the y value
        :return: float
        """
        return float(self.point.y())

    def getZVal(self):
        """
        returns the z value
        :return: float
        """
        return float(self.z)
