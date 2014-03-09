from App.models import tbl_location, tbl_subject, tbl_MSS,\
    tbl_teacher, tbl_employee, tbl_systemUser, tbl_standard,\
    tbl_subjectAndTeacher, tbl_timeTable, tbl_events
from django.http import HttpResponse
from SMS.settings import  EMPLOYEE_PREFIX



def v_responder(req):
    if req.GET.get('updateCal',''):
        data=req.GET.get('updateCal','')
        
        res="ok"
        try:
            # d is list has format [title,start date (as 2013-12-4 0:0),end date,foregroundColor,backgroundColor]
            tbl_events.objects.filter(username=req.session['username']).delete()
            for title,sd,ed,fc,bc,type in eval(data):
                try:
                    if type!='n':
                        import datetime
                        tbl_events.objects.create(username=req.session['username'],event=title,startDate=datetime.datetime.strptime(sd,"%Y-%m-%d %H:%M"),endDate=datetime.datetime.strptime(ed,"%Y-%m-%d %H:%M"),fgColor="#"+fc,bgColor="#"+bc)
                except:
                    pass
        except SyntaxError:
            res="error"
        return HttpResponse(res)
    elif req.GET.get('country',''):
        states=tbl_location.objects.filter(pid=(int(req.GET.get('country','')))).order_by('name')
        template="<div class='selectWidth1' id='statediv'>\n<select class='full' name='state' onchange='getCity(this.value)'>\n\
        <option value='-1'> ---- </option>\n"
        if states:
            for s in states:
                template=template+"<option value='"+str(s.id)+"'>"+s.name.title()+"</option>\n"
        else:
            template=template+"<option value='-1'> not found !</option>\n"
        template=template+"</select>\n</div>"
        return HttpResponse(template)
    elif req.GET.get('state',''):
        cities=tbl_location.objects.filter(pid=(int(req.GET.get('state','')))).order_by('name')
        template="<div class='selectWidth1' id='citydiv'>\n<select class='small' name='city' onchange='getArea(this.value)'>\n<option value='-1' >Select City</option>"
        if cities:
            for c in cities:
                template=template+"<option value='"+str(c.id)+"'>"+c.name.title()+"</option>\n"
        else:
            template=template+"<option value='-1'> not found !</option>\n"
        template=template+"</select>\n</div>"
        return HttpResponse(template)
    elif req.GET.get('lstate',''):
        cities=tbl_location.objects.filter(pid=(int(req.GET.get('lstate','')))).order_by('name')
        template="<div class='selectWidth1' id='citydiv'>\n<select class='small' name='lcity' onchange='getArea(this.value)'>\n<option value='-1' >Select City</option>"
        if cities:
            for c in cities:
                template=template+"<option value='"+str(c.id)+"'>"+c.name.title()+"</option>\n"
        else:
            template=template+"<option value='-1'> not found !</option>\n"
        template=template+"</select>\n</div>"
        return HttpResponse(template)
    elif req.GET.get('pstate',''):
        cities=tbl_location.objects.filter(pid=(int(req.GET.get('pstate','')))).order_by('name')
        template="<div class='selectWidth1' id='citydiv'>\n<select class='small' name='pcity' onchange='getArea(this.value)'>\n<option value='-1' >Select City</option>"
        if cities:
            for c in cities:
                template=template+"<option value='"+str(c.id)+"'>"+c.name.title()+"</option>\n"
        else:
            template=template+"<option value='-1'> not found !</option>\n"
        template=template+"</select>\n</div>"
        return HttpResponse(template)
    elif req.GET.get('getSubjectOfClass',''):
        Subjects=tbl_subject.objects.filter(standards=tbl_MSS.objects.get(id=req.GET.get('getSubjectOfClass','')).standard)
        #return HttpResponse(str(allSubject))
        
        template="<div class='selectWidth1' id='classSubject_div'>\n<select class='medium' name='subject_id' >\n<option value='-1' >Select Subject</option>"
        if Subjects:
            for s in Subjects:
                template=template+"<option value='"+str(s.id)+"'>"+s.name.title()+"</option>\n"
        else:
            template=template+"<option value='-1'> not found !</option>\n"
        template=template+"</select>\n</div>"
        return HttpResponse(template)
    elif req.GET.get('getStudentsOfClass',''):
        students=tbl_MSS.objects.get(id=req.GET.get('getStudentsOfClass','')).students.all()
        #return HttpResponse(str(allSubject))
        
        template="<div class='selectWidth1' id='classStudents_div'>\n<select class='medium' name='classStudent_id' >\n<option value='-1' >Select Students</option>"
        if students:
            for s in students:
                template=template+"<option value='"+str(s.id)+"'>"+s.rollNo.upper()+"</option>\n"
        else:
            template=template+"<option value='-1'> not found !</option>\n"
        template=template+"</select>\n</div>"
        return HttpResponse(template)
    elif req.GET.get('class',''):
        mssID=int(req.GET.get('class',''))
        allSubject=tbl_subject.objects.filter(standards=tbl_MSS.objects.get(id=mssID).standard)
        try:
            mssSAT=tbl_subjectAndTeacher.objects.filter(mssId=mssID)
        except:
            pass
        
        rows=[]
        for s in allSubject:
            temp=[]
            temp.append(s.id)
            temp.append(s.name.title())
            try:
                temp.append(mssSAT.get(mssId=mssID,subject=s.name).tid)
                temp.append(mssSAT.get(mssId=mssID,subject=s.name).ifCT)
            except:
                temp.append(-1)
                temp.append(0)
            rows.append(temp)
        
        
        teachers=tbl_teacher.objects.filter(isActive=True)
        #return HttpResponse(teachers)
        template="<table class='table table-bordered table-striped'  width='100%'>\
                    <thead align='center' >\
                        <tr class='tr_bg_list'>\
                            <td width='%'>Subject</td>\
                            <td width='%'>Assigned Teacher</td>\
                            <td width='%'>Class Teacher</td>\
                        </tr>\
                    </thead>\
                    <tbody align='center' class='font_wght'>"
        
        
        for r in rows:
            template=template+"\
        <tr class='font_wght'>\n\
            <td>"+str(r[1])+"</td>\n\
            <td>\n\
                <select class='medium'  name='t_"+str(r[0])+"'>\n\
                    <option value='-1'  selected>Select Teacher</option>\n"
            
            for t in teachers:
                emp=tbl_employee.objects.get(id=t.empId)
                if r[2]==t.id:
                    template=template+"\n\
                        <option value='"+str(t.id)+"' selected>"+emp.perDetail.fName+" "+emp.perDetail.lName+" / "+EMPLOYEE_PREFIX+str(emp.id)+"</option>\n"
                else:
                    template=template+"\n\
                        <option value='"+str(t.id)+"' >"+emp.perDetail.fName+" "+emp.perDetail.lName+" / "+EMPLOYEE_PREFIX+str(emp.id)+"</option>\n"
            
            if not teachers:
                template=template+"\n\
                    <option value='-1' > teacher not defined ! </option>\n"
            
            template=template+"\n\
                </select>\n\
            </td>\n\
            <td>\n"
            if r[3]:
                template=template+"\n\
                <input type='checkbox' name='ct_"+str(r[0])+"' value='1' checked />\n"
            else:
                template=template+"\n\
                <input type='checkbox' name='ct_"+str(r[0])+"' value='1'  />\n"
            template=template+"\n\
            </td>\n\
        </tr>\n"
        
        template=template+"\
        </tbody>\
        </table>"
        return HttpResponse(template)
    elif req.GET.get('popUser',''):
        users=tbl_systemUser.objects.filter(isActive=True,isSuper=False)
        template="<select class='small' name='user' >\n\
        <option value='-1' selected>Select User</option>"
        if users:
            for u in users:
                if u.id==int(req.GET.get('popUser','')):
                    template=template+"<option value='"+str(u.id)+"' selected>"+u.username+"</option>\n"
                else:
                    template=template+"<option value='"+str(u.id)+"' >"+u.username+"</option>\n"
        else:
            template=template+"<option value='-1'> not found !</option>\n"
        template=template+"</select>"
        return HttpResponse(template)
    elif req.GET.get('periodofclass',''):
        
        showPeriod={1:'1st',2:'2nd',3:'3rd',4:'4th',5:'5th',6:'6th',7:'7th',8:'8th',9:'9th',10:'10th',11:'11th',12:'12th',13:'13th',14:'14th',15:'15th',16:'16th',17:'17th',18:'18th',19:'19th',20:'20th'}
        allSubject=tbl_subject.objects.filter(standards=tbl_MSS.objects.get(id=req.GET.get('periodofclass','')).standard)
        totalPeriod=tbl_MSS.objects.get(id=req.GET.get('periodofclass','')).standard.period
        template="<table class='table table-bordered table-striped'  width='100%'>\
                    <thead align='center' >\
                        <tr class='tr_bg_list'>\
                             <td width='32%'>Period</td>\
                             <td width='32%'>Subject</td>\
                             <td width='36%'>Assigned Teacher</td>\
                        </tr>\
                    </thead>\
                    <tbody align='center' class='font_wght'>"
        for p in range(1,totalPeriod+1):
            template=template+"\
        <tr class='font_wght'>\n\
            <td>"+showPeriod[p]+"</td>\n\
            <td>\n\
                <select class='medium'  name='subject_"+str(p)+''''  onchange="getTeacher(document.getElementById('id_mss').value,this.value,'''+str(p)+''');">\n\
                    <option value='-1'  selected>Select Subject</option>\n'''
            
            for s in allSubject:
                template=template+"\n\
                    <option value='"+str(s.name)+"'>"+s.name.upper()+"</option>\n"
            
            if not allSubject:
                template=template+"\n\
                    <option value='-1' > no subject found for class ! </option>\n"
            
            template=template+"\n\
                </select>\n\
            </td>\n\
            <td>\n\
            <label id='tName_"+str(p)+"'></label>\n\
            <input type='hidden' value='' name='teacher_"+str(p)+"' id='teacher_id_"+str(p)+"'>\n\
            <input type='hidden' value='' name='teacher_for_id_"+str(p)+"' id='teacher_has_id_"+str(p)+"'>\n\
            </td>\n\
        </tr>\n"
        
        template=template+"\
        </tbody>\
        </table>"
        return HttpResponse(template)
    elif req.GET.get('teacherofsubjectofclass',''):
        try:
            subjectOfclass=req.GET.get('teacherofsubjectofclass','').split('of')
            tid=tbl_subjectAndTeacher.objects.get(subject=subjectOfclass[0],mssId=subjectOfclass[1]).tid
            t=tbl_teacher.objects.get(id=tid)
            return HttpResponse(EMPLOYEE_PREFIX+str(t.empId)+" / "+t.getFullName()+':'+str(t.id))
        except:
            return HttpResponse("----:")
   
    elif req.GET.get('hastimetableofmssofday',''):
        try:
            req.GET.get('hastimetableofmssofday','')
            if tbl_timeTable.objects.filter(mss=req.GET.get('hastimetableofmssofday','').split(':')[0],day=req.GET.get('hastimetableofmssofday','').split(':')[1]):
                return HttpResponse('yes')
            else:
                return HttpResponse('no')
        except:
            return HttpResponse('no')
    
    
    
    elif req.GET.get('getBlockByStandardNameAndMedium',''):
        EP=EMPLOYEE_PREFIX
        standardName=req.GET.get('getBlockByStandardNameAndMedium').split(':')[0]
        standardMedium=req.GET.get('getBlockByStandardNameAndMedium').split(':')[1]
        template=''
        teachers=tbl_teacher.objects.filter(isActive=True)
        allSubject=tbl_subject.objects.filter(standards=tbl_standard.objects.get(name=standardName,medium__name=standardMedium))
        
        mssesByStandard=tbl_MSS.objects.filter(standard__name=standardName,medium__name=standardMedium)
        
        uniqueSections=[]    
        for standard in tbl_standard.objects.filter(name=standardName,medium__name=standardMedium):
            for section in standard.sections.all():
                uniqueSections.append(section.name)
        uniqueSections=sorted(uniqueSections)
        
        
        dataRows=[]
        '''
        dataRows has format 
        [subject id , subject name ,[mss id ,...]]
        '''
        #return HttpResponse(mssesByStandard[0].section.name)
        #return HttpResponse(uniqueSections)
        for s in allSubject:
            temp1=[]
            temp1.append(s.id)
            temp1.append(s.name.title())
            temp2=[]
            for section in uniqueSections:
                temp2.append(int(mssesByStandard.get(section__name=section).id))
            temp1.append(temp2)
            dataRows.append(temp1)
            
        
        if allSubject:
                
            template=template+"\n\
            <table class='table table-bordered table-striped'   width='100%' border=''>\n\
                <thead align='center'>\n\
                    <tr class='tr_bg_list'>\n\
                        <td width=''>Subject</td>\n"
            
            for sec in uniqueSections:
                template=template+"\n\
                        <td width=''>SECTION ("+sec+")</td>"
            
            template=template+"\n\
                    </tr>\n\
                </thead>\n"
            
        
        
        #return HttpResponse(str(dataRows))
        template=template+"\n\
            <tbody align='center' class='font_wght'>\n"
            
            
        for r in dataRows:
            template=template+"\n\
            <tr class='font_wght'>\n\
                    <td>"+r[1]+"</td>\n"
            
            
            #return HttpResponse(str(r))
            
            for mssid in r[2]:
                template=template+"\n\
                    <td>\n\
                    <select class='small' name='tid_of_"+str(r[0])+":"+str(mssid)+"' value='-1'>\n\
                        <option value='-1'  selected>Select Teacher</option>\n"
                for t in teachers:
                    try:
                        if mssesByStandard.get(id=mssid).subjectAndTeachers.get(subject=r[1]).tid==t.id:
                            template=template+"\n\
                            <option value='"+str(t.id)+"' selected>"+(t.getFullName())+" / "+EP+str(t.empId)+"</option>\n"
                        else:
                            template=template+"\n\
                            <option value='"+str(t.id)+"' >"+(t.getFullName())+" / "+EP+str(t.empId)+"</option>\n"
                    except:
                        template=template+"\n\
                        <option value='"+str(t.id)+"' >"+(t.getFullName())+" / "+EP+str(t.empId)+"</option>\n"
                
                if not teachers:
                    template=template+"\n\
                    <option value='-1'  >not found</option>\n"
                    
            
                template=template+"\n\
                    </select>\n\
                    </td>\n"
                
            template=template+"\n\
            </tr>\n"
       
            
        return HttpResponse(template)
    elif req.GET.get('getMediumsOfStandardName',''):
        sn=req.GET.get('getMediumsOfStandardName','')
        
        mediums=[r[0] for r in tbl_standard.objects.filter(name=sn).values_list('medium__name').distinct()]
            
        template='''<select class='small' name='mediumName' id='medium_div' onchange="getBlockByStandardNameAndMedium(document.getElementById('standard_id').value,this.value)">\n\
        <option value='-1' selected>Select User</option>'''
        if mediums:
            for m in mediums:
                template=template+"<option value='"+str(m)+"'>"+m.title()+"</option>\n"
        else:
            template=template+"<option value='-1'> not found !</option>\n"
        template=template+"</select>"
        return HttpResponse(template)        
            
        