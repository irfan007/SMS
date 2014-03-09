from django.conf.urls import patterns, include, url
from django.contrib import admin
from views.authenticate import v_home, v_loginUser, v_logoutUser,\
    v_forgotPassword
from views.systemUser import v_user, v_addUser, v_editUser
from views.role import v_role, v_addRole, v_editRole
from views.teacher import v_teacher, v_addTeacher, v_editTeacher,\
    v_uploadMarks_p1, v_viewMarks_p1, v_viewMarksList, v_studPerformance
    

from views.student import v_addStudent, v_editStudent, v_student,\
    v_accMresponder, v_nextStudent, v_prevStudent,\
    v_studPromote, getdatatopromote, v_studHistory, v_nextstudHistory,\
    v_prevstudHistory, v_viewstudRecord, v_studRecordYearWise,\
    v_searchStudent, v_assignRollNo, v_Notice, v_user_detail
from views.medium import v_editMedium, v_medium
from views.subject import v_subject, v_addsubject, v_editsubject
from views.section import v_section, v_editsection
from views.standard import v_standard, v_addStandard, v_editStandard
from views.popup import v_popUp
from views.mss import   \
     v_addSubjectMarks, v_viewSubjectMarks
from views.responder import v_responder
from views.result import v_viewResult
from views.staff import v_staff, v_addStaff, v_editstaff
from views.fees import  v_AddfeeCategory, v_Editfeecategory ,\
    v_assignFees, v_feePayment, v_feePaymentAdd, v_feePaymentedit,\
    v_generateslip,  v_nextfeePayment,\
    v_prevfeePayment, v_feePending, v_feeCategory, v_addassignFees,\
    v_assignSessionFees
from views.school import v_school, v_addSchool, v_editSchool
from views.attendence import v_addAttendence, v_attendence,\
    v_attendencedata, v_viewAttendenceReport
from views.holidays import v_holidays, v_addHoliday, v_editHoliday,\
    v_prevHolidays, v_nextHolidays, v_Yearholidays
from views.timetable import v_createTimeTable, v_editTimeTable
from views.library_management import v_libItems, v_addLibItem, v_editLibItem,\
    v_libMembers, v_addLibMember, v_getPersonDetail, v_editLibMember,\
    v_libmanagestock, v_libstockmodify, v_libstockhistory, v_itemIssues,\
    v_libItemSearch, v_addIssue, v_editIssue, v_libItemViewAll,\
    v_libdeducthistory, v_nextitemIssues, v_previtemIssues, v_Nextlibmanagestock,\
    v_Prevlibmanagestock, v_prevlibMembers, v_nextlibMembers, v_PrevlibItems,\
    v_NextlibItems
from views.subjectAndTeacher import v_subjectAndTeacher
from views.grading import v_grading, v_addGrades, v_editGrades
from views.examType import v_editExamType, v_examType, v_responder1,\
    v_dateattendenceRecord, v_studentSibling, getstudents
from App.pp import i_decompose
from SMS.settings import SECRET_KEY
from views.clientSide import v_trial, v_activate
from django.shortcuts import render_to_response
from views.calendar import v_eventCalander
from views.schedulePeriod import v_schedulePeriod



def valid():
    from App.models import tbl_product
    import datetime
    try:
        product=tbl_product.objects.get(id=1)
        if i_decompose([str(product.sid),str(product.agent),str(product.purchaseDate),str(product.expireDate),SECRET_KEY])==product.key:
            if product.expireDate:
                if product.purchaseDate <= datetime.date.today() <= product.expireDate:
                    return True
                else:
                    return False
            else:
                return True
        else:
            product.key=None
            product.save()
            return False
    except:
        return False


