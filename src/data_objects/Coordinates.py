from ..gis_api.Point import Point


class Coordinates:
    """
    Stores the necessary information for each point
    """
    def __init__(self, point, view_name, prof_name):
        """
        constructor
        :param point: Point
        :param view_name:
        :param prof_name:
        """
        self.point = point
        self.view_name = view_name
        self.profile_name = prof_name

class RotatePoints:
    """
    Stores the rotated point information
    """
    def __init__(self, a, b):
        """
        Constructor
        :param a: float
        :param b: float
        """
        self.a = a
        self.b = b