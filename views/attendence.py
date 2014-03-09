from django.shortcuts import render_to_response
from App.models import tbl_employee, tbl_attendence, tbl_markAttendence,\
    tbl_school, tbl_systemUser
from SMS.settings import EMPLOYEE_PREFIX, MEDIA_ROOT
from django.http import HttpResponse
from views.student import dateformatConvertor
import datetime
from django.http import HttpResponseRedirect

from xlwt import Workbook
from xlwt.Style import easyxf
from django.core.servers.basehttp import FileWrapper





from django.template.context import RequestContext
from views.permission import i_hasPermission




def v_attendencedata(req,para1,para2):
    '''
    this method helps to access attendence of employees for required month(para2) and session(para1)
    '''

    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'attendance','v'):
        months=['Jan','Feb','Mar','Apr','May','June','July','Aug','Sept','Oct','Nov','Dec']
        month=int(para2)
        schoolobj=tbl_school.objects.filter()
        errors=[]
        if not schoolobj:
            errors.append("Please specify school details first in configuration settings!")
            return render_to_response('attendence.html',locals(),context_instance=RequestContext(req))
        temp=tbl_attendence.objects.values('session1').distinct()
        sessionlist=[]
        selectsession=para1
        sessionlist.append(para1)
        sessionlist.append(schoolobj[0].getSession())
        for data in temp:
            sessionlist.append(data['session1'])
        sessionlist=set(sessionlist)
        allrows=tbl_attendence.objects.filter(date__month=month,session1=para1).order_by('date')
        '''
        accessing data from database
        '''
        emps=tbl_employee.objects.filter()
        '''
        Now arranging data to produce table of required format
        '''
        temp=[]
        overall=[]
        temp1=[]
        getmonths=months[month-1]
        if not allrows:
            return render_to_response('attendence.html',locals(),context_instance=RequestContext(req))
        for e in emps:
            temp.append(e.getEMPName())
            for data in allrows:
                obj=data.marking.filter(employee=e)
                if obj:
                    for v in obj:
                        if v.employee==e:
                            temp1.append(v.gettime())
                else:
                    temp1.append("---")        
            temp.append(temp1)
            overall.append(temp)
            temp=[]
            temp1=[]
        
        return render_to_response('attendence.html',locals(),context_instance=RequestContext(req))




def v_attendence(req):
    '''
    this method will help to show  employees attendence record for current month and session
    '''
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'attendance','v'):
        months=['Jan','Feb','Mar','Apr','May','June','July','Aug','Sept','Oct','Nov','Dec']
        month=datetime.datetime.today().month
        schoolobj=tbl_school.objects.filter()
        errors=[]
        if not schoolobj:
            errors.append("Please specify school details first in configuration settings!")
            return render_to_response('attendence.html',locals(),context_instance=RequestContext(req))
        #year=datetime.datetime.today().year
        temp=tbl_attendence.objects.values('session1').distinct()
        sessionlist=[]
        selectsession=schoolobj[0].getSession()
        sessionlist.append(schoolobj[0].getSession())
        for data in temp:
            sessionlist.append(data['session1'])
        sessionlist=set(sessionlist)
        allrows=tbl_attendence.objects.filter(date__month=month,session1=schoolobj[0].getSession()).order_by('date') #accessing data from database
        emps=tbl_employee.objects.filter()
        '''
        Now arranging data to produce table of required format
        '''
        temp=[]
        overall=[]
        temp1=[]
        getmonths=months[month-1]
        if not allrows:
            return render_to_response('attendence.html',locals(),context_instance=RequestContext(req))
        for e in emps:
            temp.append(e.getEMPName)
            for data in allrows:
                obj=data.marking.filter(employee=e)
                if obj:
                    for v in obj:
                        if v.employee==e:
                            temp1.append(v.gettime())
                else:
                    temp1.append("---")        
            temp.append(temp1)
            overall.append(temp)
            temp=[]
            temp1=[]
        
        return render_to_response('attendence.html',locals(),context_instance=RequestContext(req))

