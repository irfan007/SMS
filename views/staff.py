from SMS.settings import EMPLOYEE_PREFIX, staffUDir, uploadFolder
from App.models import tbl_employee, tbl_location, tbl_empPersonalDetail,\
    tbl_systemUser
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.db.models import Q
from datetime import datetime
from App.pp import i_upload
from django.http import HttpResponseRedirect
from django.utils.dateformat import DateFormat
from views.permission import i_hasPermission

def v_staff(req):
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'staff','v'):
        ePrefix=EMPLOYEE_PREFIX
        employees=tbl_employee.objects.filter(~Q(desig='teacher'))
        return render_to_response('staffList.html',locals(),context_instance=RequestContext(req))

def v_addStaff(req):
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'staff','a'):
        
        users=tbl_systemUser.objects.filter(isActive=True,isSuper=False)
        empPrefix=EMPLOYEE_PREFIX
        empid=(tbl_employee.objects.count()+1)
        states=tbl_location.objects.filter(pid=1).order_by('name')
        states2=states
        
        if req.POST.get('addStaff',''):
            errors=[]
            
            joindate=req.POST.get('joindate',None).strip()
            totalExp=req.POST.get('totalExp','').strip()
            desig=req.POST.get('desig','').strip()
            salary=req.POST.get('salary','')
            user=int(req.POST.get('user',-1))
            
            title=req.POST.get('title','')
            fname=req.POST.get('fname','').strip()
            lname=req.POST.get('lname','').strip()
            dob=req.POST.get('dob','').strip()
            age=req.POST.get('age','').strip()
            email=req.POST.get('email','').strip()
            
            
            ladd=req.POST.get('ladd','').strip()
            lstate=int(req.POST.get('lstate',-1))
            cities=[]
            if lstate!=-1:
                cities=tbl_location.objects.filter(pid=lstate).order_by('name')
            lcity=int(req.POST.get('lcity',-1))
            lpin=req.POST.get('lpin','').strip()
            lmobile=req.POST.get('lmobile','').strip()
            llandline=req.POST.get('llandline','').strip()
            if req.POST.get('psamel','')=='1':
                padd=ladd
                pstate=lstate
                cities2=cities
                pcity=lcity
                ppin=lpin
                plandline=llandline
                pmobile=lmobile
            else:
                padd=req.POST.get('padd','').strip()
                pstate=int(req.POST.get('pstate',-1))
                if pstate!=-1:
                    cities2=tbl_location.objects.filter(pid=pstate).order_by('name')
                pcity=int(req.POST.get('pcity',-1))
                ppin=req.POST.get('ppin','').strip()
                pmobile=req.POST.get('pmobile','').strip()
                plandline=req.POST.get('plandline','').strip()
            
            #return HttpResponse(str(lcity)+"---"+str(pcity))
                  
            
            if title=='-1':
                errors.append("please select at least one title !")
            elif not fname:
                errors.append("please enter first name !")
            elif not lname:
                errors.append("please enter last name !")
            elif email and '@' not in email:
                    errors.append("please enter valid email Id !")
            
            elif not ladd:
                errors.append("please enter address of local residence !")
            elif lstate==-1:
                errors.append("please select one state of local residence !")
            elif lcity==-1:
                errors.append("please select one city of local residence !")
            elif not lpin:
                errors.append("please enter pincode of local residence !")
            elif not lmobile:
                errors.append("please enter mobile no. of local residence !")
            elif len(lmobile)<10:
                errors.append("please enter valid mobile no. of local residence !")
            elif not llandline:
                errors.append("please enter landline no. of local residence !")
            elif len(llandline)<7:
                errors.append("please enter valid landline no. of local residence !")
            
            
            elif not padd:
                errors.append("please enter address of permanent residence !")
            elif pstate==-1:
                errors.append("please select one state of permanent residence !")
            elif pcity==-1:
                errors.append("please select one city of permanent residence !")
            elif not ppin:
                errors.append("please enter pincode of permanent residence !")
            elif not pmobile:
                errors.append("please enter mobile no. of permanent residence !")
            elif len(pmobile)<10:
                errors.append("please enter valid mobile no. of permanent residence !")
            elif not plandline:
                errors.append("please enter landline no. of permanent residence !")
            elif len(plandline)<7:
                errors.append("please enter valid landline no. of permanent residence !")
            
            
            else:
                if dob:
                    try:
                        datetime.strptime(dob,'%d-%m-%Y')
                    except:
                        errors.append("please enter valid date of birth !")
                
                if joindate:        
                    try:
                        d=datetime.strptime(joindate,'%d-%m-%Y')
                        if d>datetime.today():
                            errors.append("Invalid joining date !")
                    except:
                        errors.append("please enter valid joining date !")
                
                if desig.lower()=='teacher':
                    errors.append("Non teaching staff cann't have designation 'Teacher' !")    
                        
                if not req.FILES.get('image'):
                    errors.append("please attach employee photo !")
                    
                    
            if not errors:
                findsex={'m':'m','f':'f','ms':'f'}
                empObj=tbl_employee.objects.create(desig=desig,isActive=True,joinDate=None)
                fdir=staffUDir+'/'+empPrefix+str(empObj.id)
                
                perD=tbl_empPersonalDetail.objects.create(title=title,
                                                          fName=fname,
                                                          lName=lname,
                                                          sex=findsex[title],
                                                          email=email,
                                                          lAdd=ladd,
                                                          lCity=tbl_location.objects.get(id=lcity),
                                                          lpin=lpin,
                                                          lMobile=lmobile,
                                                          lLandline=llandline,
                                                          pAdd=padd,
                                                          pCity=tbl_location.objects.get(id=pcity),
                                                          ppin=ppin,
                                                          pMobile=pmobile,
                                                          pLandline=plandline,
                                                          image=i_upload(req.FILES.get('image'),fdir,fname+'.jpg')
                                                          )
                empObj.perDetail=perD
                
                if totalExp:
                    empObj.totalExp=int(totalExp)
                if joindate:
                    empObj.joinDate=datetime.strptime(joindate,'%d-%m-%Y')
                if dob:
                    empObj.perDetail.dob=datetime.strptime(dob,'%d-%m-%Y')
                if age:
                    empObj.perDetail.age=int(age)
                if salary:
                    empObj.salary=int(salary)
                if user!=-1:
                    empObj.user=tbl_systemUser.objects.get(id=user)
                if desig:
                    empObj.desig=desig
                
                empObj.perDetail.save()
                empObj.save()
                return HttpResponseRedirect('/staff')
            return render_to_response('addStaff.html',locals(),context_instance=RequestContext(req))
        return render_to_response('addStaff.html',locals(),context_instance=RequestContext(req))


