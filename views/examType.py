from django.shortcuts import render_to_response, render
from App.models import tbl_medium, tbl_examType, tbl_systemUser, tbl_MSS,\
    tbl_employee, tbl_attendence, tbl_school, tbl_student, tbl_fees,\
    tbl_standard, tbl_shortstandard
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.template.context import RequestContext
from django.template.context import RequestContext
from views.permission import i_hasPermission
from views.student import dateformatConvertor
from SMS.settings import STUDENTPREFIX
def v_examType(req):
    '''
    this method is used to add new exam type and also to show listing
    '''
    
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'exam','v'): 
        errors=[]
        rows=tbl_examType.objects.filter()
        if req.POST.get('addExam',''):
            
            if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'exam','a'):
                '''
                form validation will be carried out
                '''
                name=req.POST.get('name','').strip()
                
                checkdup=tbl_examType.objects.filter(name=name)
                if not name:
                    errors.append('Please enter the name !')
                if checkdup:
                    errors.append('Please enter different name !')
                if errors:
                    return render_to_response('addExamType.html',locals(),context_instance=RequestContext(req))
                '''
                inserting into database
                '''
                p1=tbl_examType()
                
                p1.name=name
                
                p1.save()
                return HttpResponseRedirect('/examType/')
        return render_to_response('addExamType.html',locals(),context_instance=RequestContext(req))


def v_editExamType(req,para):
    '''
    this method will carry out editing of medium whose id is equal to para
    '''
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'exam','u'):
        para=int(para)
        
       
        row=tbl_examType.objects.get(id=para)
        name=row.name
        
        rows=tbl_examType.objects.all()
         
        if req.POST.get('editExamType',''):
            '''
            form validation will be carried out
            '''
            errors=[]
            name=req.POST.get('name','').strip()
            
            if not name:
                errors.append("Please enter the name!")
            existedName=tbl_examType.objects.filter(name=name).exclude(id=para)
            if existedName:
                errors.append("Please enter the different name!")
            
            if errors:    
                return render_to_response('editExamType.html',locals(),context_instance=RequestContext(req))
            '''
            updating database with new values
            '''
            item=tbl_examType.objects.get(id=para)
            item.name=name
            
            item.save()
            
            return HttpResponseRedirect('/examType/')
        
            
            
            
        return render_to_response('editExamType.html',locals(),context_instance=RequestContext(req))
