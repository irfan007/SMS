from django.shortcuts import render_to_response
from django.template.context import RequestContext
from App.models import tbl_MSS, tbl_subjectAndTeacher,\
    tbl_student, tbl_subjectMarks, tbl_classStudent, tbl_systemUser,\
    tbl_examType, tbl_school
from django.http import HttpResponseRedirect
from datetime import datetime
from views.permission import i_hasPermission

#def v_manageSubjectList(req):
#    #if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'setting','v'):
#    classes=[c for c in tbl_MSS.objects.filter(isActive=True).order_by('standard__name') if c.subjectAndTeachers.all()]
#    return render_to_response('manageSubjectList.html',locals(),context_instance=RequestContext(req))
#
#
#
#
#def v_manageSubjectAndTeacher(req):
#    classes=tbl_MSS.objects.filter(isActive=True)
#    EP=EMPLOYEE_PREFIX
#    if req.POST.get('manageSubjectAndTeacher'):
#        errors=[]
#        mss=int(req.POST.get('mss',-1))
#        try:
#            allSubject=tbl_subject.objects.filter(standards=tbl_MSS.objects.get(id=mss).standard)
#            rows=[[s.id,s.name.title(),int(req.POST.get('t_'+str(s.id),-1)),int(req.POST.get('ct_'+str(s.id),0))] for s in allSubject]
#        except:
#            pass
#        teachers=tbl_teacher.objects.filter(isActive=True)
#        if mss==-1:
#            errors.append("please select a class !")
##        elif tbl_MSS.objects.get(id=mss).subjectAndTeachers.all():
##            errors.append("teachers for class has already been assigned you can edit it from listing !")
#        elif not allSubject:
#            errors.append("no subjects added in selected class, please add first !")
#        else:
#            ct=0
#            for r in rows:
#                
#                if r[3]==1:
#                    ct=ct+1
#                    if ct>1:
#                        errors.append("class can have only one class teacher !")
#                elif r[3] and r[2]==-1:
#                    errors.append("please choose a teacher for "+r[1]+" subject !")
#        if not errors:
#            for r in rows:
#                mssObj=tbl_MSS.objects.get(id=mss)
#                mssObj.subjectAndTeachers.all().delete()
#                
#                sAtObj=tbl_subjectAndTeacher.objects.create(mssId=mss,tid=r[2],subject=r[1],ifCT=bool(r[3]))
#                mssObj.subjectAndTeachers.add(sAtObj)
#            return HttpResponseRedirect('/manage/subject/')
#        return render_to_response('manageSubjectAdd.html',locals(),context_instance=RequestContext(req))
#    return render_to_response('manageSubjectAdd.html',locals(),context_instance=RequestContext(req))


#def v_manageSubjectEdit(req,_mssId):
#    mss=tbl_MSS.objects.get(id=_mssId)
#    teachers=tbl_teacher.objects.filter(isActive=True)
#    EP=EMPLOYEE_PREFIX
#    
#    try:
#        allSubject=tbl_subject.objects.filter(standards=mss.standard)
#        rows=[[s.id,s.name.title(),tbl_subjectAndTeacher.objects.get(mssId=mss.id,subject=s.name).tid,tbl_subjectAndTeacher.objects.get(mssId=mss.id,subject=s.name).ifCT] for s in allSubject]
#    except:
#        pass
#    
#    if req.POST.get('manageSubjectEdit'):
#        errors=[]
#        rows=[[s.id,s.name.title(),int(req.POST.get('t_'+str(s.id),-1)),int(req.POST.get('ct_'+str(s.id),0))] for s in allSubject]
#        
#        ct=0
#        for r in rows:
#            if r[2]==-1:
#                errors.append("please choose a teacher for "+r[1]+" subject !")
#            if r[3]==1:
#                ct=ct+1
#                if ct>1:
#                    errors.append("please mark only one class teacher !")
#
#        if not errors:
#            mss.subjectAndTeachers.all().delete()
#            for r in rows:
#                sAtObj=tbl_subjectAndTeacher.objects.create(mssId=mss.id,tid=r[2],subject=r[1],ifCT=bool(r[3]))
#                mss.subjectAndTeachers.add(sAtObj)
#            return HttpResponseRedirect('/manage/subject/')
#        return render_to_response('manageSubjectEdit.html',locals(),context_instance=RequestContext(req))
#    return render_to_response('manageSubjectEdit.html',locals(),context_instance=RequestContext(req))

