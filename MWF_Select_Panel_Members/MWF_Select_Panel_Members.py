"""Selects all panel members"""
___context___ = 'Selection'
___author___ = 'Ozgur Taskin'

# How to use:
# Select any member of a panel and run the tool.
# The tool will select all the members on the panel.
# The tool will work for three categories in Revit:
# 1- Structural Columns
# 2- Structural Framing
# 3- Structural Connectors

from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from System.Collections.Generic import *

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Get element ids from selection
selected_ids = uidoc.Selection.GetElementIds()

#Filter Structural Columns, Structural Framing and Structural Connections
column_col = FilteredElementCollector(doc) \
.OfCategory(BuiltInCategory.OST_StructuralColumns) \
.WhereElementIsNotElementType() \
.ToElements()
               
framing_col = FilteredElementCollector(doc) \
.OfCategory(BuiltInCategory.OST_StructuralFraming) \
.WhereElementIsNotElementType() \
.ToElements()
               
connection_col = FilteredElementCollector(doc) \
.OfCategory(BuiltInCategory.OST_StructConnections) \
.WhereElementIsNotElementType() \
.ToElements()

panel_members_id = []
          
for id in selected_ids:
    try:
        # Get BIMSF_Container from selection
		element = doc.GetElement(id)
		param = element.LookupParameter('BIMSF_Container').AsString()

		for col_id in column_col:
            # Add structural columns to the list if they have same BIMSF_Container
			container_id = col_id.LookupParameter('BIMSF_Container')
  			if container_id and container_id.AsString() == param:
  				panel_members_id.append(col_id.Id)
                
		for fra_id in framing_col:
            # Add structural framing to the list if they have same BIMSF_Container
			container_id = fra_id.LookupParameter('BIMSF_Container')
  			if container_id and container_id.AsString() == param:
  				panel_members_id.append(fra_id.Id)
                
		for con_id in connection_col:
            # Add structural connections to the list if they have same BIMSF_Container
			container_id = con_id.LookupParameter('BIMSF_Container')
  			if container_id and container_id.AsString() == param:
  				panel_members_id.append(con_id.Id)
        # Select members
		uidoc.Selection.SetElementIds(List[ElementId](panel_members_id))
        
		break

    except:
		continue

uidoc.RefreshActiveView()