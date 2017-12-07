from qgis.gui import QgsMessageBar

class MessageWrappper:
    """
    Used to communicate with the actual qgisInterface
    """
    def __init__(self, qgisInterface):
        """
        constructor
        :param qgisInterface:
        """
        self.qgisInterface = qgisInterface

    def printMessage(self):
        pass

    def printError(self, message):
        """
        prints an error message via messageBar
        :param message: string
        :return: void
        """
        self.qgisInterface.messageBar().pushMessage("Error", message, level=QgsMessageBar.CRITICAL)

    def printWarning(self, message):
        """
        prints a warning via messageBar
        :param message: string
        :return: void
        """
        self.qgisInterface.messageBar().pushMessage("Warning", message)

    def printInfo(self, message):
        """
        prints an information via messageBar
        :param message: string
        :return: void
        """
        self.qgisInterface.messageBar().pushMessage("Information", message,level=QgsMessageBar.CRITICAL)