def v_responder1(req):
    if req.GET.get('attendence',''):
        '''
        helps to access required month,session attendence of employee through AJAX
        '''
        
        att=req.GET.get('attendence','')
        
        listing=att.split(":")
        
        month=int(listing[0])
        year=int(listing[1])
        
        allrows=tbl_attendence.objects.filter(date__month=month,date__year=year).order_by('date')
        
        emps=tbl_employee.objects.filter()
        temp=[]
        overall=[]
        temp1=[]
        template="<table class='table table-bordered table-striped' width='200%'>\n\
            <thead align='center'  class='tr_bg_list'>\n\
            <tr >\n\
            <td width='10%'>Employee</td>"
        
        if not allrows:
            template=template+"</tr></thead><tbody align='center' class='font_wght'><tr><td align='center'>No data at present</td></tr></tbody></table>"
            return HttpResponse(template)
        '''
        arranging data in required tabular formats
        '''
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
        for d in allrows:
            template=template+"<td width='10%'>"+d.rdate()+"</td>"
        template=template+"</tr></thead><tbody align='center' class='font_wght'>"
        for v in overall:
            template=template+"<tr><td>"+v[0]+"</td>"
            for ddd in v[1]:
                template=template+"<td>"+ddd+"</td>\n"
            template=template+"</tr>"
        template=template+"</tbody></table>"
        return HttpResponse(template)
    '''
    used for implementing shortcut to add standard name
    '''
    if req.GET.get('popshortstandard',''):
        
        shortstandards=tbl_shortstandard.objects.all()
        template="<select class='small' name='shortstandard' >\n\
        <option value='-1' selected>Select Standard</option>"
        if shortstandards:
            
            for c in shortstandards:
                if c.id==int(req.GET.get('popshortstandard','')):
                    
                    template=template+"<option value='"+str(c.id)+"' selected>"+c.name+"</option>\n"
                else:
                    
                    template=template+"<option value='"+str(c.id)+"' >"+c.name+"</option>\n"
        else:
            template=template+"<option value='-1'> not found !</option>\n"
        template=template+"</select>"
        return HttpResponse(template)
    '''
    used to get student information based on its Id
    '''
    if req.GET.get('studid',''):
        
        studid=req.GET.get('studid','')
        
        uniqueob=tbl_student.objects.get(id=int(studid[len(STUDENTPREFIX):]))
        template="<div class='section'>\n\
        <label>STUDENT NAME </label><div>\n\
        <input type='text' name='name' readonly value='"+uniqueob.perDetail.fName+"' />\n\
        </div></div>\n\
        <div class='section'>\n\
        <label>Standard </label><div>\n\
        <input type='text' name='standard' readonly value='"+uniqueob.standard.name+"' />\n\
        </div></div>\n\
        <div class='section'>\n\
        <label>Medium </label><div>\n\
        <input type='text' name='medium' readonly value='"+uniqueob.standard.medium.name+"' />\n\
        </div></div>\n\
        "
        return HttpResponse(template)
    '''
    Used to get fee for required month and session
    '''
    
    if req.GET.get('mont',''):
        studname=''
        studstandard=''
        studmedium=''
        studamt=''
        try:
            
            monthyear=req.GET.get('mont','')
            
            listing=monthyear.split(':')
            
            
            month=int(listing[1])
            
            year=int(listing[0])
            
            studid=listing[2]
            
            getstudid=int(studid[len(STUDENTPREFIX):])
            
            uniquestud=tbl_student.objects.get(id=getstudid)
            studname=uniquestud.getName()            
            getdata=uniquestud.history.get(year=year)
            getmedium=getdata.mss.medium
                        
            getstandard=getdata.mss.standard
            studstandard=getstandard.name
            studmedium=getmedium.name
            getstandobj=tbl_standard.objects.get(name=getstandard.name,medium=getmedium)
            uniqueob=tbl_fees.objects.get(month=month,year=year,standard=getstandobj)
            
            
            studamt=uniqueob.amount
            
            
            template="<div class='section'>\n\
            <label>Name</label><div>\n\
            <input type='text' name='name' readonly value='"+str(studname)+"' />\n\
            </div></div><div class='section'>\n\
            <label>Standard</label><div>\n\
            <input type='text' name='standard' readonly value='"+str(studstandard)+"' />\n\
            </div></div><div class='section'>\n\
            <label>Medium</label><div>\n\
            <input type='text' name='medium' readonly value='"+str(studmedium)+"' />\n\
            </div></div>\n\
            <div class='section'>\n\
            <label>Amount</label><div>\n\
            <input type='text' name='amount' readonly value='"+str(studamt)+"' />\n\
            </div></div>\n\
            "
        except:
            template="<div class='section'>\n\
            <label>Name</label><div>\n\
            <input type='text' name='name' readonly value='"+str(studname)+"' />\n\
            </div></div><div class='section'>\n\
            <label>Standard</label><div>\n\
            <input type='text' name='standard' readonly value='"+str(studstandard)+"' />\n\
            </div></div><div class='section'>\n\
            <label>Medium</label><div>\n\
            <input type='text' name='medium' readonly value='"+str(studmedium)+"' />\n\
            </div></div>\n\
            <div class='section'>\n\
            <label>Amount</label><div>\n\
            <input type='text' name='amount' readonly value='"+str(studamt)+"' />\n\
            </div></div>\n\
            "
        
        return HttpResponse(template)
          
def v_studentSibling(req):
    '''
    used to get information about child based on its id
    '''
    if req.GET.get('siblingID',''):
        
        studid=req.GET.get('siblingID','')
        
        uniqueob=tbl_student.objects.get(id=int(studid[len(STUDENTPREFIX):]))
        template="<div class='section'>\n\
        <label>NAME </label><div>\n\
        <input type='text' name='name' readonly value='"+uniqueob.perDetail.fName+"' />\n\
        </div></div>\n\
        "
        return HttpResponse(template)
    if req.GET.get('siblingID2',''):
        
        studid=req.GET.get('siblingID2','')
        
        uniqueob=tbl_student.objects.get(id=int(studid[len(STUDENTPREFIX):]))
        template="<div class='section'>\n\
        <label>NAME </label><div>\n\
        <input type='text' name='name' readonly value='"+uniqueob.perDetail.fName+"' />\n\
        </div></div>\n\
        "
        return HttpResponse(template)
