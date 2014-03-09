from django.shortcuts import render_to_response
from views.student import dateformatConvertor, dateformatReverse
from App.models import tbl_holiday, tbl_student, tbl_school, tbl_systemUser
from django.http import HttpResponseRedirect
from django.http import HttpResponse
import datetime
from SMS.settings import manavPageParameter

from django.template.context import RequestContext
from views.permission import i_hasPermission
    
    
    
    
def v_holidays(req):
    '''
    this method will help in listing of holidays
    '''
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'holiday','v'): 
        schoolobj=tbl_school.objects.filter()
        errors=[]
        if not schoolobj:
            errors.append("Please enter the setting first in configuration!")
            return render_to_response('holidays.html',locals(),context_instance=RequestContext(req))
        pagination_parameter=manavPageParameter    #Used for next and previous (i.e pagination)
        NEXT=False
        allrows=tbl_holiday.objects.filter(session1=schoolobj[0].getSession()).order_by('date')
        temp=tbl_holiday.objects.values('session1').distinct()
        sessionlist=[]
        selectsession=schoolobj[0].getSession()
        sessionlist.append(schoolobj[0].getSession())
        for data in temp:
            sessionlist.append(data['session1'])
        sessionlist=set(sessionlist)
        
        totalRows=len(allrows)
        TO=len(allrows)
        if len(allrows)>pagination_parameter:
            TO=pagination_parameter
            NEXT=True
        FROM=1
        allrows=allrows[:pagination_parameter]
        
        return render_to_response('holidays.html',locals(),context_instance=RequestContext(req))
    
    

def v_nextHolidays(req,para,para1):
    '''
    this method helps to access next rows of holidays present in database
    '''  
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'holiday','v'):
        para=int(para)
        
        FROM=para+1
        pagination_parameter=manavPageParameter
        schoolobj=tbl_school.objects.filter()
        pagination_parameter=pagination_parameter+para
        NEXT=False
        allrows=tbl_holiday.objects.filter(session1=para1).order_by('date')
        
        temp=tbl_holiday.objects.values('session1').distinct()
        sessionlist=[]
        sessionlist.append(para1)
        selectsession=para1
        sessionlist.append(schoolobj[0].getSession())
        for data in temp:
            sessionlist.append(data['session1'])
        sessionlist=set(sessionlist)
        totalRows=len(allrows)
        TO=len(allrows)
        if len(allrows)>pagination_parameter:
            TO=pagination_parameter
            NEXT=True
        
        
        allrows=allrows[para:pagination_parameter]
        PREV="True"
        back=para
        
        #return HttpResponse(allrows)
        return render_to_response('holidays.html',locals(),context_instance=RequestContext(req))
    

def v_prevHolidays(req,para,para1):
    '''
    this method helps to access previous holidays rows from the database
    '''
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'holiday','v'):
        schoolobj=tbl_school.objects.filter()
        
        para=int(para)
        TO=para
        pagination_parameter=manavPageParameter
        back=para-pagination_parameter
        
        allrows=tbl_holiday.objects.filter(session1=para1).order_by('date')
        temp=tbl_holiday.objects.values('session1').distinct()
        sessionlist=[]
        sessionlist.append(para1)
        selectsession=para1
        sessionlist.append(schoolobj[0].getSession())
        for data in temp:
            sessionlist.append(data['session1'])
        sessionlist=set(sessionlist)
        totalRows=len(allrows)
        NEXT=False
        FROM=back+1
        if len(allrows)>back:
            NEXT=True
        allrows=allrows[back:para]
        if back==0:
            PREV=False
        else:
            PREV=True
        
        return render_to_response('holidays.html',locals(),context_instance=RequestContext(req))


