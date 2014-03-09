from django.shortcuts import render_to_response
from django.template.context import RequestContext
from App.models import tbl_MSS, tbl_examType, tbl_stdPersonalDetail, tbl_subject,\
    tbl_subjectMarks, tbl_systemUser, tbl_grades
from views.permission import i_hasPermission

def hasGrade(marks):
    allRows=tbl_grades.objects.all()
    for d in allRows:
        if marks<=d.start:
            if marks>d.end:
                return d.name


def v_viewResult(req):
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'teacher','v'):
        classes=tbl_MSS.objects.filter(isActive=True)
        exams=tbl_examType.objects.all()
        
        
        if req.POST.get('result',''):
            
            errors=[]
            mss_id=int(req.POST.get('mss_id',-1))
            exam_id=int(req.POST.get('exam_id',-1))
            classStudent_id=int(req.POST.get('classStudent_id',-1))
            try:
                exam=tbl_examType.objects.get(id=exam_id)
                subjectMarks=tbl_subjectMarks.objects.filter(mssId=mss_id,testName=exam.name);
            except:
                pass
            
            if exam_id==-1:
                errors.append("please select exam !")
            elif mss_id==-1:
                errors.append("please select class !")
            elif classStudent_id==-1:
                errors.append("please select roll no. !")
            elif not subjectMarks:
                errors.append("No result found !")
            if not errors:
                
                mssObj=tbl_MSS.objects.get(id=mss_id)
                students=mssObj.students.all()
                classStudentObj=students.get(id=classStudent_id)
                name=tbl_stdPersonalDetail.objects.get(id=classStudentObj.studentId).getName()
                
                
                subjects=tbl_subject.objects.filter(standards=mssObj.standard)
                
                '''
                data=[['subject','max','min','obtained'], ...]
                '''
                data=[]
                maxSum=0
                obtainedSum=0
                resultStatus=1
                for s in subjects:
                    try:
                        sm=subjectMarks.get(subject=s.name)
                        detail=eval(sm.detail)
                        marks=eval(sm.marks)
                        if marks[classStudentObj.studentId]>=detail['min']:
                            data.append([sm.subject,1,detail['max'],detail['min'],marks[classStudentObj.studentId]])
                        else:
                            if marks[classStudentObj.studentId]==-1:
                                data.append([sm.subject,-1,detail['max'],detail['min'],marks[classStudentObj.studentId]])
                            else:
                                data.append([sm.subject,0,detail['max'],detail['min'],marks[classStudentObj.studentId]])
                            resultStatus=0
                            
                        
                        maxSum=maxSum+detail['max']
                        if marks[classStudentObj.studentId]!=-1:
                            obtainedSum=obtainedSum+marks[classStudentObj.studentId]
                    except:
                        pass
                
                result={'maxSum':maxSum,'obtainedSum':obtainedSum,'status':resultStatus,'percent':int(float(obtainedSum)/maxSum*100),'stdGrade':hasGrade(int(float(obtainedSum)/maxSum*100))}
                
    
            
            return render_to_response('result.html',locals(),context_instance=RequestContext(req))
        return render_to_response('result.html',locals(),context_instance=RequestContext(req))