from django.shortcuts import render_to_response
from views.permission import i_hasPermission
from App.models import tbl_systemUser, tbl_MSS, tbl_subject, tbl_timeTable,\
    tbl_teacher, tbl_subjectAndTeacher
from django.http import HttpResponse
from django.template.context import RequestContext

def v_schedulePeriod(req):
    '''
    timetable rows created only once for a mss you schedule ,of alldays and allperiods either has subject or not(subject=-1) , editing same mss will not delete any rows only edit 
    '''
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'schedule','a'):
        classes=[c for c in tbl_MSS.objects.filter(isActive=True).order_by('standard')]
        showPeriod={1:'1st',2:'2nd',3:'3rd',4:'4th',5:'5th',6:'6th',7:'7th',8:'8th',9:'9th',10:'10th',11:'11th',12:'12th',13:'13th',14:'14th',15:'15th',16:'16th',17:'17th',18:'18th',19:'19th',20:'20th'}
        days={1:'MON',2:'TUE',3:'WED',4:'THU',5:'FRI',6:'SAT',7:'SUN'}
        
        try:
            '''
            shared for both cases given below 
            '''
            mss=int(req.POST.get('mss',-1))
            subjects=tbl_subject.objects.filter(standards=tbl_MSS.objects.get(id=mss).standard)
            oldData=tbl_timeTable.objects.filter(mss=mss)
        except:
            pass
        
        
        if req.POST.get('load_button'):
            dataRows=[]
            for d in days:
                temp=[]
                temp.append(d)
                temp.append(days[d])
                periodSubjects=[]
                for p in range(1,tbl_MSS.objects.get(id=mss).standard.period+1):
                    try:
                        periodSubjects.append(str(oldData.get(day=d,period=p).subject))
                    except tbl_timeTable.DoesNotExist:
                        periodSubjects.append('-1')
                temp.append(periodSubjects)    
                dataRows.append(temp)
        
            #return HttpResponse(str(dataRows))
            return render_to_response('schedule.html',locals(),context_instance=RequestContext(req))
        
        elif req.POST.get("save_button"):
            '''
            dataRow is 2d array of 1-d
            each single 1-d array is represent one row of form data and has format like this
            dataRow=[ [ day(int) ,day(name),[hindi,java,...]] , ..]
            '''
            errors=[]
            if mss==-1:
                errors.append('please select at least one class !')
            
            '''
            persist data on form after save clicked 
            '''
            dataRows=[]
            for d in days:
                temp=[]
                temp.append(d)
                temp.append(days[d])
                periodSubjects=[]
                for p in range(1,tbl_MSS.objects.get(id=mss).standard.period+1):
                    periodSubjects.append(str(req.POST.get('day_'+str(d)+'_period_'+str(p),'-1')))
                
                temp.append(periodSubjects)    
                dataRows.append(temp)
            
            if not errors:
                #return HttpResponse(str(dataRows));
                for dayNo,dayName,_subjects in dataRows:
                    for p,s in enumerate(_subjects):
                        '''
                        if timetable row for ( same day and period ) aleady exist then modify the same 
                        else create new one in except clause
                        '''
                        try:
                            ttRow=oldData.get(day=dayNo,period=p+1)
                            ttRow.subject=s
                            if s=='-1':
                                ttRow.teacher=None
                            ttRow.save()
                        except tbl_timeTable.DoesNotExist:
                            
                            if s!='-1':
                                sAt=tbl_subjectAndTeacher(mssId=mss,subject=s)
                                if sAt:
                                    tbl_timeTable.objects.create(mss=tbl_MSS.objects.get(id=mss),day=dayNo,period=p+1,subject=s,teacher=tbl_teacher.objects.get(id=sAt.tid))
                            else:
                                tbl_timeTable.objects.create(mss=tbl_MSS.objects.get(id=mss),day=dayNo,period=p+1,subject=s)
                    
                return render_to_response('schedule.html',locals(),context_instance=RequestContext(req))
        return render_to_response('schedule.html',locals(),context_instance=RequestContext(req))