def v_addAttendence(req):
    '''
    will help to mark attendence for the employees and staff
    '''
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'attendance','a'):
        schoolobj=tbl_school.objects.filter()
        errors=[]
        if not schoolobj:
            errors.append("Please specify school details first in configuration settings!")
            return render_to_response('addAttendence.html',locals(),context_instance=RequestContext(req))
        code=EMPLOYEE_PREFIX
        todaydate=datetime.datetime.today().date()
        allemp=tbl_employee.objects.filter(isActive=True,joinDate__lte=todaydate)
        
        x=datetime.datetime.strptime(str(todaydate), '%Y-%m-%d')
        date1=x.strftime('%d-%m-%Y')
        overall=[]
        temp=[]
        errors=[]
        try:
            getuniquerow=tbl_attendence.objects.get(date=todaydate,session1=schoolobj[0].getSession())
            
            for values in getuniquerow.marking.all():
                temp=[]
                temp.append(values.employee.getEMPId())
                temp.append(values.employee.getEMPName())
                    
                            
                temp.append(values.absent)
                            
                temp.append(values.gettimeinHour())
                            
                temp.append(values.gettimeinMin())
                temp.append(values.gettimeoutHour())
                temp.append(values.gettimeoutMin())
                        
                    
                overall.append(temp)
        
        except:
            
            for data in allemp:
                '''
                arranging data in proper tabular format
                '''
                temp=[]
                temp.append(data.getEMPId())
                temp.append(data.getEMPName())
                temp.append(None)
                temp.append('')
                temp.append('')
                temp.append('')
                temp.append('')
                overall.append(temp)
        
        if req.POST.get('addAttendence',''):
            '''
            performing form validation
            '''
            date1=req.POST.get('date1','')
            
            try:
                date=dateformatConvertor(date1)
            except:
                errors.append("Please enter valid date!")
                return render_to_response('addAttendence.html',locals(),context_instance=RequestContext(req))
            allemp=tbl_employee.objects.filter(isActive=True,joinDate__lte=date)
            '''
            accessing data from form and arranging it in proper order
            '''
            overall=[]
            temp=[]
            for data in allemp:
                
                
                temp=[]
                temp.append(data.getEMPId())
                temp.append(data.getEMPName())
                check=req.POST.get(str(data.getEMPId()),'')
                
                if check=='1':
                    temp.append(check)
                else:
                    temp.append(None)
                if not check:
                    if not req.POST.get(data.getEMPId()+'timeinhour','') or not req.POST.get(data.getEMPId()+'timeinmin','') :
                        errors.append("Please enter timein for employees who are not absent!")
                    
                timeinhour=req.POST.get(data.getEMPId()+'timeinhour','')
                timeinmin=req.POST.get(data.getEMPId()+'timeinmin','')
                temp.append(timeinhour)
                temp.append(timeinmin)
                
                timeouthour=req.POST.get(data.getEMPId()+'timeouthour','')
                timeoutmin=req.POST.get(data.getEMPId()+'timeoutmin','')
                temp.append(timeouthour)
                temp.append(timeoutmin)
                
                
                overall.append(temp)
            
            if not errors:
                '''
                Finally inserting data in the database
                '''
                duprow=tbl_attendence.objects.filter(date=date,session1=schoolobj[0].getSession())
                if duprow:
                    for objects in duprow:
                        objects.marking.remove()
                        objects.delete()
                        
                
                p1=tbl_attendence()
                p1.date=date
                p1.session1=schoolobj[0].getSession()
                p1.save()
                for data in overall:
                    p2=tbl_markAttendence()
                    p2.employee=tbl_employee.objects.get(id=int(data[0][len(EMPLOYEE_PREFIX):]))
                    if data[2]=="1":
                        p2.absent=True
                    else:
                        try:
                            timein=datetime.time(int(data[3]),int(data[4]))
                            p2.timein=timein
                        except:
                            timein=datetime.time(0,0)
                    
                            
                        
                    
                    if data[5]:
                        if data[6]:
                        
                            timeout=datetime.time(int(data[5]),int(data[6]))
                        else:
                            timeout=datetime.time(int(data[5]),0)
                        p2.timeout=timeout
                    else:
                        pass
                    
                                            
                    p2.save()
                    p1.marking.add(p2)
                p1.save()
                return HttpResponseRedirect('/attendences/')
            errors=set(errors)
            return render_to_response('addAttendence.html',locals(),context_instance=RequestContext(req))
           
        return render_to_response("addAttendence.html",locals(),context_instance=RequestContext(req))

