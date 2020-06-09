"""Selects all panel members"""
___context___ = 'Open Sheets'
___author___ = 'Ozgur Taskin'

# How to use:
# Select any sheet from Project Browser
# Run the tool
# You can select multiple sheets with holding CTRL or SHIFT

from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from System.Collections.Generic import *

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Create an empty list
sheet_list = []

# Get selection ids
selected_ids = uidoc.Selection.GetElementIds()

# Filter all sheets in the model
all_sheets = FilteredElementCollector(doc) \
.OfCategory(BuiltInCategory.OST_Sheets) \
.WhereElementIsNotElementType() \
.ToElements()

# Get Sheet Number parameters from selection
for id in selected_ids:
	element = doc.GetElement(id)
	param = element.LookupParameter('Sheet Number').AsString()
    # Get Sheet Number parameters from all sheets
	for selection in all_sheets:
		selection_param = selection.LookupParameter('Sheet Number').AsString()
        # If sheet number parameters matches between selection list and all sheets
        # add view element to empty list
		if param == selection_param:
			sheet_list.append(selection)

# Open sheets
for sheet in sheet_list:
	uidoc.RequestViewChange( sheet )