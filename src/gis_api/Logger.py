from qgis.core import QgsMessageLog


class Logger:
    """
    Wrapper for the qgis logger
    """

    def __init__(self, pluginName):
        """
        Constructor
        :param pluginName: string
        """
        self.pluginName = pluginName

    def log(self, message):
        """
        writes a message in the qgis log
        :param message: string
        :return: void
        """
        QgsMessageLog.logMessage(message, self.pluginName)
