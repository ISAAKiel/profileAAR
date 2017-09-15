from qgis.gui import QgsMessageBar
from qgis.core import *
import sys
class ErrorHandler: 
    def __init__(self, qgisInterface):
        self.qgisInterface = qgisInterface

    def singleprofile(self, coord_proc, view_check, profile_name):
        # TODO: check for consistency before calculation
        # TODO: check for spatial consistency (no points should be more than x meters apart)
        
        # check if actual profile has less then 4 points
        if len(coord_proc) <= 3:
            #if it is less, print error message
            self.qgisInterface.messageBar().pushMessage("Error", "A profile needs min. 4 points. Error on profile: "+str(profile_name), level=QgsMessageBar.CRITICAL)
            #cancel execution of the script
            sys.exitfunc()

        # check if the view value is the same in all features
        if len(view_check) != 1:
            # if it is not the same, print error message
            self.qgisInterface.messageBar().pushMessage("Error", "The view column of your data is inconsistant (either non or two different views are present). Error on profile: " + str(profile_name), level=QgsMessageBar.CRITICAL)
            # cancel execution of the script
            sys.exitfunc()

        # check if the view is one of the four cardinal directions
        if view_check[0].upper() not in ["N", "E", "S", "W"]:
            # if it is not the same, print error message
            self.qgisInterface.messageBar().pushMessage("Error", "The view value is not one of the four cardinal directions. Error on profile: " + str(profile_name), level=QgsMessageBar.CRITICAL)
            # cancel execution of the script
            sys.exitfunc()
            
    def singlelayer(self, layer):
        #check will be the return after checking the data
        check = False
        #only use vector layers
        if layer.type() != QgsMapLayer.VectorLayer:
            check = False
        #only use point vector layers (check of vector before, because this crashes on rasterdata)
        elif layer.geometryType() != QGis.Point:
            check = False
        #Check if the vectorlayer is projected
        elif layer.crs().geographicFlag() == True:
            self.qgisInterface.messageBar().pushMessage("Information", "Layer "+layer.name()+ " was dropped, because it is not projected. ", level=QgsMessageBar.INFO)
            check = False
        else:
            check = True
        return check
    
    def linreg_residuals:
        #calculate the residuals for each point and add the as an Attribute
        
        #print the mean, min, max residuals of each profile