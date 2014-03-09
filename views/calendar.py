from views.permission import i_hasPermission
from App.models import tbl_employee, tbl_events, tbl_systemUser, Notice
from django.shortcuts import render_to_response
from django.template.context import RequestContext


def i_getUser(byUsername):
    try:
        return tbl_systemUser.objects.get(username=byUsername)
    except tbl_employee.DoesNotExist:
        return None


def v_eventCalander(req):
    if i_hasPermission(i_getUser(req.session.get('username','')),'crm','v'):
        eventsData="["
        import datetime
        events=tbl_events.objects.filter(username=req.session.get('username',''))
        i=0
        for e in events:
            eventsData=eventsData+"['"+e.event+"','"+str(e.startDate)+"','"+str(e.endDate)+"','"+e.fgColor+"','"+e.bgColor+"','"+str(e.createdOn)+"','e']"
            try:
                events[i+1]
                eventsData=eventsData+","
            except IndexError:
                pass
            i=i+1
        
        
        i=0
        notices=Notice.objects.filter(isActive=True)
        if events and notices:
            eventsData=eventsData+","
        for n in notices:
            eventsData=eventsData+"['"+n.message+"','"+str(n.date)+" 00:00:00','"+str(n.date)+" 00:00:00','#ffffff','#006B24','"+str(n.date)+" 00:00:00','n']"
            try:
                notices[i+1]
                eventsData=eventsData+","
            except IndexError:
                pass
            i=i+1
        
        eventsData=eventsData+"]"
        return render_to_response("calendar.html",locals(),context_instance=RequestContext(req))