def v_generateAttendenceReport(req):
    '''
    this method is used to show employee/staff attendence in excel form (based on year,month specified)
    '''
    months=['Jan','Feb','Mar','Apr','May','June','July','Aug','Sept','Oct','Nov','Dec']
    mondict={1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'June',7:'July',8:'Aug',9:'Sept',10:'Oct',11:'Nov',12:'Dec'}
    month=datetime.datetime.today().month
    year=datetime.datetime.today().year
    errors=[]
    if req.POST.get('attendenceExcel',''):
        month=int(req.POST.get('month',''))
        year=req.POST.get('year','').strip()
        
        if not year:
            errors.append("Please enter the year!")
            return render_to_response('attendenceReport.html',locals(),context_instance=RequestContext(req))
        '''
        arranging data,to genarate result in desired tabular format
        '''
        allrows=tbl_attendence.objects.filter(date__month=month,date__year=int(year)).order_by('date')
        emps=tbl_employee.objects.filter()
        temp=[]
        overall=[]
        temp1=[]
        if not allrows:
            return HttpResponse('<script>alert("No data exist");location.href="/report/attendence/"</script>')
        for e in emps:
            temp.append(e.perDetail.fName)
            for data in allrows:
                obj=data.marking.filter(employee=e)
                if obj:
                    for v in obj:
                        if v.employee==e:
                            temp1.append(v.gettime())
                else:
                    temp1.append("---")        
            temp.append(temp1)
            overall.append(temp)
            temp=[]
            temp1=[]
        '''
        creating excel sheet
        '''
        w = Workbook()
    
        ws = w.add_sheet('AttendenceReport')
        ws.col(0).width=30*256
        styletoprow=easyxf('align: vertical center, horizontal center;'
                           'font: name Arial;'
                           'border:bottom thin,right thin,top thin;'
                           )
        styletoprow1=easyxf('align: vertical center, horizontal center;'
                            'font: name Arial,bold true;'
                     
                            'border:bottom thin,right thin,top thin;'
                            )
        
        ws.write(0,0,'Attendence Report '+mondict[month]+' '+str(year),styletoprow1)                                  
        ws.write(1,0,'Employee',styletoprow1)
        x=1
        for data in allrows:
            ws.write(1,x,data.getday(),styletoprow1)
            x=x+1
        y=2
        
        for v in overall:
            z=1
            ws.write(y,0,v[0],styletoprow1)
            
            for ddd in v[1]:
                ws.write(y,z,ddd,styletoprow)
                z=z+1
            y=y+1
        
        
        w.save(MEDIA_ROOT+'attendence report.xls')
        myfile=open(MEDIA_ROOT+'attendence report.xls',"r")
        response = HttpResponse(FileWrapper(myfile), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=attendenceReport.xls'
        return response
        
    return render_to_response('attendenceReport.html',locals(),context_instance=RequestContext(req))
def v_viewAttendenceReport(req):
    '''
    this is used to get attendence data for employee for different months,or to get monthly report for individual employee
    attendence depending on option selected
    '''
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'attendance','v'):
        months=['Jan','Feb','Mar','Apr','May','June','July','Aug','Sept','Oct','Nov','Dec']
        errors=[]
        schoolobj=tbl_school.objects.filter()
        errors=[]
        if not schoolobj:
            errors.append("Please specify school details first in configuration settings!")
            return render_to_response('viewattendenceReport.html',locals(),context_instance=RequestContext(req))
        if req.POST.get('viewData',''):
            opt=req.POST.get('option','')
            if opt=="1":
                '''
                this will show attendance data for all the employees for selected month
                '''
                month=int(req.POST.get('month',''))
                if month==-1:
                    errors.append("Please select the month")
                    return render_to_response('viewattendenceReport.html',locals(),context_instance=RequestContext(req))
                getBack=True
                allrows=tbl_attendence.objects.filter(date__month=month,session1=schoolobj[0].getSession()).order_by('date')
                
                emps=tbl_employee.objects.filter()
                temp=[]
                overall=[]
                temp1=[]
                if not allrows:
                    return HttpResponse('<script>alert("No data exist");location.href="/report/attendence/"</script>')
                for e in emps:
                    temp.append(e.getEMPId)
                    temp.append(e.getEMPName())
                    absent=0
                    present=0
                    
                    for data in allrows:
                        obj=data.marking.filter(employee=e)
                        
                        if obj:
                            for v in obj:
                                if v.employee==e:
                                    if v.absent==True:
                                        absent=absent+1
                                    else:
                                        present=present+1
                    temp1.append(present)
                    temp1.append(absent)
                    temp1.append(absent+present)    
                        
                                    
                    temp.append(temp1)
                    overall.append(temp)
                    temp=[]
                    temp1=[]
                
                return render_to_response('viewattendenceReport.html',locals(),context_instance=RequestContext(req))
            if opt=="2":
                '''
                this will show attendance data for all the month for selected employee
                '''
                opt=req.POST.get('option','')
                getBack1=True
                emps=tbl_employee.objects.filter(isActive=True)
                temp=[]
                overall=[]
                #year=datetime.datetime.today().year
                emp=int(req.POST.get('employee',''))
                if emp==-1:
                    errors.append("Please select the employee")
                    return render_to_response('viewattendenceReport.html',locals(),context_instance=RequestContext(req))
                getEmpl= tbl_employee.objects.get(id=int(emp))
                i=1
                while(i<=12):
                    months=['Jan','Feb','Mar','Apr','May','June','July','Aug','Sept','Oct','Nov','Dec']
                    temp=[]
                    absent=0
                    present=0
                    getAttend=tbl_attendence.objects.filter(session1=schoolobj[0].getSession(),date__month=i)
                    for data in getAttend:
                        getvalues=data.marking.filter(employee=getEmpl)
                        
                        if getvalues:
                            for v in getvalues:
                                if v.employee==getEmpl:
                                    if v.absent==True:
                                        absent=absent+1
                                    else:
                                        present=present+1
                    temp.append(months[i-1])                    
                    temp.append(present)
                    temp.append(absent)
                    temp.append(absent+present)
                    #return HttpResponse(temp[2])
                    if getAttend:
                        overall.append(temp)
                    
                        temp=[]    
                    i=i+1        
                return render_to_response('viewattendenceReport.html',locals(),context_instance=RequestContext(req))        
        return render_to_response('viewattendenceReport.html',locals(),context_instance=RequestContext(req))