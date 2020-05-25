"""Creates panel schedule from selection"""
___context___ = 'Selection'
___author___ = 'Ozgur Taskin'


# How to use:
# Create a schedule named 'Sample_Schedule'. 
# You must add BIMSF_Container field. Add any other fields as you want.
# Assign two filters
# 1- BIMSF_Description / does not equal / PLABEL. This filter will remove panel labels from the schedule.
# 2- BIMSF_Container / equals / (place any panel number from the model)
# Select one or more panels members and run the code. 
# The tool will duplicate the 'Sample_Schedule', change the title and apply filter.

# The title for the new schedule:
# The tool creates 'Panel Number + Framing List' as the title.
# if you want to change 'Framing List' part, scroll down and change ' Framing List' on line 48.

from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from System.Collections.Generic import *

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Get BIMSF_Container from selection
selected_ids = uidoc.Selection.GetElementIds()

cont_list = []
param_list = []

for id in selected_ids:
	element = doc.GetElement(id)
	item = element.LookupParameter('BIMSF_Container')
	if item is not None:
		item = item.AsString()
	if item is not None:
		cont_list.append(item)
	
for cont in cont_list:
	if cont not in param_list:
		param_list.append(cont)

t = Transaction (doc, 'Create Schedule')
t.Start()
    
for param in param_list:
    schedule_title = param + ' Framing List'
    
    # Dublicate Sample_Schedule
    # Rename new schedule
    # Add filter to the new schedule
    schedule_col = FilteredElementCollector(doc) \
    .OfCategory(BuiltInCategory.OST_Schedules) \
    .WhereElementIsNotElementType() \
    .ToElements()
    

    
    # Dublicate Sample_Schedule
    for schedule_d in schedule_col:
        if schedule_d.ViewName == 'Sample_Schedule':
            schedule = schedule_d.Duplicate(ViewDuplicateOption.Duplicate)

    # Filter new schedule
    schedule_col_rename = FilteredElementCollector(doc) \
    .OfCategory(BuiltInCategory.OST_Schedules) \
    .WhereElementIsNotElementType() \
    .ToElements()
    
    # Rename schedule
    for schedule_r in schedule_col_rename:
        if schedule_r.ViewName == 'Sample_Schedule Copy 1':
            schedule_name = schedule_r.LookupParameter('View Name')
            schedule_name.Set(schedule_title)

    # Filter renamed schedule
    schedule_col_filter = FilteredElementCollector(doc) \
    .OfCategory(BuiltInCategory.OST_Schedules) \
    .WhereElementIsNotElementType() \
    .ToElements()
    
    # Create schedule filter from Sample_Schedule
    for schedule_cf in schedule_col_filter:
        if schedule_cf.ViewName == 'Sample_Schedule':
            ref_definition = schedule_cf.Definition
            ref_filter = ref_definition.GetFilter(1)
		
            a = ref_definition.GetFieldId(0)
            b = ref_filter.FilterType
            
            filter = ScheduleFilter(a, b, param)
    
    for schedule_f in schedule_col_filter:
        if schedule_f.ViewName == schedule_title:
            new_def = schedule_f.Definition
            new_def.RemoveFilter(1)
            new_def.AddFilter(filter)

t.Commit()