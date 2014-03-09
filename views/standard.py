from django.shortcuts import render_to_response, render
from App.models import tbl_class, tbl_standard, tbl_medium, tbl_shortstandard,\
    tbl_MSS, tbl_teacher, tbl_systemUser
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.template.context import RequestContext
from views.permission import i_hasPermission
def v_standard(req):
    '''
    this method will carry out listing of various standards in database
    '''
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'standard','v'): 
        rows=tbl_standard.objects.filter()
        abc=rows.values('name').annotate()
        overall=[] 
        for item in abc:
            '''
            this is used to populate data in required tabular format
            '''
            temp=[]   
            temp1=[]
            temp2=[]
            classes=rows.filter(name=item['name'])
            
            temp.append(len(classes))
            temp.append(classes[0].name)
            for data in classes:
                temp1.append(data.medium)
                
                temp1.append(data.sections.all())
                temp1.append(data.id)
                temp2.append(temp1)
                temp1=[]
            temp.append(temp2)    
            overall.append(temp)
            
        return render_to_response('standard.html',locals(),context_instance=RequestContext(req))

def v_addStandard(req):
    '''
    this will add new standard along with its medium and sections to database
    '''
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'standard','a'):
        errors=[]
        mediums=tbl_medium.objects.filter(isActive=True)
        sections=tbl_class.objects.filter(isActive=True)
        getTeachers=tbl_teacher.objects.filter(isActive=True)
        getlength=1
        lists=[]
        if req.POST.get('addStandard',''):
            
            '''
            this will carry out form validation
            '''
            getBack=True
            i=1
            getlength=int(req.POST.get('getlength',''))
            temp=[]
            overall=[]
            while i<=getlength:
                temp=[]
                name=req.POST.get('standard'+str(i),'').strip()
                temp.append(name)
                medium=int(req.POST.get('medium'+str(i),''))
                temp.append(medium)
                section=int(req.POST.get('section'+str(i),''))
                temp.append(section)
                period=req.POST.get('period'+str(i),'').strip()
                temp.append(period)
                teacher=int(req.POST.get('teacher'+str(i),''))
                temp.append(teacher)
                timePeriod=(req.POST.get('timePeriod'+str(i),'')).strip()
                temp.append(timePeriod)
                if not name:
                    errors.append("Please  enter the name")
                    
                if medium==-1:
                    errors.append("Please select the medium")
                    
                if section==-1:
                    errors.append("Please select the section")
                    
                try:
                    period=int(period)
                except:
                    errors.append("Please enter the valid periods")
                if period==0:
                    errors.append("Please enter the valid periods")
                if timePeriod:
                    try:
                        timePeriod=int(timePeriod)
                    except:
                        errors.append("Please enter the valid duration!")
                        
                if timePeriod==0:
                    errors.append("Please enter the valid duration!")
                    
                    
                i=i+1
                overall.append(temp)
            errors=set(errors)
            if errors:
                return render_to_response('addStandard.html',locals(),context_instance=RequestContext(req))
            errors=[]
            for data in overall:
                uniquedata=tbl_medium.objects.get(id=data[1])
                uniquesection=tbl_class.objects.get(id=data[2])
                standards=tbl_standard.objects.filter(name=data[0],medium=uniquedata.id)
                if standards:
                    sectionlist=standards[0].sections.all()
                    if uniquesection in sectionlist:
                        errors.append('class %s-%s-%s already exists!'%(uniquedata.name,data[0],uniquesection.name))
                        
                    else:
                        standards[0].sections.add(uniquesection)
                        standards[0].createMSS(data[4])
                else:
                    standobj=tbl_standard()
                    standobj.save()
                    standobj.name=data[0]
                    try:
                        data[5]=int(data[5])
                        standobj.timePeriod=data[5]
                    except:
                        pass
                    standobj.medium=uniquedata
                    standobj.period=data[3]
                    standobj.sections.add(uniquesection)
                    standobj.save()
                    standobj.createshortstandard()
                    standobj.createMSS(data[4])
                    
                    
            if errors:
                return render_to_response('addStandard.html',locals(),context_instance=RequestContext(req))
            else:
                return HttpResponseRedirect('/standards/')
        return render_to_response('addStandard.html',locals(),context_instance=RequestContext(req))
