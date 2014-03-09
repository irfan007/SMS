from django.shortcuts import render_to_response
from django.template.context import RequestContext
from App.models import tbl_MSS, tbl_subject, tbl_timeTable, tbl_teacher,\
    tbl_systemUser
from django.http import HttpResponseRedirect
from SMS.settings import EMPLOYEE_PREFIX
from views.permission import i_hasPermission


def v_createTimeTable(req):
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'schedule','a'):
        
        #if c.subjectAndTeachers.all()
        classes=[c for c in tbl_MSS.objects.filter(isActive=True).order_by('standard')]
        days={1:'MON',2:'TUE',3:'WED',4:'THU',5:'FRI',6:'SAT',7:'SUN'}
        if req.method=="POST":
            errors=[]
            mss=int(req.POST.get('mss',-1))
            day=int(req.POST.get('day',-1))
            
            showPeriod={1:'1st',2:'2nd',3:'3rd',4:'4th',5:'5th',6:'6th',7:'7th',8:'8th',9:'9th',10:'10th',11:'11th',12:'12th',13:'13th',14:'14th',15:'15th',16:'16th',17:'17th',18:'18th',19:'19th',20:'20th'}
            
            try:
                allSubject=tbl_subject.objects.filter(standards=tbl_MSS.objects.get(id=mss).standard)
                dataRows=[]
                for p in range(1,tbl_MSS.objects.get(id=mss).standard.period+1):
                    temp=[]
                    temp.append(p)
                    temp.append(showPeriod[p])
                    temp.append(req.POST.get('subject_'+str(p),None))
                    temp.append(req.POST.get('teacher_'+str(p),None))
                    temp.append(req.POST.get('teacher_for_id_'+str(p),None))
                    dataRows.append(temp)
            except:
                pass
            #return HttpResponse(str(dataRows))
            if mss==-1:
                errors.append("please select class !")
            elif day==-1:
                errors.append("please select day !")
            
            
            if not errors:
                for data in dataRows:
                    tt=tbl_timeTable(mss=tbl_MSS.objects.get(id=mss),day=day,period=data[0],subject=data[2])
                    if data[4]:
                        tt.teacher=tbl_teacher.objects.get(id=data[4])
                    tt.save()
                return HttpResponseRedirect("/timetable/"+str(mss)+'/'+str(day))
            return render_to_response('createTimeTable.html',locals(),context_instance=RequestContext(req))
        return render_to_response('createTimeTable.html',locals(),context_instance=RequestContext(req))




def v_editTimeTable(req,mss_id,day):
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'schedule','u'):
        
        classes=[c for c in tbl_MSS.objects.filter(isActive=True).order_by('standard')]
        showPeriod={1:'1st',2:'2nd',3:'3rd',4:'4th',5:'5th',6:'6th',7:'7th',8:'8th',9:'9th',10:'10th',11:'11th',12:'12th',13:'13th',14:'14th',15:'15th',16:'16th',17:'17th',18:'18th',19:'19th',20:'20th'}
        days={1:'MON',2:'TUE',3:'WED',4:'THU',5:'FRI',6:'SAT',7:'SUN'}
        
        try:
            allSubject=tbl_subject.objects.filter(standards=tbl_MSS.objects.get(id=mss_id).standard)
            dataRows=[]
            for r in tbl_timeTable.objects.filter(mss=mss_id,day=day).order_by('period'):
                temp=[]
                
                temp.append(r.period)
                temp.append(showPeriod[r.period])
                temp.append(r.subject)
                
                if r.teacher:
                    temp.append(EMPLOYEE_PREFIX+str(r.teacher.empId)+" / "+r.teacher.getFullName())
                    temp.append(r.teacher.id)
                else:
                    temp.append('----')
                    temp.append('')
                
                dataRows.append(temp)
            
        except:
            pass
        
        mss=int(mss_id)
        day=int(day)
        
        
        
        if req.method=="POST":
            errors=[]
            mss=int(req.POST.get('mss',-1))
            day=int(req.POST.get('day',-1))
            
            try:
                dataRows=[]
                for p in range(1,tbl_MSS.objects.get(id=mss).standard.period+1):
                    temp=[]
                    temp.append(p)
                    temp.append(showPeriod[p])
                    temp.append(req.POST.get('subject_'+str(p),None))
                    temp.append(req.POST.get('teacher_'+str(p),None))
                    temp.append(req.POST.get('teacher_for_id_'+str(p),None))
                    dataRows.append(temp)
            except:
                pass
            #return HttpResponse(str(dataRows))
            if mss==-1:
                errors.append("please select class !")
            elif day==-1:
                errors.append("please select day !")
            
            
            if not errors:
                tbl_timeTable.objects.filter(mss=mss,day=day).delete()
                for data in dataRows:
                    tt=tbl_timeTable(mss=tbl_MSS.objects.get(id=mss),day=day,period=data[0],subject=data[2])
                    if data[4]:
                        tt.teacher=tbl_teacher.objects.get(id=data[4])
                    tt.save()
                return HttpResponseRedirect("/timetable/"+str(mss)+'/'+str(day))
            return render_to_response('editTimeTable.html',locals(),context_instance=RequestContext(req))
    
        return render_to_response('editTimeTable.html',locals(),context_instance=RequestContext(req))
        