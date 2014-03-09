from django.contrib import admin
from App.models import tbl_standard, tbl_class, tbl_contentType, tbl_doc,\
    tbl_employee, tbl_empPersonalDetail, tbl_experienceDetail, tbl_location,\
    tbl_medium, tbl_permission, tbl_role, tbl_school, tbl_teaEducationalDetail,\
    tbl_teacher, tbl_subject, tbl_student, tbl_stdPersonalDetail,\
    tbl_stdEducationalDetail, tbl_sibling, tbl_systemUser, tbl_classStudent,\
     tbl_examResult, tbl_MSS\
    , tbl_subjectAndTeacher, tbl_subjectMarks, tbl_shortstandard, tbl_examType,\
    tbl_markAttendence, tbl_attendence, tbl_holiday, tbl_taskList,\
    tbl_feetype, tbl_feeParameter, tbl_fees, tbl_feePayment\
    , tbl_timeTable, tbl_libItem, tbl_issueItem, tbl_uniqueitemList,\
    tbl_supplier, tbl_removeLibItems, tbl_libMember, tbl_libIssuePeriod,\
    tbl_itemInfo, tbl_studentLog, tbl_tempFees, tbl_grades, tbl_product,\
    tbl_studentFacility, tbl_events, Notice
from django.contrib.admin.options import ModelAdmin

    
class O_doc(ModelAdmin):
    list_display=('id','name','file')
    
class O_content(ModelAdmin):
    list_display=('id','category','name','isActive')
class O_sANDt(ModelAdmin):
    list_display=('id','subject')

class O_employee(ModelAdmin):
    list_display=('id','perDetail')

class O_empPerDetails(ModelAdmin):
    list_display=('id','fName','lName')


admin.site.register(tbl_school)
admin.site.register(Notice)
admin.site.register(tbl_events)
admin.site.register(tbl_medium)
admin.site.register(tbl_standard)
admin.site.register(tbl_subject)
admin.site.register(tbl_class)


admin.site.register(tbl_contentType,O_content)
admin.site.register(tbl_permission)
admin.site.register(tbl_role)
admin.site.register(tbl_location)
admin.site.register(tbl_doc,O_doc)

admin.site.register(tbl_teacher)
admin.site.register(tbl_systemUser)
admin.site.register(tbl_employee,O_employee)
admin.site.register(tbl_empPersonalDetail,O_empPerDetails)
admin.site.register(tbl_experienceDetail)
admin.site.register(tbl_teaEducationalDetail)

admin.site.register(tbl_student)
admin.site.register(tbl_stdPersonalDetail)
admin.site.register(tbl_stdEducationalDetail)
admin.site.register(tbl_sibling)

admin.site.register(tbl_classStudent)
admin.site.register(tbl_examType)

admin.site.register(tbl_examResult)
admin.site.register(tbl_MSS)
admin.site.register(tbl_subjectAndTeacher,O_sANDt)
admin.site.register(tbl_subjectMarks)
admin.site.register(tbl_shortstandard)
admin.site.register(tbl_timeTable)
admin.site.register(tbl_libItem)
admin.site.register(tbl_issueItem)
admin.site.register(tbl_uniqueitemList)
admin.site.register(tbl_supplier)
admin.site.register(tbl_removeLibItems)
admin.site.register(tbl_libMember)
admin.site.register(tbl_libIssuePeriod)
admin.site.register(tbl_itemInfo)


#admin.site.unregister()
admin.site.register(tbl_markAttendence)
admin.site.register(tbl_attendence)
admin.site.register(tbl_holiday)
admin.site.register(tbl_taskList)
admin.site.register(tbl_feetype)
admin.site.register(tbl_feeParameter)
admin.site.register(tbl_fees)
admin.site.register(tbl_feePayment)
admin.site.register(tbl_studentLog)


admin.site.register(tbl_tempFees)
admin.site.register(tbl_grades)
admin.site.register(tbl_product)
admin.site.register(tbl_studentFacility)



