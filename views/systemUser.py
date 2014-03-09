
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from App.models import tbl_role, tbl_systemUser
from django.http import HttpResponseRedirect
from App.pp import i_upload, i_getUser
from SMS.settings import userUDir
from views.permission import i_hasPermission


def isUser(usrname):
    try:
        if tbl_systemUser.objects.get(username=usrname):
            return True
    except:
        return False
def isUserEmail(email):
    try:
        if tbl_systemUser.objects.get(email=email):
            return True
    except:
        return False
def getUser(usrname):
    try:
        return tbl_systemUser.objects.get(username=usrname)
    except:
        pass

def getUserByEmail(email):
    try:
        return tbl_systemUser.objects.get(email=email)
    except:
        pass


def v_user(req):
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'user','v'):
        
        users=tbl_systemUser.objects.filter(isSuper=False)
        return render_to_response('userList.html',locals(),context_instance=RequestContext(req))

def v_addUser(req):
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'user','a'):
        roles=tbl_role.objects.filter(isActive=True)
        imagePath=None
        #states=tbl_location.objects.filter(pid=1)
        #empPrefix=EMPLOYEE_PREFIX
        if req.POST.get('addUser',''):
            errors=[]
            username=req.POST.get('username','').strip()
            pwd=req.POST.get('pwd','').strip()
            cpwd=req.POST.get('cpwd','').strip()
            email=req.POST.get('email',None).strip()
            role=int(req.POST.get('role',''))
            active=req.POST.get('active',False)
            admin=req.POST.get('admin',False)
            
            #-----------------cleaning done----------------
            if len(username)==0:
                errors.append("please enter a username !")
            elif not 5 <= len(username) <= 15:
                errors.append("username length should be between 5-15 characters !")
            elif isUser(username):
                errors.append("this username is already exist !")
            elif len(pwd)==0:
                errors.append("please enter a password !")
            elif not 5 <= len(pwd) <= 15:
                errors.append("password length should be between 5-15 characters !")
            elif not pwd==cpwd:
                errors.append("both password fields must be match !")
            elif '@' not in email:
                errors.append("please enter a valid email address !")
            elif isUserEmail(email):
                errors.append("this email ID is already registered !")
            elif role==-1:
                errors.append("please select atleast one role !")
            else:
                if active:
                    active=True
                if admin:
                    admin=True
                if req.FILES.get('image'):
                    imagePath=i_upload(req.FILES['image'],userUDir,username+'.jpeg')
            if not errors:
                tbl_systemUser.objects.create(username=username,
                                            password=pwd,
                                            email=email,
                                            role=tbl_role.objects.get(id=role),
                                            isActive=active,
                                            isAdmin=admin,
                                            image=imagePath
                                            )
                return HttpResponseRedirect('/user')
            return render_to_response('addUser.html',locals(),context_instance=RequestContext(req))     
        return render_to_response('addUser.html',locals(),context_instance=RequestContext(req))


def v_editUser(req,id_):
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'user','u'):
        
        roles=tbl_role.objects.filter(isActive=True)
        user=i_getUser(id_)
        username=user.username
        email=user.email
        role=user.role.id
        active=user.isActive
        admin=user.isAdmin
        pwd=user.password
        cpwd=user.password
        
        try:  
            imagePath=user.image.url
        except:
            imagePath=''
        if req.POST.get('editUser',''):
            errors=[]
            username=req.POST.get('username','').strip()
            pwd=req.POST.get('pwd','').strip()
            cpwd=req.POST.get('cpwd','').strip()
            email=req.POST.get('email',None).strip()
            role=int(req.POST.get('role',''))
            active=req.POST.get('active',False)
            admin=req.POST.get('admin',False)
            
            #----------------------------------    
            if len(username)==0:
                errors.append("please enter a username !")
            elif not 5 <= len(username) <= 15:
                errors.append("username length should be between 5-15 characters !")
            elif isUser(username) and getUser(username).username!=user.username:
                errors.append("this username is already exist !")
            elif len(pwd)==0:
                errors.append("please enter a password !")
            elif not 5 <= len(pwd) <= 15:
                errors.append("password length should be between 5-15 characters !")
            elif user.password!=pwd and not pwd==cpwd:
                errors.append("both password fields must be match !")
            elif '@' not in email:
                errors.append("please enter a valid email address !")
            elif getUserByEmail(email) and getUserByEmail(email).email!=user.email:
                errors.append("this email ID is already registered !")
            elif role==-1:
                errors.append("please select atleast one role !")
            else:
                
                if active:
                    active=True
                if admin:
                    admin=True
                if req.FILES.get('image'):
                    imagePath=i_upload(req.FILES['image'],userUDir,username+'.jpeg')
            
            #-----------------done----------------
            if not errors:
                user.username=username
                user.password=pwd
                user.email=email
                user.role=tbl_role.objects.get(id=role)
                user.isActive=active
                user.isAdmin=admin
                user.image=imagePath
                user.save()
                return HttpResponseRedirect('/user/edit/'+str(user.id))
            return render_to_response('editUser.html',locals(),context_instance=RequestContext(req))     
        return render_to_response('editUser.html',locals(),context_instance=RequestContext(req))
        