def v_editStandard(req,para):
    '''
    this method is used to update/view the existing standard details
    '''
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'standard','u'):
        para=int(para)
        getTeachers=tbl_teacher.objects.filter(isActive=True)
        
        uniqueobj=tbl_standard.objects.get(id=para)
        mssrows=tbl_MSS.objects.filter(isActive=True,standard=uniqueobj,medium=uniqueobj.medium)
        
        temp=[]
        overall=[]
        errors=[]
        if req.POST.get('editStandard',''):
            '''
            performing form validation
            '''
            i=1
            
            getBack=True
            for values in mssrows:
                temp=[]
                period=req.POST.get('period'+str(values.id),'').strip()
                teacher=int(req.POST.get('teacher'+str(values.id),''))
                
                
                timePeriod=(req.POST.get('timePeriod'+str(values.id),'')).strip()
                status=int(req.POST.get('status'+str(values.id),''))
                try:
                    period=int(period)
                    
                except:
                    errors.append('Please enter the valid periods')
                if period==0:
                    errors.append('Please enter the valid periods!')
                if timePeriod:
                    try:
                        timePeriod=int(timePeriod)
                    except:
                        errors.append('Please enter the valid duration!')
                if timePeriod==0:
                    errors.append('Please enter the valid duartion!')
                            
                temp.append(uniqueobj.name)
                temp.append(uniqueobj.medium.name)
                temp.append(values.section.name)
                temp.append(period)
                temp.append(teacher)
                temp.append(timePeriod)
                temp.append(status)
                temp.append(values.id)
                overall.append(temp)
            #return HttpResponse(overall)
            if errors:
                return render_to_response('editStandard.html',locals(),context_instance=RequestContext(req))
            else:
                uniqueobj.sections=[]
                
                for values in mssrows:# this help to iterate through various rows
                    '''
                    now updating database with new values
                    '''
                    period=int(req.POST.get('period'+str(values.id),'').strip())
                    teacher=int(req.POST.get('teacher'+str(values.id),''))
                    
                    temp.append(teacher)
                    timePeriod=req.POST.get('timePeriod'+str(values.id),'').strip()
                    try:
                        timePeriod=int(timePeriod)
                    except:
                        timePeriod=0
                    if teacher==-1:
                        values.classTeacher=None
                        
                    else:
                        
                        uniqueteacher=tbl_teacher.objects.get(id=teacher)
                        
                        values.classTeacher=uniqueteacher
                        values.save()
                    status=int(req.POST.get('status'+str(values.id),''))
                    if status==1:
                        values.isActive=True
                        uniqueobj.sections.add(values.section)
                    else:
                        values.isActive=False
                        
                    
                    uniqueobj.period=int(period)
                    uniqueobj.timePeriod=timePeriod
                    values.save()
                    uniqueobj.save()
                
                return HttpResponseRedirect('/standards/')    
                    
                
        for values in mssrows:
            temp=[]
            
            temp.append(uniqueobj.name)
            temp.append(uniqueobj.medium.name)
            temp.append(values.section.name)
            
            temp.append(uniqueobj.period)
            if values.classTeacher:
                
                temp.append(values.classTeacher.id)
            else:
                temp.append(-1)
            temp.append(uniqueobj.timePeriod)
            temp.append(values.id)
            overall.append(temp)
        
        return render_to_response('editStandard.html',locals(),context_instance=RequestContext(req))
def v_addData(req):
    mediums=tbl_medium.objects.all()
    sections=tbl_class.objects.all()
    allTeachers=tbl_teacher.objects.filter()
    return render_to_response('test1.html',locals(),context_instance=RequestContext(req))
def v_addXXX(req):
    if req.POST.get('addStandard',''):
        values=req.POST.get('fun123','')
        values=req.POST.get('standard2','')
        return HttpResponse(values)
#selectBox-arrow.gif