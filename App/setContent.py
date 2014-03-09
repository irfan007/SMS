from App.models import tbl_contentType


def setUpContentType():
	'''
	_types contains content type as
	'category':'name1,name2,...' 
	
	NOTE: must be updated!!!!
	'''
	_types=[
		['configuration','role:user:staff:medium:section:standard:subject:holiday:setting:exam:grades'],
		['teacher','teacher'],
		['student','student'],
		['fees','fees'],
		['attendance','attendance'],
		['library','library'],
		['subject and teacher','assign'],
		['schedule period','schedule'],
		['notice','notice'],
		]
	
	for cat,names in _types:
		for name in names.split(':'):
			tbl_contentType.objects.create(category=cat,name=name,isActive=True)
	
	print '<<CONTENT TYPE DONE>>'		
		
#setUpContentType()