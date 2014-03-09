#this file basically contains various AJAX used in the project
from django.shortcuts import render_to_response
from App.models import tbl_shortstandard, tbl_student, tbl_fees, tbl_attendence,\
    tbl_employee, tbl_MSS, tbl_holiday, tbl_role, tbl_systemUser, tbl_standard,\
    tbl_school
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from SMS.settings import STUDENTPREFIX, userUDir
from views.student import dateformatReverse, dateformatConvertor
from views.systemUser import isUser, isUserEmail
from App.pp import i_upload



def v_popUp(req,option):
    if option=="shortstandard":#this is used to make shortcut in order to add standard name in standard section
        if req.POST.get('addshortstandard',''):
            errors=[]
            name=req.POST.get('name','').strip()
            if not name:
                errors.append("Please enter the name!")
            dupname=tbl_shortstandard.objects.filter(name=name)
            
            if dupname:
                errors.append("Please enter the different name,this name already exist!")
            
            if errors:
                return render_to_response('popshortstandard.html',locals())
            p1=tbl_shortstandard(name=name)
            p1.save()
            
             
            temp="\n\
                <script>\n\
                try{\n\
                    window.opener.setPopshortstandard("
            temp=temp+str(p1.id)+")\n\
                    window.close();\n\
                    }catch(error){alert(error);}\n\
                </script>"
            return HttpResponse(temp)
    
        return render_to_response('popshortstandard.html',locals())  
    elif option=="user":
        roles=tbl_role.objects.filter(isActive=True)
        imagePath=None
   
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
                user=tbl_systemUser.objects.create(username=username,
                                            password=pwd,
                                            email=email,
                                            role=tbl_role.objects.get(id=role),
                                            isActive=active,
                                            isAdmin=admin,
                                            image=imagePath
                                            )
                temp="\n\
                <script>\n\
                try{\n\
                    window.opener.setPopUser("
                temp=temp+str(user.id)+")\n\
                    window.close();\n\
                    }catch(error){alert(error);}\n\
                </script>"
                return HttpResponse("<p>"+temp+"</p>")
            return render_to_response('pop_addUser.html',locals())    
        return render_to_response('pop_addUser.html',locals())
        
        #return HttpResponse('in user')  
    