def v_addSubjectMarks(req,_sAtId):
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'teacher','a'):
        
        errors=[]
        sAtObj=tbl_subjectAndTeacher.objects.get(id=_sAtId)
        MSS=tbl_MSS.objects.get(id=sAtObj.mssId)
        rows=[[s.studentId,tbl_student.objects.get(id=s.studentId).getName(),s.rollNo,'',False]for s in MSS.students.all()]
        examTypes=tbl_examType.objects.all()
        
        for r in rows:
            try:
                r[3]=int(req.POST.get('marks_'+str(r[0])))
                r[4]=bool(req.POST.get('absent_'+str(r[0]),0))
            except:
                pass
    
        
        if req.POST.get('addMarks'):
            
            title=req.POST.get('title',None)
            testdate=req.POST.get('testdate',None)
            
            maximum=req.POST.get('maximum')
            minimum=req.POST.get('minimum')
            
            
                
            if not title:
                errors.append("Please select exam type !")
            elif sAtObj.subjectResults.filter(testName=title,hasSession=tbl_school.objects.all()[0].getSession()):
                errors.append("Marks of  '"+sAtObj.subject+"' for exam '"+title.title()+"' already uploaded !")
            elif not testdate:
                errors.append("Please enter date of test !")
            elif not maximum:
                errors.append("Please enter maximum marks for test !")
            elif int(maximum) <=0:
                errors.append("Please enter valid maximum marks for test !")
            elif not minimum:
                errors.append("Please enter minimum marks for test !")
            elif not 0<=int(minimum)<=int(maximum):
                errors.append("Please enter valid passing marks !")
            else:
                maximum=int(maximum)
                minimum=int(minimum)
                
                try:
                    datetime.strptime(testdate,'%d-%m-%Y')
                except:
                    errors.append("Please enter a valid date of test !")
                
                for r in rows:
                    if req.POST.get('marks_'+str(r[0])):
                        r[3]=int(req.POST.get('marks_'+str(r[0])))
                        if not 0<=r[3]<=maximum:
                            errors.append('please enter a valid marks for '+str(r[2])+' !')
                        else:
                            if bool(req.POST.get('absent_'+str(r[0]),0)):
                                errors.append('please uncheck absent for '+str(r[2])+' !')
                            
                    else:
                        if bool(req.POST.get('absent_'+str(r[0]),0)):
                            r[4]=True
                            r[3]=-1
                        else:    
                            errors.append('please enter marks for '+str(r[2])+' !') 
                            
                            
                
                    
                                       
                    
            if not errors:
                '''
                marks={class Student Id:subject marks,....}
                detail="{'total':100,'pass':75,'fail':23},'absent':2,'max':100,'min':35"}
                rows=[[s.id,tbl_student.objects.get(id=s.studentId).getName(),s.rollNo,'',False]for s in MSS.students.all()]
                '''
                marksData={}
                aggregateData={}
                
                pass_=0
                fail_=0
                absent_=0
                for r in rows:
                    marksData[int(r[0])]=r[3]
                    if r[3]>=minimum:
                        pass_=pass_+1
                    else:
                        if r[3]==-1:
                            absent_=absent_+1
                        else:
                            fail_=fail_+1
                
                aggregateData['total']=MSS.students.count()
                aggregateData['pass']=pass_
                aggregateData['fail']=fail_
                aggregateData['absent']=absent_
                aggregateData['max']=maximum
                aggregateData['min']=minimum
                
                #return HttpResponse(str(aggregateData))
                sm=tbl_subjectMarks.objects.create(hasSession=tbl_school.objects.all()[0].getSession(),mssId=sAtObj.mssId,tid=sAtObj.tid,subject=sAtObj.subject,testName=title,testDate=datetime.strptime(testdate,'%d-%m-%Y'),marks=str(marksData),detail=str(aggregateData))
                sAtObj.subjectResults.add(sm)
                sAtObj.hasSession=tbl_school.objects.all()[0].getSession()
                sAtObj.save()
                return HttpResponseRedirect('/result/subject/'+str(sm.id))
        return render_to_response('addSubjectMarks.html',locals(),context_instance=RequestContext(req))
    



def v_viewSubjectMarks(req,_smId):
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'teacher','v'):
        
        sm=tbl_subjectMarks.objects.get(id=_smId)
        mss=tbl_MSS.objects.get(id=sm.mssId)
        detail=eval(sm.detail)
        d=eval(sm.marks)
        
        '''
        data row format
        [    full Name    ,    rollNo    ,    marks    ,    is fail    ]
        '''
        data=[]
        for k in sorted(d):
            temp=[]
            pDetail=tbl_student.objects.get(id=k).perDetail
            temp.append(tbl_classStudent.objects.get(studentId=k).rollNo)
            temp.append(pDetail.fName+" "+pDetail.lName)
            if d[k]>=detail['min']:
                temp.append(d[k])
                temp.append(False)
            else:
                if d[k]==-1:
                    temp.append("ABSENT")
                    temp.append(False)
                else:
                    temp.append(d[k])
                    temp.append(True)
            data.append(temp)
        
        return render_to_response('viewSubjectMarks.html',locals(),context_instance=RequestContext(req))