if True:
    admin.autodiscover()
    
    urlpatterns = patterns('',
        
        url(r'^admin/', include(admin.site.urls)),    
        url(r'^events/',v_eventCalander),
        
        
        
        url(r'^$',v_home),
        
        
        
        url(r'^subjectandteacher/$',v_subjectAndTeacher),
        url(r'^responder/',v_responder),
        url(r'^pop/(.+)$',v_popUp),
        
        
        url(r'^login/$',v_loginUser),
        url(r'^logout/$',v_logoutUser),
        url(r'^forgotPassword/$',v_forgotPassword),
        
        url(r'^user/$',v_user),
        url(r'^user/add/$',v_addUser),
        url(r'^user/edit/([\d]+)',v_editUser),
        
        url(r'^role/$',v_role),
        url(r'^role/add/$',v_addRole),
        url(r'^role/edit/([\d]+)',v_editRole),
        
        url(r'^staff/$',v_staff),
        url(r'^staff/add/$',v_addStaff),
        url(r'^staff/edit/([\d]+)',v_editstaff),
        
        url(r'^teacher/$',v_teacher),
        url(r'^teacher/add/$',v_addTeacher),
        url(r'^teacher/edit/([\d]+)',v_editTeacher),
        url(r'^teacher/upload/marks',v_uploadMarks_p1),
        url(r'^teacher/view/marks/$',v_viewMarks_p1),
        url(r'^teacher/view/marks/([\d]+)',v_viewMarksList),
        
        
        
        #url(r'^subjectAndTeacher/$',v_manageSubjectList),
        #url(r'^manage/subject/add/$',v_manageSubjectAndTeacher),
        #url(r'^manage/subject/([\d]+)',v_manageSubjectEdit),
        url(r'^add/marks/([\d]+)',v_addSubjectMarks),
        url(r'^result/subject/([\d]+)',v_viewSubjectMarks),
        url(r'^result/$',v_viewResult),
        
        #url(r'^manage/subject/$',v_manageSubjectList),
        
        
        url(r'^timetable/$',v_schedulePeriod),
        #url(r'^timetable/$',v_createTimeTable),
        #url(r'^timetable/([\d]+)/([\d]+)/$',v_editTimeTable),
        url(r'^studPerformance/$',v_studPerformance),
        
        #----------------------------------------------------------manav
        
        url(r'^student/add/$',v_addStudent),
        url(r'^student/edit/([\d]+)/',v_editStudent),
        url(r'^students/$',v_student),
        url(r'^search/student/$',v_searchStudent),
        url(r'^Nextstudent/([\d]+)/',v_nextStudent),
        url(r'^Prevstudent/([\d]+)/',v_prevStudent),
        
        url(r'^mediums/$',v_medium),
        #url(r'^medium/add/$',v_addMedium),
        url(r'^medium/edit/([\d]+)/',v_editMedium),
        url(r'^subjects/$',v_subject),
        url(r'^subject/add/$',v_addsubject),
        url(r'^subject/edit/([\d]+)/',v_editsubject),
        url(r'^sections/$',v_section),
        
        url(r'^section/edit/([\d]+)/',v_editsection),
        url(r'^standards/$',v_standard),
        url(r'^standard/add/$',v_addStandard),
        url(r'^standard/edit/([\d]+)/$',v_editStandard),
        
        
        url(r'^accMresponder/$',v_accMresponder),
        
        url(r'^add/(.+)/',v_popUp),
        
        
        url(r'^responderM/',v_responder1),
        url(r'^attendence/add/$',v_addAttendence),
        url(r'^holidays/$',v_holidays),
        url(r'^holidays/(.+)/$',v_Yearholidays),
        url(r'^Nextholidays/([\d]+)/(.+)/',v_nextHolidays),
        url(r'^Prevholidays/([\d]+)/(.+)/',v_prevHolidays),
        url(r'^holiday/add/$',v_addHoliday),
        url(r'^holiday/edit/(.+)/$',v_editHoliday),
        
        url(r'^attendences/$',v_attendence),
        url(r'^attendence/data/(.+)/([\d]+)/$',v_attendencedata),
        
        url(r'^attendenceM/$',v_dateattendenceRecord),
        
        
        
        
        
        
        
        url(r'^feeCategory/$',v_feeCategory),
        url(r'^feeCategory/add/$',v_AddfeeCategory),
        url(r'^feeCategory/edit/([\d]+)/$',v_Editfeecategory),
        url(r'^assignFees/add/$',v_addassignFees),
        
        url(r'^assignFees/$',v_assignFees),
        url(r'^assignFees/(.+)/$',v_assignSessionFees),
        
        url(r'^feePayment/$',v_feePayment),
        url(r'^feePayment/add/([\d]+)/$',v_feePaymentAdd),
        url(r'^feePayment/edit/([\d]+)/$',v_feePaymentedit),
        url(r'^generatefeeslip/$',v_generateslip),
        
        
        url(r'^NextfeePayment/([\d]+)/',v_nextfeePayment),
        url(r'^PrevfeePayment/([\d]+)/',v_prevfeePayment),
        url(r'^pendingfee/$',v_feePending),
        url(r'^school/$',v_school),
        url(r'^school/add/$',v_addSchool),
        url(r'^school/edit/([\d]+)/$',v_editSchool),
        
        url(r'^studentsibling/',v_studentSibling),
        
        
        url(r'^report/attendence/$',v_viewAttendenceReport),
        
        
        
        url(r'^libItems/$',v_libItems),
        url(r'^NextlibItems/([\d]+)/$',v_NextlibItems),
        url(r'^PrevlibItems/([\d]+)/$',v_PrevlibItems),
        
        url(r'^libItem/add/$',v_addLibItem),
        url(r'^libItem/edit/([\d]+)/$',v_editLibItem),
        url(r'^libItem/viewall/([\d]+)/$',v_libItemViewAll),
        
        
        
        url(r'^libMembers/$',v_libMembers),
        url(r'^NextlibMembers/([\d]+)/$',v_nextlibMembers),
        url(r'^PrevlibMembers/([\d]+)/$',v_prevlibMembers),
        url(r'^libMember/add/$',v_addLibMember),
        url(r'^libMember/edit/([\d]+)/$',v_editLibMember),
        
        url(r'^libPersonDetail/$',v_getPersonDetail),
        
        url(r'^manageStocks/$',v_libmanagestock),
        url(r'^NextmanageStocks/([\d]+)/$',v_Nextlibmanagestock),
        url(r'^PrevmanageStocks/([\d]+)/$',v_Prevlibmanagestock),
        url(r'^libstock/modify/([\d]+)/$',v_libstockmodify),
        url(r'^libstock/history/([\d]+)/$',v_libstockhistory),
        url(r'^stockdeducted/([\d]+)/$',v_libdeducthistory),
        
        
        url(r'^Issues/$',v_itemIssues),
        url(r'^nextIssues/([\d]+)/$',v_nextitemIssues),
        url(r'^prevIssues/([\d]+)/$',v_previtemIssues),
        url(r'^libItemSearch/$',v_libItemSearch),
        url(r'^libItemIssue/add/([\d]+)/$',v_addIssue),
        url(r'^libItemIssue/edit/([\d]+)/$',v_editIssue),
        
        
        url(r'^studPromote/$',v_studPromote),
        url(r'^promoteStudDetails/$',getdatatopromote),
        url(r'^getstudM/$',getstudents),
        url(r'^studentHistory/$',v_studHistory),
        
        url(r'^stud/History/([\d]+)/',v_viewstudRecord),
        url(r'^NextstudHistory/([\d]+)/',v_nextstudHistory),
        url(r'^PrevstudHistory/([\d]+)/',v_prevstudHistory),
        url(r'^stud/data/(.+)/([\d]+)/',v_studRecordYearWise),
        #url(r'^xxx/$',v_addData),
        #url(r'^standard/adding/$',v_addXXX),
        url(r'^grading/$',v_grading),
        url(r'^grades/add/$',v_addGrades),
        url(r'^grades/edit/$',v_editGrades),
        
        
        url(r'^examType/$',v_examType),
        
        url(r'^examType/edit/([\d]+)/$',v_editExamType),
        
        url(r'^assignRollNo/$',v_assignRollNo),
        
        url(r'^notice/',v_Notice),    
        url(r'^myaccount/',v_user_detail),
        
    )

else:
    admin.autodiscover()
    urlpatterns = patterns('',
        #url(r'^admin/', include(admin.site.urls)),
        url(r'^trial/$',v_trial),
        url(r'^activate/',v_activate),
        url(r'^done/',lambda req:render_to_response("thank.html")),
        url(r'',lambda req:render_to_response("startup.html")),
    )