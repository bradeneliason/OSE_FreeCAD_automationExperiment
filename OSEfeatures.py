"""
An example of creating a feature for dimensional lumber

TODO
  - Hide the height and width properties
  - get the nominal dimensions to update the height and width properties
  - change the color to look like wood
"""

import FreeCAD, Part, math
from FreeCAD import Base
from pivy import coin

class PartFeature:
	def __init__(self, obj):
		obj.Proxy = self

nomToAct = {"1": 0.75, "2": 1.5, "3": 2.5, "4": 3.5, "6": 5.5, "8": 7.25, "10":9.25, "12":11.25}

class Lumber(PartFeature):
	
	def __init__(self, obj):
		PartFeature.__init__(self, obj)
		''' Add some custom properties to our lumber feature '''
		obj.addProperty("App::PropertyLength","Length","Lumber","Length of the lumber").Length='8 ft'
		obj.addProperty("App::PropertyLength","Width","Lumber","Width of the lumber").Width='3.5 in'
		obj.addProperty("App::PropertyLength","Height","Lumber", "Height of the lumber").Height='1.5 in'
		obj.addProperty('App::PropertyEnumeration', 'Size', 'Lumber', 'Nominal Dimensions')
		obj.Size = ["1x2", "1x3", "1x4", "1x6", "1x8", "1x10","1x12", "2x2", "2x3", "2x4", "2x6", "2x8", "2x10", "2x12", "4x4", "4x6", "6x6"]
		obj.Size = "2x4"
        
        # Name the feature based on nominal size
		obj.Label = obj.Size + "_001"
		
		# Set Width and Height properties to read only mode
		obj.setEditorMode("Width", 1)
		obj.setEditorMode("Height", 1)

	def onChanged(self, fp, prop):
		''' Print the name of the property that has changed '''
		FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")
		# Update width and height from nominal dimentions
		if str(prop) == "Size":
				dims = fp.Size.split("x")
				fp.Width = str(nomToAct[dims[1]]) + ' in'
				fp.Height = str(nomToAct[dims[0]]) + ' in'
				fp.Label = fp.Size + "_" + fp.Label.split("_")[1] # update label (optional)
				self.execute(fp)

	def execute(self, fp):
		''' Print a short message when doing a recomputation, this method is mandatory '''
		FreeCAD.Console.PrintMessage("Recompute Python Lumber feature\n")
		fp.Shape = Part.makeBox(fp.Length,fp.Width,fp.Height)

class ViewProviderLumber:
	def __init__(self, obj):
		''' Set this object to the proxy object of the actual view provider '''
		obj.Proxy = self

	def attach(self, obj):
		''' Setup the scene sub-graph of the view provider, this method is mandatory '''
		return

	def updateData(self, fp, prop):
		''' If a property of the handled feature has changed we have the chance to handle this here '''
		return

	def getDisplayModes(self,obj):
		''' Return a list of display modes. '''
		modes=[]
		return modes

	def getDefaultDisplayMode(self):
		''' Return the name of the default display mode. It must be defined in getDisplayModes. '''
		return "Shaded"

	def setDisplayMode(self,mode):
		''' Map the display mode defined in attach with those defined in getDisplayModes.
		Since they have the same names nothing needs to be done. This method is optional.
		'''
		return mode

	def onChanged(self, vp, prop):
		''' Print the name of the property that has changed '''
		FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")

	def getIcon(self):
		''' Return the icon in XMP format which will appear in the tree view. This method is optional
		and if not defined a default icon is shown.
		'''
		return """
			/* XPM */
			static const char * ViewProviderLumber_xpm[] = {
			"16 16 6 1",
			" 	c None",
			".	c #141010",
			"+	c #615BD2",
			"@	c #C39D55",
			"#	c #000000",
			"$	c #57C355",
			"        ........",
			"   ......++..+..",
			"   .@@@@.++..++.",
			"   .@@@@.++..++.",
			"   .@@  .++++++.",
			"  ..@@  .++..++.",
			"###@@@@ .++..++.",
			"##$.@@$#.++++++.",
			"#$#$.$$$........",
			"#$$#######      ",
			"#$$#$$$$$#      ",
			"#$$#$$$$$#      ",
			"#$$#$$$$$#      ",
			" #$#$$$$$#      ",
			"  ##$$$$$#      ",
			"   #######      "};
			"""

	def __getstate__(self):
		''' When saving the document this object gets stored using Python's cPickle module.
		Since we have some un-pickable here -- the Coin stuff -- we must define this method
		to return a tuple of all pickable objects or None.
		'''
		return None

	def __setstate__(self,state):
		''' When restoring the pickled object from document we have the chance to set some
		internals here. Since no data were pickled nothing needs to be done here.
		'''
		return None


def makeLumber():
	doc = FreeCAD.activeDocument()
	a=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","Lumber")
	Lumber(a)
	ViewProviderLumber(a.ViewObject)
	doc.recompute()
	return a