def v_dateattendenceRecord(req):
    schoolobj=tbl_school.objects.filter()
    
    
    if req.GET.get('dateatten',''):
        '''
        will help to access data from attendence table filtered by date,and helps to access employee attendance for that date
        '''
        getdate=dateformatConvertor(str(req.GET.get('dateatten','')))
        
        
        allemp=tbl_employee.objects.filter(isActive=True,joinDate__lte=getdate)
        try:
            
            getuniquerow=tbl_attendence.objects.get(date=getdate,session1=schoolobj[0].getSession())
            
            temp=[]
            overall=[]
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
            '''
            arranging data in required tabular format
            '''
            template="<table class='table table-bordered table-striped' width='100%'>\n\
            <thead align='center'  class='tr_bg_list'>\n\
            <tr><td width='12%'>EMPID</td><td width='20%'>Name</td>\n\
            <td width='5%'>Absent</td><td width='15%'>TimeIn</td>\n\
            <td width='20%'>TimeOut</td></tr></thead><tbody align='center' class='font_wght'>"
            
            for data in overall:
                
                template=template+"<tr><td>"+str(data[0])+"</td><td>"+str(data[1])+"</td>"
                
                if data[2]:
                    template=template+"<td><input type='checkbox' value='1' name='"+data[0]+"' checked /></td>"
                else:
                    template=template+"<td><input type='checkbox' value='1' name='"+data[0]+"' /></td>"
                
                template=template+"<td><input type='text' maxlength='2' style='width:30px;' value='"+str(data[3])+"' name='"+data[0]+"timeinhour' onkeypress='return isNumberKey(event)' placeholder='HH' onchange='checkhour(this.value)'>:\n\
                <input type='text' maxlength='2' style='width:30px;' name='"+data[0]+"timeinmin' value='"+data[4]+"' onkeypress='return isNumberKey(event)' placeholder='MM' onchange='checkmin(this.value)' /></td>\n\
                <td><input type='text' maxlength='2' style='width:30px;' value='"+str(data[5])+"' name='"+data[0]+"timeouthour' onkeypress='return isNumberKey(event)' placeholder='HH' onchange='checkhour(this.value)'>:\n\
                <input type='text' maxlength='2' style='width:30px;' name='"+data[0]+"timeoutmin' value='"+data[6]+"' onkeypress='return isNumberKey(event)' placeholder='MM' onchange='checkmin(this.value)' /></td></tr>"
            template=template+"</tbody></table>"
            
            return HttpResponse(template)
        except:
            overall=[]
            temp=[]
            allemp=tbl_employee.objects.filter(isActive=True,joinDate__lte=getdate)
            for data in allemp:
                temp=[]
                temp.append(data.getEMPId())
                temp.append(data.getEMPName())
                temp.append(None)
                temp.append('')
                temp.append('')
                temp.append('')
                temp.append('')
                overall.append(temp)
            
            template="<table class='table table-bordered table-striped' width='100%'>\n\
            <thead align='center'  class='tr_bg_list'>\n\
            <tr><td width='12%'>EMPID</td><td width='20%'>Name</td>\n\
            <td width='5%'>Absent</td><td width='15%'>TimeIn</td>\n\
            <td width='20%'>TimeOut</td></tr></thead><tbody align='center' class='font_wght'>"
            
            for data in overall:
                
                template=template+"<tr><td>"+str(data[0])+"</td><td>"+str(data[1])+"</td>"
                
                
                
                template=template+"<td><input type='checkbox' value='1' name='"+str(data[0])+"' /></td>"
                
                template=template+"<td><input type='text' maxlength='2' style='width:30px;' value='"+data[3]+"' name='"+str(data[0])+"timeinhour' onkeypress='return isNumberKey(event)' placeholder='HH' onchange='checkhour(this.value)'>:\n\
                <input type='text' maxlength='2' style='width:30px;' name='"+str(data[0])+"timeinmin' value='"+data[4]+"' onkeypress='return isNumberKey(event)' placeholder='MM' onchange='checkmin(this.value)' /></td>\n\
                <td><input type='text' maxlength='2' style='width:30px;' value='"+str(data[5])+"' name='"+str(data[0])+"timeouthour' onkeypress='return isNumberKey(event)' placeholder='HH' onchange='checkhour(this.value)'>:\n\
                <input type='text' maxlength='2' style='width:30px;' name='"+str(data[0])+"timeoutmin' value='"+data[6]+"' onkeypress='return isNumberKey(event)' placeholder='MM' onchange='checkmin(this.value)' /></td></tr>"
            template=template+"</tbody></table>"
            
            return HttpResponse(template)
def getstudents(req):
    '''
    this is used to access all the student from selected class,through AJAX
    '''
    if req.GET.get('getStudentsOfClass',''):
        students=tbl_MSS.objects.get(id=req.GET.get('getStudentsOfClass','')).students.all()
        
        
        template="<div class='selectWidth1' id='classStudents_div'>\n<select class='medium' name='classStudent_id' >\n<option value='-1' >Select Students</option>"
        if students:
            for s in students:
                template=template+"<option value='"+str(s.id)+"'>"+str(s.getstudentId()).upper()+"</option>\n"
        else:
            template=template+"<option value='-1'> not found !</option>\n"
        template=template+"</select>\n</div>"
        return HttpResponse(template)