def v_editstaff(req,_id):
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'staff','u'):
        
        users=tbl_systemUser.objects.filter(isActive=True,isSuper=False)
        empPrefix=EMPLOYEE_PREFIX
        empObj=tbl_employee.objects.get(id=_id)
        empid=empObj.id
        states=tbl_location.objects.filter(pid=1).order_by('name')
        states2=states
        
        
        title=empObj.perDetail.title
        fname=empObj.perDetail.fName
        lname=empObj.perDetail.lName
        
        if empObj.perDetail.dob:
            dob=DateFormat(empObj.perDetail.dob).format('d-m-Y')
        if empObj.perDetail.age:
            age=empObj.perDetail.age
        if empObj.perDetail.email:
            email=empObj.perDetail.email
        
        if empObj.perDetail.lAdd:
            ladd=empObj.perDetail.lAdd
        if empObj.perDetail.lCity:
            lstate=tbl_location.objects.get(id=empObj.perDetail.lCity.pid).id
            cities=tbl_location.objects.filter(pid=lstate).order_by('name')
            lcity=empObj.perDetail.lCity.id
        if empObj.perDetail.lpin:
            lpin=empObj.perDetail.lpin
        if empObj.perDetail.lMobile:
            lmobile=empObj.perDetail.lMobile
        if empObj.perDetail.lLandline:
            llandline=empObj.perDetail.lLandline
     
        
        if empObj.perDetail.pAdd:
            padd=empObj.perDetail.pAdd
        if empObj.perDetail.pCity:
            pstate=tbl_location.objects.get(id=empObj.perDetail.pCity.pid).id
            cities2=tbl_location.objects.filter(pid=pstate).order_by('name')
            pcity=empObj.perDetail.pCity.id
        if empObj.perDetail.ppin:
            ppin=empObj.perDetail.ppin
        if empObj.perDetail.pMobile:
            pmobile=empObj.perDetail.pMobile
        if empObj.perDetail.pLandline:
            plandline=empObj.perDetail.pLandline
        if empObj.perDetail.image:
            photoPath=uploadFolder+empObj.perDetail.image.url    
        
        
        
        if empObj.totalExp:
            totalExp=empObj.totalExp
        if empObj.joinDate:
            joindate=DateFormat(empObj.joinDate).format('d-m-Y')
        if empObj.desig:
            desig=empObj.desig
        if empObj.user:
            user=empObj.user.id
        if empObj.salary:
            salary=empObj.salary
        if req.POST.get('editStaff',''):
            errors=[]
            eduDetails=[]
            expDetails=[]
            fdir=staffUDir+'/'+empPrefix+str(empObj.id)
            
            joindate=req.POST.get('joindate',None).strip()
            totalExp=req.POST.get('totalExp','').strip()
            desig=req.POST.get('desig','').strip()
            salary=req.POST.get('salary','')
            user=int(req.POST.get('user',-1))
            
            title=req.POST.get('title','')
            fname=req.POST.get('fname','').strip()
            lname=req.POST.get('lname','').strip()
            dob=req.POST.get('dob','').strip()
            age=req.POST.get('age','').strip()
            email=req.POST.get('email','').strip()
            
            
            
            ladd=req.POST.get('ladd','').strip()
            lstate=int(req.POST.get('lstate',-1))
            if lstate!=-1:
                cities=tbl_location.objects.filter(pid=lstate).order_by('name')
            lcity=int(req.POST.get('lcity',-1))
            lpin=req.POST.get('lpin','').strip()
            lmobile=req.POST.get('lmobile','').strip()
            llandline=req.POST.get('llandline','').strip()
            
            padd=req.POST.get('padd','').strip()
            pstate=int(req.POST.get('pstate',-1))
            if pstate!=-1:
                cities2=tbl_location.objects.filter(pid=pstate).order_by('name')
            pcity=int(req.POST.get('pcity',-1))
            ppin=req.POST.get('ppin','').strip()
            pmobile=req.POST.get('pmobile','').strip()
            plandline=req.POST.get('plandline','').strip()
            
            
            if title=='-1':
                errors.append("please select at least one title !")
            elif not fname:
                errors.append("please enter first name !")
            elif not lname:
                errors.append("please enter last name !")
            elif email and '@' not in email:
                    errors.append("please enter valid email Id !")
            
            elif not ladd:
                errors.append("please enter address of local residence !")
            elif lstate==-1:
                errors.append("please select one state of local residence !")
            elif lcity==-1:
                errors.append("please select one city of local residence !")
            elif not lpin:
                errors.append("please enter pincode of local residence !")
            elif not lmobile:
                errors.append("please enter mobile no. of local residence !")
            elif len(lmobile)<10:
                errors.append("please enter valid mobile no. of local residence !")
            elif not llandline:
                errors.append("please enter landline no. of local residence !")
            elif len(llandline)<7:
                errors.append("please enter valid landline no. of local residence !")
            
            
            elif not padd:
                errors.append("please enter address of permanent residence !")
            elif pstate==-1:
                errors.append("please select one state of permanent residence !")
            elif pcity==-1:
                errors.append("please select one city of permanent residence !")
            elif not ppin:
                errors.append("please enter pincode of permanent residence !")
            elif not pmobile:
                errors.append("please enter mobile no. of permanent residence !")
            elif len(pmobile)<10:
                errors.append("please enter valid mobile no. of permanent residence !")
            elif not plandline:
                errors.append("please enter landline no. of permanent residence !")
            elif len(plandline)<7:
                errors.append("please enter valid landline no. of permanent residence !")
            elif not empObj.perDetail.image and not req.FILES.get('image'):
                errors.append("please attach employee photo !")
            else:
                if dob:
                    try:
                        datetime.strptime(dob,'%d-%m-%Y')
                    except:
                        errors.append("please enter valid date of birth !")
                
                if joindate:        
                    try:
                        d=datetime.strptime(joindate,'%d-%m-%Y')
                        if d>datetime.today():
                            errors.append("Invalid joining date !")
                    except:
                        errors.append("please enter valid joining date !")
                
            if not errors:
                findsex={'m':'m','f':'f','ms':'f'}
                
                empObj.perDetail.title=title
                empObj.perDetail.fName=fname
                empObj.perDetail.lName=lname
                if age:
                    empObj.perDetail.age=age
                else:
                    empObj.perDetail.age=None
                empObj.perDetail.sex=findsex[title]
                if dob:
                    empObj.perDetail.dob=datetime.strptime(dob,'%d-%m-%Y')
                else:
                    empObj.perDetail.dob=None
                
                if email:
                    empObj.perDetail.email=email
                else:
                    empObj.perDetail.email=None
                    
                    
                empObj.perDetail.lAdd=ladd
                empObj.perDetail.lCity=tbl_location.objects.get(id=lcity)
                empObj.perDetail.lpin=lpin
                empObj.perDetail.lMobile=lmobile
                empObj.perDetail.lLandline=llandline
                empObj.perDetail.pAdd=padd
                empObj.perDetail.pCity=tbl_location.objects.get(id=pcity)
                empObj.perDetail.ppin=ppin
                empObj.perDetail.pMobile=pmobile
                empObj.perDetail.pLandline=plandline
                if req.FILES.get('image'):
                    empObj.perDetail.image=i_upload(req.FILES.get('image'),fdir,fname+'.jpg')
                
                if totalExp:
                    empObj.totalExp=int(totalExp)
                else:
                    empObj.totalExp=None
                if joindate:
                    empObj.joinDate=datetime.strptime(joindate,'%d-%m-%Y')
                else:
                    empObj.joinDate=None
                if salary:
                    empObj.salary=int(salary)
                else:
                    empObj.salary=None
                if user==-1:
                    empObj.user=None
                else:
                    empObj.user=tbl_systemUser.objects.get(id=user)
                if desig:    
                    empObj.desig=desig
                else:
                    empObj.desig=None
                empObj.perDetail.save()
                empObj.save()
                return HttpResponseRedirect('/staff/edit/'+str(empObj.id))
            return render_to_response('editStaff.html',locals(),context_instance=RequestContext(req))
        return render_to_response('editStaff.html',locals(),context_instance=RequestContext(req))