def v_addHoliday(req):
    '''
    this method will help to insert new record in the database
    '''
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'holiday','a'):
        errors=[]
        getlength=1
        schoolobj=tbl_school.objects.filter()
        if not schoolobj:
            errors.append("Please enter the setting first in configuration!")
        
        if req.POST.get('addHoliday',''):
            '''
            performing form validation
            ''' 
            getback=True
            getlength=int(req.POST.get('getlength',''))
            i=1
            temp=[]
            overall=[]
            while i<=getlength:
                temp=[]
                date1=req.POST.get('date'+str(i),'').strip()
                reason=req.POST.get('reason'+str(i),'').strip()
                date=''
                try:
                    date=dateformatConvertor(date1)
                except:
                    errors.append("Please enter the valid date!")
               
                if not reason:
                    errors.append("Please enter the festival or reason!")
                if date:
                    dup=tbl_holiday.objects.filter(date=date)
                    if dup:
                        errors.append("date %s already exists in holidays list!"%(date1))
                temp.append(date1)
                temp.append(reason)
                overall.append(temp)
                i=i+1
                
            errors=set(errors)
            if errors:
                return render_to_response('addHoliday.html',locals(),context_instance=RequestContext(req))
            
            else:
                '''
                insert the new record in database table tbl_holiday
                '''
                for data in overall:
                    p1=tbl_holiday()
                    p1.date=dateformatConvertor(data[0])
                    p1.festival=data[1]
                    p1.session1=schoolobj[0].getSession()
                    p1.save()
                
    
            return HttpResponseRedirect('/holidays/')
        return render_to_response('addHoliday.html',locals(),context_instance=RequestContext(req))
def v_editHoliday(req,para1):
    '''
    this will help to view/edit inserted data from holidays
    '''
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'holiday','u'):
        schoolobj=tbl_school.objects.filter()
        
        allrows=tbl_holiday.objects.filter(session1=para1)
        errors=[]
        overall=[]
        temp=[]
        if req.POST.get('editHoliday',''):
            '''
            performing form validation
            '''
            getBack=True
            for data in allrows:
                temp=[]
                date=req.POST.get('date'+str(data.id),'').strip()
                fest=req.POST.get('reason'+str(data.id),'').strip()
                date1=''
                try:
                
                    date1=dateformatConvertor(date)
                except:
                    errors.append("Please enter the valid date!")
                if not fest:
                    errors.append("Please enter the festival or reason!")
                if date1:
                    dup=tbl_holiday.objects.filter(date=date1).exclude(id=data.id)
                    if dup:
                        errors.append("date %s already exists in holidays list!"%(date))
                temp.append(data.id)
                temp.append(date)
                temp.append(fest)    
                overall.append(temp)    
            errors=set(errors)
            if errors:
                return render_to_response('editHoliday.html',locals(),context_instance=RequestContext(req))
            else:
                '''
                finally updating database with new values
                '''
                for data in overall:
                    p1=tbl_holiday.objects.get(id=data[0])
                    p1.date=dateformatConvertor(data[1])
                    p1.festival=data[2]
                    p1.session1=schoolobj[0].getSession()
                    
                    p1.save()
            return HttpResponseRedirect('/holidays/')
        return render_to_response('editHoliday.html',locals(),context_instance=RequestContext(req))
    
def v_Yearholidays(req,para):
    '''
    helps to access holidays list of different session year
    '''
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'holiday','v'):
    
        pagination_parameter=manavPageParameter    #Used for next and previous (i.e pagination)
        NEXT=False
        allrows=tbl_holiday.objects.filter(session1=para).order_by('date')
        temp=tbl_holiday.objects.values('session1').distinct()
        schoolobj=tbl_school.objects.filter()
        sessionlist=[]
        sessionlist.append(para)
        selectsession=para
        sessionlist.append(schoolobj[0].getSession())
        for data in temp:
            sessionlist.append(data['session1'])
        sessionlist=set(sessionlist)
        totalRows=len(allrows)
        TO=len(allrows)
        if len(allrows)>pagination_parameter:
            TO=pagination_parameter
            NEXT=True
        FROM=1
        allrows=allrows[:pagination_parameter]
        return render_to_response('holidays.html',locals(),context_instance=RequestContext(req))
        
    