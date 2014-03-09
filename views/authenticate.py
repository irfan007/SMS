#from django.http import HttpResponse
from App.models import  tbl_systemUser, tbl_school
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from django.core.mail import send_mail
from SMS.settings import EMAIL_HOST_USER


#def i_findURl(emp):
#    defultURL={
#                  'role':'/role/',
#                  'user':'/user/',
#                  'setting':'/school/add/',
#                  'staff':'/staff/',
#                  'medium':'/mediums/',
#                  'section':'/sections/',
#                  'standard':'/standards/',
#                  'subject':'/subjects/',
#                  'holiday':'/holidays/',
#                  
#    }
#    try:
#        if emp.isAdmin:
#            return defultURL['user'] 
#        return defultURL[emp.role.permissions.filter(view=True)[0].content.name]
#    except:
#        return "/myaccount/"
    

def i_getUserByEmail(email):
    try:
        return tbl_systemUser.objects.get(email=email)
    except:
        return None

def i_validateUser(usr,pwd):
    try:
        usr=tbl_systemUser.objects.get(username=usr,isActive=True)
        if usr.password==pwd:
            return usr
    except:
        return None   

def v_home(req):
    try:
        cuser=tbl_systemUser.objects.get(username=req.session.get('username',''))
        if cuser.isAdmin:
            if not tbl_school.objects.all():
                return HttpResponseRedirect('/school/add')
            else:
                return render_to_response('myDashboard.html',locals(),context_instance=RequestContext(req))    
        else:
            return render_to_response('myDashboard.html',locals(),context_instance=RequestContext(req))
    except tbl_systemUser.DoesNotExist:
        return HttpResponseRedirect("/login")


def v_loginUser(req):
    try:
        if tbl_systemUser.objects.get(username=req.session.get('username','')):
            return HttpResponseRedirect("/")
    except tbl_systemUser.DoesNotExist:
        pass   
        
    if req.method=='POST':
        errors=[]
        usr=None
        username=req.POST.get('username','').strip()
        password=req.POST.get('password','').strip()
        if len(username)==0:
            errors.append("Please enter username !")
        elif len(password)==0:
            errors.append("Please enter password !")
        usr=i_validateUser(username,password)
        if not usr:
            errors.append("Invalid Username Or Password !")
        if not errors:
            req.session['username']=usr.username
            return HttpResponseRedirect('/')
        return render_to_response("login.html",locals())
    return render_to_response("login.html")


def v_logoutUser(req):
    if req.session.get('username',''):
        del req.session['username']
    return HttpResponseRedirect('/')

def v_forgotPassword(req):
    try:
        if tbl_systemUser.objects.get(username=req.session.get('username','')):
            return HttpResponseRedirect("/")
    except:
        pass  
        
    if req.method=='POST':
        errors=[]
        usr=None
        email=req.POST.get('email','').strip()
        if len(email)==0:
            errors.append("Please enter a email address !")
        elif '@' not in email:
            errors.append("Please enter a valid email address !")
        else:
            usr=i_getUserByEmail(email)
            if not usr:
                errors.append("We have no user with this email Id !")
        if not errors:
            msg="\nHi "+usr.username+",\n\nYour Forgotten Password is inside '()' :("+usr.password+")\n\nThanks,\nSMS Team"
            send_mail('School Management',msg,EMAIL_HOST_USER,[email])
            return render_to_response('forgotPassword.html',{'done':True})
        return render_to_response('forgotPassword.html',locals())
        
    return render_to_response('forgotPassword.html')
    
    