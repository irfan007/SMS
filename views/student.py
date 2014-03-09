from django.http import HttpResponse
from django.shortcuts import render_to_response
import datetime
from App.models import tbl_student, tbl_stdPersonalDetail,\
    tbl_stdEducationalDetail, tbl_location, tbl_standard, tbl_medium,\
    tbl_shortstandard, tbl_class, tbl_doc, tbl_sibling, tbl_MSS,\
    tbl_classStudent, tbl_examType, tbl_subjectMarks, tbl_subject,\
    tbl_studentLog, tbl_employee, tbl_school, tbl_feetype, tbl_studentFacility,\
    tbl_systemUser, Notice, tbl_role, tbl_feePayment, tbl_subjectAndTeacher
from django.http import HttpResponseRedirect
from SMS.settings import MEDIA_ROOT, studentUDir, uploadFolder, STUDENTPREFIX,\
    manavPageParameter, userUDir
from django.forms.fields import DateField
from django.db.models import Max
from django.template.context import RequestContext
from views.permission import i_hasPermission
from views.systemUser import isUser, getUserByEmail
from getpass import getuser
from App.pp import i_upload
#from views.fees import getvalidstudent


def getvalidstudent(studid):
    '''
    helps to access student by its id
    '''
    prefix=studid[:len(STUDENTPREFIX)]
    if prefix.upper()==STUDENTPREFIX:
        try:
            getid=int(studid[len(STUDENTPREFIX):])
            uniqueobj=tbl_student.objects.get(id=getid)
            return uniqueobj 
        except:
            return None

def dateformatConvertor(date):
    '''
    covert one date format into another
    '''
    date=datetime.datetime.strptime(date, '%d-%m-%Y')
    return date.strftime('%Y-%m-%d')
def v_test(req):
   
    return render_to_response('test3.html')


def v_searchStudent(req):
    '''
    used to search student by its id,name and other parameters
    '''
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'student','v'): 
    
        allMSS=tbl_MSS.objects.filter(isActive=True)
        errors=[]
        rows=[]
        if req.POST.get('advancesearch',''):
            getid=req.POST.get('studentid','')
            fname=req.POST.get('fname','')
            lname=req.POST.get('lname','')
            getMSS=int(req.POST.get('getMSS',''))
            
            if getid:
                getstud=getvalidstudent(getid)
                if getstud:
                    rows.append(getstud)
                    return render_to_response('studentInfo.html',locals(),context_instance=RequestContext(req))
                else:
                    errors.append("Please enter valid student id!")
                    return render_to_response('studentInfo.html',locals(),context_instance=RequestContext(req))
            if getMSS>0:
                getMSSobj=tbl_MSS.objects.get(id=getMSS)
                getrows=tbl_student.objects.filter(standard=getMSSobj.standard,section=getMSSobj.section)
                
                for data in getrows:
                    if fname.upper() in data.perDetail.fName.upper():
                        
                        if lname.upper() in data.perDetail.lName.upper():
                            rows.append(data)
                rows=set(rows)
                return render_to_response('studentInfo.html',locals(),context_instance=RequestContext(req))
            if not fname:
                fname=''
            if not lname:
                lname=''
            allStud=tbl_student.objects.filter()
            
            for data in allStud:
                if fname.upper() in data.perDetail.fName.upper():
                    
                    if lname.upper() in data.perDetail.lName.upper():
                        rows.append(data)
            rows=set(rows)
            return render_to_response('studentInfo.html',locals(),context_instance=RequestContext(req))
            
        return render_to_response('studentInfo.html',locals(),context_instance=RequestContext(req))

def v_student(req):#this function is written to carry out listing of students
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'student','v'): 
        x=STUDENTPREFIX
       
        rows=tbl_student.objects.filter()
        pagination_parameter=manavPageParameter    #Used for next and previous (i.e pagination)
        
        NEXT=False
        totalRows=len(rows)
        TO=len(rows)
        if len(rows)>pagination_parameter:
            TO=pagination_parameter
            NEXT=True
        FROM=1
        rows=rows[:pagination_parameter]
        allMSS=tbl_MSS.objects.filter(isActive=True)
        return render_to_response('student.html',locals(),context_instance=RequestContext(req))
    

def v_nextStudent(req,para):
    '''
    used to find next list of students having rows equal to manavPageParameter
    '''
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'student','v'):
        para=int(para)
        FROM=para+1
        pagination_parameter=manavPageParameter
        
        pagination_parameter=pagination_parameter+para
        
        rows=tbl_student.objects.filter()
        totalRows=len(rows)
        NEXT=False
        TO=len(rows)
        if len(rows)>pagination_parameter:
            TO=pagination_parameter
            NEXT=True
        rows=rows[para:pagination_parameter]
        PREV="True"
        back=para
        allMSS=tbl_MSS.objects.filter(isActive=True)
    
        return render_to_response('student.html',locals(),context_instance=RequestContext(req))

def v_prevStudent(req,para):
    '''
    used to find previous list of students having rows equal to manavPageParameter
    '''
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'student','v'):
        para=int(para)
        TO=para
        pagination_parameter=manavPageParameter
        back=para-pagination_parameter
        
        rows=tbl_student.objects.filter()
        totalRows=len(rows)
        NEXT=False
        FROM=back+1
        if len(rows)>back:
            NEXT=True
        rows=rows[back:para]
        if back==0:
            PREV=False
        else:
            PREV=True
        allMSS=tbl_MSS.objects.filter(isActive=True)
        return render_to_response('student.html',locals(),context_instance=RequestContext(req))


def v_addStudent(req): 
    '''
    this method will add new admitted student in the student database
    '''
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'student','a'):
        facilities=tbl_feetype.objects.filter(facility=True)
        overallFac=[[x,None] for x in facilities]
        
        errors=[]
        schoolobj=tbl_school.objects.filter()
        
        if not schoolobj:
            errors.append("Please specify the school details in setting of configuration!")
            return render_to_response('student.html',locals(),context_instance=RequestContext(req))
        states=tbl_location.objects.filter(pid=1).order_by('name')
        mediums=tbl_medium.objects.filter(isActive=True)
        getmed=None
        if len(mediums)==1:
            getmed=mediums[0]
            mediums=[]
            
        shortstandards=tbl_shortstandard.objects.all()
        sections=tbl_class.objects.filter(isActive=True)
        if req.POST.get('addStudent'):
            '''This will perform form validation on various 
            personal details parameter of student,parents information and other information needed to get admission'''
            
            adddate=req.POST.get('adddate','').strip()
            firstname=req.POST.get('firstname','').strip()
            lastname=req.POST.get('lastname','').strip()
            dob=req.POST.get('dob','').strip()
            age=req.POST.get('age','').strip()
                
            sex=req.POST.get('sex','')
            if not mediums:
                medium=getmed.id
            else:
                medium=int(req.POST.get('medium',''))
            shortstandard=int(req.POST.get('shortstandard','')) # shortstandard is just to access the name of standard
            section=int(req.POST.get('section',''))
            laddress=req.POST.get('laddress','').strip()
            getlstate=int(req.POST.get('lstate',''))
            if getlstate>=1:
                lcities=tbl_location.objects.filter(pid=getlstate).order_by('name')
            else:
                lcities=None
            getlcity=int(req.POST.get('lcity',''))
            
            lpincode=req.POST.get('lpincode','').strip()
                
            lcontact=req.POST.get('lcontact','').strip()
                
            lmobileno=req.POST.get('lmobileno','').strip()
            for ff in overallFac:
                fac=req.POST.get('fac'+str(ff[0].id),'')
                ff[1]=fac
            
                
            if req.POST.get('psamel','')=='1':
                paddress=laddress
                getpstate=getlstate
                pcities=lcities
                getpcity=getlcity
                ppincode=lpincode
                pcontact=lcontact
                pmobileno=lmobileno
            else:  
                paddress=req.POST.get('paddress','').strip()
                getpstate=int(req.POST.get('pstate',''))
                if getpstate>=1:
                    pcities=tbl_location.objects.filter(pid=getpstate).order_by('name')
                getpcity=int(req.POST.get('pcity',''))
            
                ppincode=req.POST.get('ppincode','').strip()
                pcontact=req.POST.get('pcontact','').strip()
                
                pmobileno=req.POST.get('pmobileno','').strip()
            
            fathername=req.POST.get('fathername','').strip()
            fatheroccupation=req.POST.get('fatheroccupation','').strip()
            fathersalary=req.POST.get('fathersalary','').strip()
            
                    
            fatherofficeno=req.POST.get('fatherofficeno','').strip()
                
            fathermobileno=req.POST.get('fathermobileno','').strip()
            
                
                
            mothername=req.POST.get('mothername','').strip()
            motheroccupation=req.POST.get('motheroccupation','').strip()
            mothersalary=req.POST.get('mothersalary','').strip()
            
            motherofficeno=req.POST.get('motherofficeno','').strip()
            
            mothermobileno=req.POST.get('mothermobileno','').strip()
                
            otherpersonname=req.POST.get('otherpersonname','').strip()
            otherpersonno=req.POST.get('otherpersonno','').strip()
            
            relation=req.POST.get('relation','').strip()
            preschoolname=req.POST.get('preschoolname','').strip()
            
            prestandard=req.POST.get('prestandard','').strip()
            prepassingyear=req.POST.get('prepassingyear','').strip()
            oldAddNo=req.POST.get('oldAddNo','').strip()
            oldRollNo=req.POST.get('oldRollNo','').strip()
            premedium=req.POST.get('premedium','').strip()
            sib1id=req.POST.get('sib1id','').strip()
            sib1name=req.POST.get('sib1name','').strip()
            
            status=True
            temp=""
            try:
                
                temp="admission date!"
                adddate1=dateformatConvertor(adddate)
                temp="date of birth!"     
                dob1=dateformatConvertor(dob)
                
                    
                   
            except:
                
                errors.append("Please enter valid "+temp)
            
                return render_to_response('addStudent.html',locals(),context_instance=RequestContext(req))
            if not firstname:
                errors.append("Please enter the first name in personal details!")
            elif not lastname:
                errors.append("Please enter the last name in personal details!")
            elif not dob:
                errors.append("Please enter the date of birth in personal details!")
            elif sex=="-1":
                errors.append("Please select the sex in personal details!")
            elif medium==-1:
                errors.append("Please select the medium !")
                
            elif shortstandard==-1:
                errors.append("Please select the standard !")
            elif section==-1:
                errors.append("Please select the section!")
                
            elif not laddress:
                errors.append("Please enter local address in personal details!")
            elif not paddress:
                errors.append("Please enter permanent address in personal details!")
            elif not lmobileno:
                errors.append("Please enter mobile no in local address detail !")
            if errors:
                return render_to_response('addStudent.html',locals(),context_instance=RequestContext(req))
            if lcontact:
                if len(lcontact)<6:
                    errors.append("Please enter the valid contact no in local address details!")
                    return render_to_response('addStudent.html',locals(),context_instance=RequestContext(req))
            if lmobileno:
                if len(lmobileno)<10:
                    errors.append("Please enter valid mobile no in local address details !")
                    return render_to_response('addStudent.html',locals(),context_instance=RequestContext(req))
            if not pmobileno:
                
                errors.append("Please enter mobile no in permanent address detail!")
                return render_to_response('addStudent.html',locals(),context_instance=RequestContext(req))
            if pcontact:
                if len(pcontact)<6:
                    errors.append("Please enter the valid contact no in permanent address details!")
                    return render_to_response('addStudent.html',locals(),context_instance=RequestContext(req))
    
            if pmobileno:
                if len(pmobileno)<10:
                    errors.append("Please enter valid mobile no in permanent address details !")
                    return render_to_response('addStudent.html',locals(),context_instance=RequestContext(req))
                    
            if getlstate<1:
                errors.append("Please select state in local address details!")
                return render_to_response('addStudent.html',locals(),context_instance=RequestContext(req))        
            if getlcity<1:
                errors.append("Please select city in local address details!")
                return render_to_response('addStudent.html',locals(),context_instance=RequestContext(req))
            if getpstate<1:
                errors.append("Please select state in permanent address details!")
                return render_to_response('addStudent.html',locals(),context_instance=RequestContext(req))        
            if getpcity<1:
                errors.append("Please select city in permanent address details!")
                return render_to_response('addStudent.html',locals(),context_instance=RequestContext(req))    
            if fathermobileno or fatherofficeno or fathersalary or fatheroccupation:
                if not fathername:
                    errors.append("Please enter the father name!")
            if mothermobileno or motherofficeno or mothersalary or motheroccupation:
                if not mothername:
                    errors.append("Please enter the mother name!")
            if errors:
                return render_to_response('addStudent.html',locals(),context_instance=RequestContext(req))
            
            try:
                age=int(age)
            except:
                errors.append("Please enter valid dob !")
                return render_to_response('addStudent.html',locals(),context_instance=RequestContext(req))
            if age<1:
                errors.append("Please enter the valid dob !")
                return render_to_response('addStudent.html',locals(),context_instance=RequestContext(req))
            rows=tbl_standard.objects.filter(name=tbl_shortstandard.objects.get(id=shortstandard).name)
            getfilter=rows.filter(medium=tbl_medium.objects.get(id=medium))
            if not getfilter:
                errors.append("Please select valid medium,standard,section")
            else:
                getmorefilter=getfilter.filter(sections=tbl_class.objects.get(id=section))
                if not getmorefilter:
                    errors.append("Please select valid medium,standard,section")
            if errors:
                return render_to_response('addStudent.html',locals(),context_instance=RequestContext(req))
            if fathermobileno:
                if len(fathermobileno)<10:
                    errors.append("Please enter the valid father mobile no")
                    return render_to_response('addStudent.html',locals(),context_instance=RequestContext(req))
            if fatherofficeno:
                if len(fatherofficeno)<6:
                    errors.append("Please enter the valid father contact no")
                    return render_to_response('addStudent.html',locals(),context_instance=RequestContext(req))
            if motherofficeno:
                if len(motherofficeno)<6:
                    errors.append("Please enter the valid mother contact no!")
                    return render_to_response('addStudent.html',locals(),context_instance=RequestContext(req))
            if mothermobileno:
                if len(mothermobileno)<10:
                    errors.append("Please enter valid mother mobile no!")
                    return render_to_response('addStudent.html',locals(),context_instance=RequestContext(req))
            
            
            
            if prestandard or premedium or prepassingyear or oldAddNo or oldRollNo:
                if not preschoolname:
                    errors.append("Please enter the school name!")
                    return render_to_response('addStudent.html',locals(),context_instance=RequestContext(req))
            sib1obj=None
            if sib1id:
                matchPrefix=sib1id[0:len(STUDENTPREFIX)]
                matchPrefix=matchPrefix.upper()
                if matchPrefix!=STUDENTPREFIX:
                    sib1obj=None
                    errors.append("Please enter valid sibling1 id !")
                    return render_to_response('addStudent.html',locals(),context_instance=RequestContext(req))
                else:
                    try:
                        sib1obj=tbl_student.objects.get(id=int(sib1id[len(STUDENTPREFIX):]))
                    except:
                        sib1obj=None
                        errors.append("Please enter valid sibling1 id !")
                        return render_to_response('addStudent.html',locals(),context_instance=RequestContext(req))
            
            sib2id=req.POST.get('sib2id','').strip()
            sib2obj=None
            if sib2id:
                matchPrefix=sib2id[0:len(STUDENTPREFIX)]
                matchPrefix=matchPrefix.upper()
                if matchPrefix!=STUDENTPREFIX:
                    sib2obj=None
                    errors.append("Please enter valid sibling2 id !")
                    return render_to_response('addStudent.html',locals(),context_instance=RequestContext(req))
                else:
                    try:
                        sib2obj=tbl_student.objects.get(id=int(sib2id[len(STUDENTPREFIX):]))
                    except:
                        sib2obj=None
                        errors.append("Please enter valid sibling2 id !")
                        return render_to_response('addStudent.html',locals(),context_instance=RequestContext(req))
            sib3id=req.POST.get('sib3id','').strip()
            
            sib3obj=None
            if sib3id:
                matchPrefix=sib3id[0:len(STUDENTPREFIX)]
                matchPrefix=matchPrefix.upper()
                if matchPrefix!=STUDENTPREFIX:
                    sib3obj=None
                    errors.append("Please enter valid sibling3 id !")
                    return render_to_response('addStudent.html',locals(),context_instance=RequestContext(req))
                else:
                    try:
                        sib3obj=tbl_student.objects.get(id=int(sib3id[len(STUDENTPREFIX):]))
                    except:
                        sib3obj=None
                        errors.append("Please enter valid sibling3 id !")
                        return render_to_response('addStudent.html',locals(),context_instance=RequestContext(req))
            #return HttpResponse(sib3obj)
            
            
                    
            standobj=tbl_standard.objects.filter(medium=tbl_medium.objects.get(id=medium),name=tbl_shortstandard.objects.get(id=shortstandard).name)
            
            secobj=tbl_class.objects.get(id=section)
            
            '''
            inserting data in to the database
            '''
            p1=tbl_student()
            p1.save()
            if sib1obj:
                xx=tbl_sibling()
                xx.studentId=sib1obj.id
                xx.save()
                p1.siblings.add(xx)
            if sib2obj:
                xx=tbl_sibling()
                xx.studentId=sib2obj.id
                xx.save()
                p1.siblings.add(xx)
            if sib3obj:
                xx=tbl_sibling()
                xx.studentId=sib3obj.id
                xx.save()
                p1.siblings.add(xx)
                
            p1.standard=standobj[0]
            p1.section=secobj
            p2=tbl_stdPersonalDetail()
            p2.fName=firstname
            p2.lName=lastname
            p2.age=age
            p2.sex=sex
            p2.dob=dob1
            if req.FILES.get('studImage'):
                
                imagePath=upload(req.FILES['studImage'],str(p1.id))
                p2.image=imagePath
                
            p2.lAdd=laddress
            p2.lCity=tbl_location.objects.get(id=getlcity)
            if lpincode:
                p2.lpin=lpincode
            if lmobileno:    
                p2.lMobile=lmobileno
            if lcontact:
                p2.lLandline=lcontact
            p2.pAdd=paddress
            p2.pCity=tbl_location.objects.get(id=getpcity)
            if ppincode:
                p2.ppin=ppincode
            if pmobileno:
                p2.pMobile=pmobileno
            if pcontact:    
                p2.pLandline=pcontact
            
            
            p2.fatherName=fathername
            p2.fOccupation=fatheroccupation
            if fathersalary:
                p2.fSalary=fathersalary
            if fatherofficeno:    
                p2.fOfficeNo=fatherofficeno
            if fathermobileno:
                p2.fMobile=fathermobileno
            p2.motherName=mothername
            p2.mOccupation=motheroccupation
            if mothersalary:
                p2.mSalary=mothersalary
            if motherofficeno:    
                p2.mOfficeNo=motherofficeno
            if mothermobileno:    
                p2.mMobile=mothermobileno
            p2.personName=otherpersonname
            p2.relation=relation
            if otherpersonno:
                p2.contactNo=otherpersonno
            p2.save()
            if preschoolname:
                p3=tbl_stdEducationalDetail()
                p3.save()
                p3.school=preschoolname
                p3.oldAdmission=oldAddNo
                p3.rollNo=oldRollNo
                p3.standard=prestandard
                if prepassingyear:
                    p3.pYear=prepassingyear
                p3.medium=premedium
                if req.FILES.get('documents',''):
                
                    imagePath1=upload1(req.FILES['documents'],'document'+str(p3.id),str(p1.id))
                    new=tbl_doc()
                    new.name=new.id
                    new.belongTo='s'
                    new.file=imagePath1
                    new.save()
                    p3.docs.add(new)
                if req.FILES.get('tc',''):
                
                    imagePath1=upload1(req.FILES['tc'],'tc'+str(p3.id),str(p1.id))
                    new=tbl_doc()
                    new.name=new.id
                    new.belongTo='s'
                    new.file=imagePath1
                    new.save()
                    p3.docs.add(new)
                if req.FILES.get('cc',''):
                
                    imagePath1=upload1(req.FILES['cc'],'cc'+str(p3.id),str(p1.id))
                    new=tbl_doc()
                    new.name=new.id
                    new.belongTo='s'
                    new.file=imagePath1
                    new.save()
                    p3.docs.add(new)
                if req.FILES.get('mc',''):
                
                    imagePath1=upload1(req.FILES['mc'],'mc'+str(p3.id),str(p1.id))
                    new=tbl_doc()
                    new.name=new.id
                    new.belongTo='s'
                    new.file=imagePath1
                    new.save()
                    p3.docs.add(new)
                
                p3.save()
            else:
                p3=None
            
            for fac in overallFac:
                if fac[1]:
                    newRowFac=tbl_studentFacility()
                    newRowFac.facility=fac[0]
                    newRowFac.save()
                    p1.facilities.add(newRowFac)
            p1.perDetail=p2
            p1.eduDetail=p3
            p1.isActive=status
            p1.createdOn=adddate1
            p1.save()
            obj=tbl_MSS.objects.get(medium=p1.standard.medium,standard=p1.standard,section=p1.section)
            newobject=tbl_studentLog()
            newobject.mss=obj
            
            
            newobject.session1=schoolobj[0].getSession()
            newobject.save()
            new=tbl_classStudent()
            new.studentId=p1.id
                
            new.save()
            obj.students.add(new)
            p1.history.add(newobject)
            obj.save()
            return HttpResponseRedirect('/students/') 
                
        return render_to_response('addStudent.html',locals(),context_instance=RequestContext(req))

        
def i_getAllStates(byCountryId):
    try:
        return tbl_location.objects.filter(pid=byCountryId).order_by('name')
    except tbl_location.DoesNotExist:
        return 0
    
    
def upload(fileObj,name):
    '''
    this method is written to carry out jpeg image upload
    '''
    import os
    subDirectory=studentUDir
    try:
        with open(MEDIA_ROOT+subDirectory+'/'+name+'/'+str(name)+'image'+".jpeg", 'w') as destination:
            for chunk in fileObj.chunks():
                destination.write(chunk)
        return subDirectory+'/'+name+'/'+name+'image'+".jpeg"
    except IOError:
        if not os.path.exists(MEDIA_ROOT+subDirectory):
            os.makedirs(MEDIA_ROOT+subDirectory)
        os.mkdir(MEDIA_ROOT+subDirectory+'/'+name)
        with open(MEDIA_ROOT+subDirectory+'/'+name+'/'+str(name)+'image'+".jpeg", 'w') as destination:
            for chunk in fileObj.chunks():
                destination.write(chunk)
        return subDirectory+'/'+name+'/'+name+'image'+".jpeg"
def upload1(fileObj,name,name1):
    '''
    this method is written to carry out upload of student document
    '''
    import os
    subDirectory=studentUDir
    try:
        with open(MEDIA_ROOT+subDirectory+'/'+name1+'/'+str(name)+'doc'+".jpeg", 'w') as destination:
            for chunk in fileObj.chunks():
                destination.write(chunk)
        return subDirectory+'/'+name1+'/'+name+'doc'+".jpeg"
    except IOError:
        if not os.path.exists(MEDIA_ROOT+subDirectory):
            os.makedirs(MEDIA_ROOT+subDirectory)
        if not os.path.exists(MEDIA_ROOT+subDirectory+'/'+name1):
            os.makedirs(MEDIA_ROOT+subDirectory+'/'+name1)
        with open(MEDIA_ROOT+subDirectory+'/'+name1+'/'+str(name)+'doc'+".jpeg", 'w') as destination:
            for chunk in fileObj.chunks():
                destination.write(chunk)
        return subDirectory+'/'+name1+'/'+name+'doc'+".jpeg"

def v_editStudent(req,para): 
    '''
    this method is written to carry out editing of student information feed in database
    '''
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'student','u'):
        facilities=tbl_feetype.objects.filter(facility=True)
        overallFac=[[x,None] for x in facilities]
        errors=[]
        schoolobj=tbl_school.objects.filter()
        
        if not schoolobj:
            errors.append("Please specify the school details in setting of configuration!")
            return render_to_response('student.html',locals(),context_instance=RequestContext(req))
        mediums=tbl_medium.objects.all()
        shortstandards=tbl_shortstandard.objects.all()
        sections=tbl_class.objects.all()
        states=tbl_location.objects.filter(pid=1).order_by('name')
        para=int(para)
        getstud=tbl_student.objects.get(id=para)
        
        if not req.POST.get('editStudent',''):
        
       
            for fac in overallFac:
                if getstud.facilities.filter(facility=fac[0]):
                    fac[1]="1"
            status=getstud.isActive
            if status==True:
                status="1"
            else:
                status="2"
            
            addate=getstud.createdOn
            addate=dateformatReverse(str(addate))
            firstname=getstud.perDetail.fName
            lastname=getstud.perDetail.lName
            dob=dateformatReverse(str(getstud.perDetail.dob))
            age=getstud.perDetail.age
            sex=getstud.perDetail.sex
            #mssid=getstud.history.filter(session1=getstud)[0].mss
            mssid=tbl_MSS.objects.get(standard=getstud.standard,medium=getstud.standard.medium,section=getstud.section)
            medium=mssid.medium.id
            shortstandard=tbl_shortstandard.objects.filter(name=mssid.standard.name)[0].id
            section=mssid.section.id
            siblings=getstud.siblings.all()
            sibtemp=[]
            for data in siblings:
                
                sibtemp.append(data.getsibid())
                sibtemp.append(data.getsibname())
            try:
                image=getstud.perDetail.image.url
                image=uploadFolder+image
            except:
                image=""    
            laddress=getstud.perDetail.lAdd
            getlcity=getstud.perDetail.lCity.id
            getlstate=getstud.perDetail.lCity.pid
            lcities=tbl_location.objects.filter(pid=getlstate).order_by('name')
            if getstud.perDetail.lpin:
                lpincode=getstud.perDetail.lpin
            
            if getstud.perDetail.lMobile:
                lmobileno=getstud.perDetail.lMobile
            if getstud.perDetail.lLandline:
                lcontact=getstud.perDetail.lLandline
            paddress=getstud.perDetail.pAdd
            getpcity=getstud.perDetail.pCity.id
            getpstate=getstud.perDetail.pCity.pid
            pcities=tbl_location.objects.filter(pid=getpstate).order_by('name')
            if getstud.perDetail.ppin:
                ppincode=getstud.perDetail.ppin
            if getstud.perDetail.pLandline:
                pcontact=getstud.perDetail.pLandline
            if getstud.perDetail.pMobile:
                pmobileno=getstud.perDetail.pMobile
            fathername=getstud.perDetail.fatherName
            fatheroccupation=getstud.perDetail.fOccupation
            if getstud.perDetail.fSalary:
                fathersalary=getstud.perDetail.fSalary
            if getstud.perDetail.fOfficeNo:
                fatherofficeno=getstud.perDetail.fOfficeNo
            if getstud.perDetail.fMobile:
                fathermobileno=getstud.perDetail.fMobile
            mothername=getstud.perDetail.motherName
            motheroccupation=getstud.perDetail.mOccupation
            if getstud.perDetail.mSalary:
                mothersalary=getstud.perDetail.mSalary
            if getstud.perDetail.mOfficeNo:
                motherofficeno=getstud.perDetail.mOfficeNo
            if getstud.perDetail.mMobile:
                mothermobileno=getstud.perDetail.mMobile
            otherpersonname=getstud.perDetail.personName
            if getstud.perDetail.contactNo:
                otherpersonno=getstud.perDetail.contactNo
            relation=getstud.perDetail.relation
            if getstud.eduDetail:
                preschoolname=getstud.eduDetail.school
                prestandard=getstud.eduDetail.standard
                oldAddNo=getstud.eduDetail.oldAdmission
                oldRollNo=getstud.eduDetail.rollNo
                if getstud.eduDetail.pYear:
                    prepassingyear=getstud.eduDetail.pYear
                premedium=getstud.eduDetail.medium
                
                    
                tempo=getstud.eduDetail.docs.all()
                for tt in tempo: 
                    
                    
                    getAdd=tt.file.url
                    if getAdd:
                        listing=getAdd.split('/')
                        if 'document' in listing[-1]:
                            documents=uploadFolder+getAdd
                        elif 'cc' in listing[-1]:
                            cc=uploadFolder+getAdd
                        elif 'tc' in listing[-1]:
                            tc=uploadFolder+getAdd
                        elif 'mc' in listing[-1]:
                            mc=uploadFolder+getAdd
                            
                
                
        if req.POST.get('editStudent',''):
            
            errors=[]
            '''This will perform form validation on various 
            personal details parameter of student,parents information and other information needed to get admission'''
            for ff in overallFac:
                fac=req.POST.get('fac'+str(ff[0].id),'')
                ff[1]=fac
            sibtemp=[]
            getstud.facilities.all().delete()
            
            for fac in overallFac:
                if fac[1]:
                    newFacility=tbl_studentFacility()
                    newFacility.facility=fac[0]
                    newFacility.save()
                    getstud.facilities.add(newFacility)
                
            addate=req.POST.get('addate','').strip()
            
            firstname=req.POST.get('firstname','').strip()
            lastname=req.POST.get('lastname','').strip()
            dob=req.POST.get('dob','').strip()
            age=req.POST.get('age','').strip()
                
            sex=req.POST.get('sex','')
            medium=int(req.POST.get('medium',''))
            shortstandard=int(req.POST.get('shortstandard',''))
            section=int(req.POST.get('section',''))
            
            laddress=req.POST.get('laddress','').strip()
            getlstate=int(req.POST.get('lstate',''))
            status=req.POST.get('status','')
            if getlstate>=1:
                lcities=tbl_location.objects.filter(pid=getlstate).order_by('name')
                
            
            getlcity=int(req.POST.get('lcity',''))
            
            
            lpincode=req.POST.get('lpincode','').strip()
                
            lcontact=req.POST.get('lcontact','').strip()
                
            lmobileno=req.POST.get('lmobileno','').strip()  
            paddress=req.POST.get('paddress','').strip()
            getpstate=int(req.POST.get('pstate',''))
            if getpstate>=1:
                pcities=tbl_location.objects.filter(pid=getpstate).order_by('name') 
            getpcity=int(req.POST.get('pcity',''))
            
            ppincode=req.POST.get('ppincode','').strip()
                
            pcontact=req.POST.get('pcontact','').strip()
                
            pmobileno=req.POST.get('pmobileno','').strip()
                
            fathername=req.POST.get('fathername','').strip()
            fatheroccupation=req.POST.get('fatheroccupation','').strip()
            fathersalary=req.POST.get('fathersalary','').strip()
            
                    
            fatherofficeno=req.POST.get('fatherofficeno','').strip()
                
            fathermobileno=req.POST.get('fathermobileno','').strip()
            
                
                
            mothername=req.POST.get('mothername','').strip()
            motheroccupation=req.POST.get('motheroccupation','').strip()
            mothersalary=req.POST.get('mothersalary','').strip()
            
            motherofficeno=req.POST.get('motherofficeno','').strip()
            
            mothermobileno=req.POST.get('mothermobileno','').strip()
                
            otherpersonname=req.POST.get('otherpersonname','').strip()
            otherpersonno=req.POST.get('otherpersonno','').strip()
            
            relation=req.POST.get('relation','').strip()
            preschoolname=req.POST.get('preschoolname','').strip()
            
            prestandard=req.POST.get('prestandard','').strip()
            prepassingyear=req.POST.get('prepassingyear','').strip()
            
                    
            premedium=req.POST.get('premedium','').strip()
            sib1id=req.POST.get('sib1id','').strip()
            sib1name=req.POST.get('sib1name','').strip()
            sib2id=req.POST.get('sib2id','').strip()
            sib2name=req.POST.get('sib2name','').strip()
            sib3id=req.POST.get('sib3id','').strip()
            sib3name=req.POST.get('sib3name','').strip()
            sibtemp.append(sib1id)
            sibtemp.append(sib1name)
            sibtemp.append(sib2id)
            sibtemp.append(sib2name)
            sibtemp.append(sib3id)
            sibtemp.append(sib3name)
            
            oldRollNo=req.POST.get('oldRollNo','').strip()
            oldAddNo=req.POST.get('oldAddNo','').strip()
            temp=""
            try:
                
                temp="admission date!"
                addate1=dateformatConvertor(addate)
                
                temp="date of birth!"
                dob1=dateformatConvertor(dob)
            except:
                errors.append("Please enter valid "+temp)
            if status=="1":
                getstud.isActive=True
            else:
                getstud.isActive=False
            if errors:
                return render_to_response('editStudent.html',locals(),context_instance=RequestContext(req))
            if not firstname:
                errors.append("Please enter the first name in personal details!")
            elif not lastname:
                errors.append("Please enter the last name in personal details!")
            elif not dob:
                errors.append("Please enter the date of birth in personal details!")
            elif sex=="-1":
                errors.append("Please select the sex in personal details!")
            
            elif shortstandard==-1:
                errors.append("Please select the standard !")
            
            elif not laddress:
                errors.append("Please enter local address in personal details!")
            elif not paddress:
                errors.append("Please enter permanent address in personal details!")
            elif not lmobileno:
                errors.append("Please enter local mobile no !")
            if errors:
                return render_to_response('editStudent.html',locals(),context_instance=RequestContext(req))        
            if not pmobileno:
                
                errors.append("Please enter permanent mobile no !")
                return render_to_response('editStudent.html',locals(),context_instance=RequestContext(req))
            if lcontact:
                if len(lcontact)<6:
                    errors.append("Please enter the valid contact no in local address details!")
                    return render_to_response('editStudent.html',locals(),context_instance=RequestContext(req))
            if lmobileno:
                if len(lmobileno)<10:
                    errors.append("Please enter valid mobile no in local address details !")
                    return render_to_response('editStudent.html',locals(),context_instance=RequestContext(req))
            
            if pcontact:
                if len(pcontact)<6:
                    errors.append("Please enter the valid contact no in permanent address details!")
                    return render_to_response('editStudent.html',locals(),context_instance=RequestContext(req))
    
            if pmobileno:
                if len(pmobileno)<10:
                    errors.append("Please enter valid mobile no in permanent address details !")
                    return render_to_response('editStudent.html',locals(),context_instance=RequestContext(req))
            if getlstate<1:
                errors.append("Please select state in local address details!")
                return render_to_response('editStudent.html',locals(),context_instance=RequestContext(req))        
            if getlcity<1:
                errors.append("Please select city in local address details!")
                return render_to_response('editStudent.html',locals(),context_instance=RequestContext(req))
            if getpstate<1:
                errors.append("Please select state in permanent address details!")
                return render_to_response('editStudent.html',locals(),context_instance=RequestContext(req))        
            if getpcity<1:
                errors.append("Please select city in permanent address details!")    
                return render_to_response('editStudent.html',locals(),context_instance=RequestContext(req))
            if fathermobileno or fatherofficeno or fathersalary or fatheroccupation:
                if not fathername:
                    errors.append("Please enter the father name!")
                    return render_to_response('editStudent.html',locals(),context_instance=RequestContext(req))
            if mothermobileno or motherofficeno or mothersalary or motheroccupation:
                if not mothername:
                    errors.append("Please enter the mother name!")
                    return render_to_response('editStudent.html',locals(),context_instance=RequestContext(req))
            if errors:
                return render_to_response('editStudent.html',locals(),context_instance=RequestContext(req))
            try:
                age=int(age)
            except:
                errors.append("Please enter valid dob !")
                return render_to_response('editStudent.html',locals(),context_instance=RequestContext(req))
            if age<1:
                errors.append("Please enter the valid dob !")
                return render_to_response('editStudent.html',locals(),context_instance=RequestContext(req))
            
            if fathermobileno:
                if len(fathermobileno)<10:
                    errors.append("Please enter the valid father mobile no")
                    return render_to_response('editStudent.html',locals(),context_instance=RequestContext(req))
            if fatherofficeno:
                if len(fatherofficeno)<6:
                    errors.append("Please enter the valid father contact no")
                    return render_to_response('editStudent.html',locals(),context_instance=RequestContext(req))
            if motherofficeno:
                if len(motherofficeno)<6:
                    errors.append("Please enter the valid mother contact no!")
                    return render_to_response('editStudent.html',locals(),context_instance=RequestContext(req))
            if mothermobileno:
                if len(mothermobileno)<10:
                    errors.append("Please enter valid mother mobile no!")
                    return render_to_response('editStudent.html',locals(),context_instance=RequestContext(req))
            rows=tbl_standard.objects.filter(name=tbl_shortstandard.objects.get(id=shortstandard).name)
            getfilter=rows.filter(medium=tbl_medium.objects.get(id=medium))
            if not getfilter:
                errors.append("Please select valid medium,standard,section")
            else:
                getmorefilter=getfilter.filter(sections=tbl_class.objects.get(id=section))
                if not getmorefilter:
                    errors.append("Please select valid medium,standard,section")
            if errors:
                return render_to_response('editStudent.html',locals(),context_instance=RequestContext(req))
            if prestandard or premedium or prepassingyear or oldAddNo or oldRollNo:
                if not preschoolname:
                    errors.append("Please enter the school name!")
                    return render_to_response('editStudent.html',locals(),context_instance=RequestContext(req))
                 
            standobj=tbl_standard.objects.filter(medium=tbl_medium.objects.get(id=medium),name=tbl_shortstandard.objects.get(id=shortstandard).name)
            
            secobj=tbl_class.objects.get(id=section)
            getstud.siblings.all().delete()
            sib1obj=None
            if sib1id:
                matchPrefix=sib1id[0:len(STUDENTPREFIX)]
                matchPrefix=matchPrefix.upper()
                if matchPrefix!=STUDENTPREFIX:
                    sib1obj=None
                    errors.append("Please enter valid sibling1 id !")
                    return render_to_response('editStudent.html',locals(),context_instance=RequestContext(req))
                else:
                    try:
                        sib1obj=tbl_student.objects.get(id=int(sib1id[len(STUDENTPREFIX):]))
                    except:
                        sib1obj=None
                        errors.append("Please enter valid sibling1 id !")
                        return render_to_response('editStudent.html',locals(),context_instance=RequestContext(req))
            
            sib2id=req.POST.get('sib2id','').strip()
            sib2obj=None
            if sib2id:
                matchPrefix=sib2id[0:len(STUDENTPREFIX)]
                matchPrefix=matchPrefix.upper()
                if matchPrefix!=STUDENTPREFIX:
                    sib2obj=None
                    errors.append("Please enter valid sibling2 id !")
                    return render_to_response('editStudent.html',locals(),context_instance=RequestContext(req))
                else:
                    try:
                        sib2obj=tbl_student.objects.get(id=int(sib2id[len(STUDENTPREFIX):]))
                    except:
                        sib2obj=None
                        errors.append("Please enter valid sibling2 id !")
                        return render_to_response('editStudent.html',locals(),context_instance=RequestContext(req))
            sib3id=req.POST.get('sib3id','').strip()
            
            sib3obj=None
            if sib3id:
                matchPrefix=sib3id[0:len(STUDENTPREFIX)]
                matchPrefix=matchPrefix.upper()
                if matchPrefix!=STUDENTPREFIX:
                    sib3obj=None
                    errors.append("Please enter valid sibling3 id !")
                    return render_to_response('editStudent.html',locals(),context_instance=RequestContext(req))
                else:
                    try:
                        sib3obj=tbl_student.objects.get(id=int(sib3id[len(STUDENTPREFIX):]))
                    except:
                        sib3obj=None
                        errors.append("Please enter valid sibling3 id !")
                        return render_to_response('editStudent.html',locals(),context_instance=RequestContext(req))
            '''
            finally updating the database as per the changes
            '''
            
            if sib1obj:
                xx=tbl_sibling()
                xx.studentId=sib1obj.id
                xx.save()
                getstud.siblings.add(xx)
            if sib2obj:
                xx=tbl_sibling()
                xx.studentId=sib2obj.id
                xx.save()
                getstud.siblings.add(xx)
            if sib3obj:
                xx=tbl_sibling()
                xx.studentId=sib3obj.id
                xx.save()
                getstud.siblings.add(xx)
            
            
            
                
                     
            
            getstud.standard=standobj[0]
            getstud.section=secobj
            
            getstud.perDetail.fName=firstname
            getstud.perDetail.lName=lastname
            getstud.perDetail.age=age
            getstud.perDetail.sex=sex
            getstud.perDetail.dob=dob1
            if req.FILES.get('studImage'):
                
                imagePath=upload(req.FILES['studImage'],str(getstud.id))
                getstud.perDetail.image=imagePath
            getstud.perDetail.lAdd=laddress
            getstud.perDetail.lCity=tbl_location.objects.get(id=getlcity)
            if lpincode:
                
                getstud.perDetail.lpin=lpincode
            if lmobileno:    
                getstud.perDetail.lMobile=lmobileno
            if lcontact:
            
                getstud.perDetail.lLandline=lcontact
            getstud.perDetail.pAdd=paddress
            getstud.perDetail.pCity=tbl_location.objects.get(id=getpcity)
            if ppincode:
                getstud.perDetail.ppin=ppincode
            if pmobileno:
                getstud.perDetail.pMobile=pmobileno
            if pcontact:    
                getstud.perDetail.pLandline=pcontact
            
            
            getstud.perDetail.fatherName=fathername
            getstud.perDetail.fOccupation=fatheroccupation
            if fathersalary:
                getstud.perDetail.fSalary=fathersalary
            if fatherofficeno:    
                getstud.perDetail.fOfficeNo=fatherofficeno
            if fathermobileno:
                getstud.perDetail.fMobile=fathermobileno
            getstud.perDetail.motherName=mothername
            getstud.perDetail.mOccupation=motheroccupation
            if mothersalary:
                getstud.perDetail.mSalary=mothersalary
            if motherofficeno:    
                getstud.perDetail.mOfficeNo=motherofficeno
            if mothermobileno:    
                getstud.perDetail.mMobile=mothermobileno
            getstud.perDetail.personName=otherpersonname
            getstud.perDetail.relation=relation
            if otherpersonno:
                getstud.perDetail.contactNo=otherpersonno
            getstud.perDetail.save()
            if not getstud.eduDetail:
                if preschoolname:
                    p3=tbl_stdEducationalDetail()
                    p3.school=preschoolname
                    p3.standard=prestandard
                    p3.oldAdmission=oldAddNo
                    p3.rollNo=oldRollNo
                    if prepassingyear:
                        p3.pYear=prepassingyear
                    p3.medium=premedium
                    p3.save()
                    if req.FILES.get('documents',''):
                
                        imagePath1=upload1(req.FILES['documents'],'document'+str(p3.id),str(getstud.id))
                        new=tbl_doc()
                        new.name=new.id
                        new.belongTo='s'
                        new.file=imagePath1
                        new.save()
                        p3.docs.add(new)
                    if req.FILES.get('tc',''):
                
                        imagePath1=upload1(req.FILES['tc'],'tc'+str(p3.id),str(getstud.id))
                        new=tbl_doc()
                        new.name=new.id
                        new.belongTo='s'
                        new.file=imagePath1
                        new.save()
                        p3.docs.add(new)
                    if req.FILES.get('cc',''):
                
                        imagePath1=upload1(req.FILES['cc'],'cc'+str(p3.id),str(getstud.id))
                        new=tbl_doc()
                        new.name=new.id
                        new.belongTo='s'
                        new.file=imagePath1
                        new.save()
                        p3.docs.add(new)
                    if req.FILES.get('mc',''):
                
                        imagePath1=upload1(req.FILES['mc'],'mc'+str(p3.id),str(getstud.id))
                        new=tbl_doc()
                        new.name=new.id
                        new.belongTo='s'
                        new.file=imagePath1
                        new.save()
                        p3.docs.add(new)
                
                
                    
                
                    p3.save()
                else:
                    p3=None
                getstud.eduDetail=p3
            else:
                if not preschoolname:
                    getstud.eduDetail=None
                else:
                    getstud.eduDetail.school=preschoolname
                    getstud.eduDetail.standard=prestandard
                    if prepassingyear:
                        getstud.eduDetail.pYear=prepassingyear
                    getstud.eduDetail.medium=premedium
                    getstud.eduDetail.rollNo=oldRollNo
                    getstud.eduDetail.oldAdmission=oldAddNo
                    #getstud.eduDetail.docs=[]
                    if req.FILES.get('documents',''):
                
                        imagePath1=upload1(req.FILES['documents'],'document'+str(getstud.eduDetail.id),str(getstud.id))
                        new=tbl_doc()
                        new.name=new.id
                        new.belongTo='s'
                        new.file=imagePath1
                        new.save()
                        
                        getstud.eduDetail.docs.add(new)
                    if req.FILES.get('tc',''):
                
                        imagePath1=upload1(req.FILES['tc'],'tc'+str(getstud.eduDetail.id),str(getstud.id))
                        new=tbl_doc()
                        new.name=new.id
                        new.belongTo='s'
                        new.file=imagePath1
                        new.save()
                        
                        getstud.eduDetail.docs.add(new)
                    if req.FILES.get('cc',''):
                
                        imagePath1=upload1(req.FILES['cc'],'cc'+str(getstud.eduDetail.id),str(getstud.id))
                        new=tbl_doc()
                        new.name=new.id
                        new.belongTo='s'
                        new.file=imagePath1
                        new.save()
                        
                        getstud.eduDetail.docs.add(new)
                    if req.FILES.get('mc',''):
                
                        imagePath1=upload1(req.FILES['mc'],'mc'+str(getstud.eduDetail.id),str(getstud.id))
                        new=tbl_doc()
                        new.name=new.id
                        new.belongTo='s'
                        new.file=imagePath1
                        new.save()
                        
                        getstud.eduDetail.docs.add(new)
                    '''if req.FILES.get('documents',''):
                
                        imagePath1=upload1(req.FILES['documents'],str(getstud.eduDetail.id),str(getstud.id))
                        new=tbl_doc()
                        new.name=new.id
                        new.belongTo='s'
                        new.file=imagePath1
                        new.save()
                        getstud.eduDetail.docs=[]
                        getstud.eduDetail.docs.add(new)'''
                        
            getstud.createdOn=addate1
            
            getstud.save()
            
            
            getlog=getstud.history.filter(session1=schoolobj[0].getSession())
            #year=getlog['year__max']
            obj=tbl_MSS.objects.get(medium=getstud.standard.medium,standard=getstud.standard,section=getstud.section)
            if getlog:
            
                uniquemssobj=getlog[0].mss
            
                uniquemssobj.students.get(studentId=getstud.id).delete()
                uniquemssobj.save()
                
                getlog[0].mss=obj
                getlog[0].save()
            
                new=tbl_classStudent()
                new.studentId=getstud.id
                    
                new.save()
                obj.students.add(new)
                obj.save()
                getstud.save()
            else:
                newRow=tbl_studentLog()
                newRow.mss=obj
                newRow.session1=schoolobj[0].getSession()
                newRow.save()
                getstud.history.add(newRow)
                getstud.save()       
            return HttpResponseRedirect('/students/')
            
            
        return render_to_response('editStudent.html',locals(),context_instance=RequestContext(req))
def dateformatReverse(date): 
    '''
    used for date formats conversion
    '''
    date=datetime.datetime.strptime(date, '%Y-%m-%d')
    
    return date.strftime('%d-%m-%Y')

def v_accMresponder(req): 
    
    if req.GET.get('lstate',''): 
        '''
        this is used to get local city based on local state selected in form
        '''
        lcities=i_getAllStates(int(req.GET.get('lstate','')))
        template="\n\
        <div class='selectWidth1' id='citydiv1'>\
        <select class='small' name='lcity' id='lcity'>\n\
        <option value='-1'> ---- </option>\n"
        if lcities:
            for c in lcities:
                template=template+"<option value='"+str(c.id)+"'>"+c.name+"</option>\n"
        else:
            template=template+"<option value='-1'> NOT FOUND !</option>\n"
        template=template+"</select>\n\
        </div>"
        return HttpResponse(template)
    if req.GET.get('pstate',''):
        '''
        this is used to get permanent city based on permanent state
        '''
        pcities=i_getAllStates(int(req.GET.get('pstate','')))
        template="\n\
        <div class='selectWidth1' id='citydiv2'>\
        <select class='small' name='pcity' id='pcity'>\n\
        <option value='-1'> ---- </option>\n"
        if pcities:
            for c in pcities:
                template=template+"<option value='"+str(c.id)+"'>"+c.name+"</option>\n"
        else:
            template=template+"<option value='-1'> NOT FOUND !</option>\n"
        template=template+"</select>\n\
        </div>"
        return HttpResponse(template)
    
    if req.GET.get('studID1',''):
        '''
        this will help to access student information based on its ID
        '''    
          
        studentid=req.GET.get('studID1','')
        matchPrefix=studentid[0:len(STUDENTPREFIX)]
        matchPrefix=matchPrefix.upper()
        iD=studentid[len(STUDENTPREFIX):]
        
        
        if matchPrefix!=STUDENTPREFIX:
            template="<input type='text' name='sibname1'  value='' readonly style='width:150px'  />"
            
            return HttpResponse(template)
        
        try:
            iD=int(iD)
            stringname=tbl_student.objects.get(id=iD).getName()
        
            template="<input type='text' name='sibname1'  value='"+stringname+"' readonly style='width:150px'  />"
            
            return HttpResponse(template)
        except:
            
            template="<input type='text' name='sibname1'  value='' readonly style='width:150px'  />"
            
            return HttpResponse(template)
    if req.GET.get('studID2',''):
        '''
        this will help to access student information based on its ID
        '''
        
          
        studentid=req.GET.get('studID2','')
        matchPrefix=studentid[0:len(STUDENTPREFIX)]
        matchPrefix=matchPrefix.upper()
        iD=studentid[len(STUDENTPREFIX):]
        
        
        if matchPrefix!=STUDENTPREFIX:
            template="<input type='text' name='sibname2'  value='' readonly style='width:150px'  />"
            
            return HttpResponse(template)
        
        try:
            iD=int(iD)
            stringname=tbl_student.objects.get(id=iD).getName()
        
            template="<input type='text' name='sibname2'  value='"+stringname+"' readonly style='width:150px'  />"
            
            return HttpResponse(template)
        except:
            
            template="<input type='text' name='sibname2'  value='' readonly style='width:150px'  />"
            
            return HttpResponse(template)
    if req.GET.get('studID3',''):
        '''
        this will help to access student information based on its ID
        '''
        
          
        studentid=req.GET.get('studID3','')
        matchPrefix=studentid[0:len(STUDENTPREFIX)]
        matchPrefix=matchPrefix.upper()
        iD=studentid[len(STUDENTPREFIX):]
        
        
        if matchPrefix!=STUDENTPREFIX:
            template="<input type='text' name='sibname3'  value='' readonly style='width:150px'  />"
            
            return HttpResponse(template)
        
        try:
            iD=int(iD)
            stringname=tbl_student.objects.get(id=iD).getName()
        
            template="<input type='text' name='sibname3'  value='"+stringname+"' readonly style='width:150px'  />"
            
            return HttpResponse(template)
        except:
            
            template="<input type='text' name='sibname3'  value='' readonly style='width:150px'  />"
            
            return HttpResponse(template)
    if req.GET.get('getopt',''):
        getOpt=req.GET.get('getopt','')
        if getOpt=="1":
            months=['Jan','Feb','Mar','Apr','May','June','July','Aug','Sept','Oct','Nov','Dec']
            template="<div class='section'>\
            <label>Month<sup>*</sup> </label>\
            <div class='selectWidth1'><select name='month'>\
            <option value='-1'>Select</option>"
            i=1
            for data in months:
                template=template+"<option value='"+str(i)+"' >"
                template=template+data
                i=i+1
            template=template+"</select></div></div>"
            return HttpResponse(template)
        else:
            emps=tbl_employee.objects.filter(isActive=True)
            
            template="<div class='section'>\
            <label>Employee<sup>*</sup> </label>\
            <div class='selectWidth1'><select name='employee'>\
            <option value='-1'>Select</option>"
            
            for data in emps:
                template=template+"<option value='"+str(data.id)+"'>"
                template=template+data.getEMPName()
            template=template+"</select></div></div>"
            return HttpResponse(template)

def v_studPromote(req):
    '''
    this will help to promote the student from one class to another
    '''
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'student','u'):
        schoolobj=tbl_school.objects.filter()
        errors=[]
        if not schoolobj:
            errors.append("Please enter school setting in configuration")
            return render_to_response('promotestud.html',locals(),context_instance=RequestContext(req))
        classes=tbl_MSS.objects.filter(isActive=True)
        errors=[]
        if req.POST.get('savepromote',''):
            '''
            accessing form elements and performing validation 
            '''
            mss_id=int(req.POST.get('mss_id',''))
            
            if mss_id==-1:
                errors.append("Please select the class!")
                return render_to_response('promotestud.html',locals(),context_instance=RequestContext(req))
            uniquemss=tbl_MSS.objects.get(id=mss_id)
            
            allstud=tbl_student.objects.filter(standard=uniquemss.standard,section=uniquemss.section)
            temp=[]
            show=True
            for data in allstud:
                
                temp.append(data)
            mss_promoteid=int(req.POST.get('mss_promoteid',''))
            
            
            if mss_promoteid==-1:
                
                errors.append("Operation cannot be performed!")
                mss_id=-1
                return render_to_response('promotestud.html',locals(),context_instance=RequestContext(req))
            
            for data in temp:
                
                values=req.POST.get(data.getSTUDid(),'')
                if values=='1':
                    '''
                    this will promote students to other class(whose id equal to promote mss)
                    '''
                    
                    promotemss=tbl_MSS.objects.get(id=mss_promoteid)
                    if data.history.filter(session1=schoolobj[0].getSession()):
                        obj=data.history.filter(session1=schoolobj[0].getSession())[0]
                        obj.mss=promotemss
                        obj.rollNo=None
                        obj.save()
                    else:    
                        studlog=tbl_studentLog()
                    
                        studlog.mss=promotemss
                        studlog.session=schoolobj[0].getSession()
                        studlog.save()
                        data.history.add(studlog)
                        data.save()
                    
                    
                    olddata=uniquemss.students.get(studentId=data.id)
                    olddata.delete()
                    uniquemss.save()
                    csobj=tbl_classStudent()
                    csobj.studentId=data.id
                    
                    csobj.save()
                    promotemss.students.add(csobj)
                    
                    promotemss.save()
                    data.standard=promotemss.standard
                    data.section=promotemss.section
                    data.save()
                    
                    
                else:
                    '''
                    this will not promote student to next class
                    '''
                    if data.history.filter(session1=schoolobj[0].getSession()):
                        obj=data.history.filter(session1=schoolobj[0].getSession())[0]
                        obj.mss=uniquemss
                        
                        obj.save()
                    else:
                        hisrow=tbl_studentLog()
                        hisrow.rollNo=None
                        hisrow.mss=uniquemss
                        getstudent=uniquemss.students.get(studentId=data.id)
                        getstudent.rollNo=None
                        getstudent.save()
                        hisrow.session1=schoolobj[0].getSession()
                        hisrow.save()
                        data.history.add(hisrow)
                        data.save()
            
            errors.append("Successfully promoted")
            promote_mss=-1
            mss_id=-1            
            return render_to_response('promotestud.html',locals(),context_instance=RequestContext(req))
        return render_to_response('promotestud.html',locals(),context_instance=RequestContext(req))
def getdatatopromote(req):
    '''
    this will help to access all the students present in selected MSS and arranging it in required format
    '''
    classes=tbl_MSS.objects.filter(isActive=True)
    
    if req.GET.get('getStudents',''):
        
        mss_id=int(req.GET.get('getStudents',''))
        
        if mss_id==-1:
            
            
            return HttpResponse('<script>alert("No Data found ");</script>')
        else:
            uniquemss=tbl_MSS.objects.get(id=mss_id)
            
            allstud=tbl_student.objects.filter(isActive=True,standard=uniquemss.standard,section=uniquemss.section)
            temp=[]
            for data in allstud:
                
                temp.append(data)
            
            template='<table class="table table-bordered table-striped"   width="100%">\n\
            <thead align="center"  class="tr_bg_list">\n\
            <tr><td>STUDENT ID</td><td>STUDENT NAME</td><td>Promote</td></tr>\n\
            </thead><tbody align="center" class="font_wght">'
            if temp:
                for item in temp:
                    template=template+'<tr><td>'+item.getSTUDid()+'</td>\n\
                    <td>'+item.getName()+'</td>\n\
                    <td><input type="checkbox" value="1" name="'+item.getSTUDid()+'"> </td>\n\
                    </tr>'
            else:
                template=template+'<tr><td colspan="3">No student found</td></tr>'
                    
            template=template+'</tbody></table>'
            if temp:
                template=template+'<div class="section">\n\
                <label>PROMOTE TO<sup>*</sup></label>\n\
                <div class="selectWidth1" >\n\
                <select class="small"  name="mss_promoteid" >\n\
                <option value="-1"  selected>Select Class</option>'
                for c in classes:
                    template=template+'<option value="'+str(c.id)+'">'+c.getName()+'</option>'
                template=template+'</select>\n\
                </div></div><div class="section last"><div>\n\
                <input type="submit" name="savepromote" value="PROMOTE" class="btn submit_form"></input>\n\
                </div></div>'                

        
            return HttpResponse(template)
    
def sortstudent(uniquemss):
    
    allobjects=uniquemss.students.all()
    
    length=len(uniquemss.students.all())
    i=1
    
    for data in allobjects:
        data.rollNo=i
        data.save()
        i=i+1
    i=1
    for data in allobjects:
        for v in allobjects[i:]:
            
            if data.getname()>v.getname():
                
                if data.rollNo<v.rollNo:
                    temp=data.rollNo
                    data.rollNo=v.rollNo
                    v.rollNo=temp
                    data.save()
                    v.save()
                
                    
            else:
            
                
                if data.rollNo>v.rollNo:
                
                    temp=data.rollNo
                    data.rollNo=v.rollNo
                    v.rollNo=temp
                    data.save()
                    v.save()
        i=i+1



def v_studHistory(req):
    '''
    this function is written to carry out listing of students
    '''
    
    x=STUDENTPREFIX
   
    rows=tbl_student.objects.filter()
    pagination_parameter=manavPageParameter    #Used for next and previous (i.e pagination)
    
    NEXT=False
    totalRows=len(rows)
    TO=len(rows)
    if len(rows)>pagination_parameter:
        TO=pagination_parameter
        NEXT=True
    FROM=1
    rows=rows[:pagination_parameter]
    return render_to_response('studentHistory.html',locals(),context_instance=RequestContext(req))
    

def v_nextstudHistory(req,para):
    '''
    used to find next list of students having rows equal to manavPageParameter
    '''
    para=int(para)
    FROM=para+1
    pagination_parameter=manavPageParameter
    
    pagination_parameter=pagination_parameter+para
    
    rows=tbl_student.objects.filter()
    totalRows=len(rows)
    NEXT=False
    TO=len(rows)
    if len(rows)>pagination_parameter:
        TO=pagination_parameter
        NEXT=True
    rows=rows[para:pagination_parameter]
    PREV="True"
    back=para
    
    return render_to_response('studentHistory.html',locals(),context_instance=RequestContext(req))

def v_prevstudHistory(req,para):
    '''
    used to find previous list of students having rows equal to manavPageParameter
    '''
    para=int(para)
    TO=para
    pagination_parameter=manavPageParameter
    back=para-pagination_parameter
    
    rows=tbl_student.objects.filter()
    totalRows=len(rows)
    NEXT=False
    FROM=back+1
    if len(rows)>back:
        NEXT=True
    rows=rows[back:para]
    if back==0:
        PREV=False
    else:
        PREV=True
    
    return render_to_response('studentHistory.html',locals(),context_instance=RequestContext(req))
def v_viewstudRecord(req,para):
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'student','v'):
        '''
        shows student history i.e. his class,roll,etc
        '''
        para=int(para)
        uniquestudent=tbl_student.objects.get(id=para)
        getdata=uniquestudent.history.all().order_by('session1')
        return render_to_response('viewstudrecord.html',locals(),context_instance=RequestContext(req))
def v_studRecordYearWise(req,para,para1):
    '''
    used to access the record of student whose id is para1 for the session para
    '''
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'student','v'):
        errors=[]
        exams=tbl_examType.objects.filter()
        getsession=para
        studid=int(para1)
        '''
        accessing personal details
        '''
        getstud=tbl_student.objects.get(id=studid)
        mediums=tbl_medium.objects.all()
        shortstandards=tbl_shortstandard.objects.all()
        sections=tbl_class.objects.all()
        states=tbl_location.objects.filter(pid=1).order_by('name')
        
        addate=getstud.createdOn
        addate=dateformatReverse(str(addate))
        firstname=getstud.perDetail.fName
        lastname=getstud.perDetail.lName
        dob=dateformatReverse(str(getstud.perDetail.dob))
        age=getstud.perDetail.age
        sex=getstud.perDetail.sex
            #mssid=getstud.history.filter(session1=getstud)[0].mss
        mssid=tbl_MSS.objects.get(standard=getstud.standard,medium=getstud.standard.medium,section=getstud.section)
        medium=mssid.medium.id
        shortstandard=tbl_shortstandard.objects.filter(name=mssid.standard.name)[0].id
        section=mssid.section.id
            
        laddress=getstud.perDetail.lAdd
        getlcity=getstud.perDetail.lCity.id
        getlstate=getstud.perDetail.lCity.pid
        lcities=tbl_location.objects.filter(pid=getlstate).order_by('name')
        if getstud.perDetail.lpin:
            lpincode=getstud.perDetail.lpin
            
        if getstud.perDetail.lMobile:
            lmobileno=getstud.perDetail.lMobile
        if getstud.perDetail.lLandline:
            lcontact=getstud.perDetail.lLandline
        paddress=getstud.perDetail.pAdd
        getpcity=getstud.perDetail.pCity.id
        getpstate=getstud.perDetail.pCity.pid
        pcities=tbl_location.objects.filter(pid=getpstate).order_by('name')
        if getstud.perDetail.ppin:
            ppincode=getstud.perDetail.ppin
        if getstud.perDetail.pLandline:
            pcontact=getstud.perDetail.pLandline
        if getstud.perDetail.pMobile:
            pmobileno=getstud.perDetail.pMobile
        '''
        accessing fee details 
        '''
        feeDetails=tbl_feePayment.objects.filter(session1=getsession,studid=getstud)
        selected_session=para
        history=getstud.history.filter(session1=para)
        if history:
            mss_id=history[0].mss.id
            
        classStudent_id=para1
        try:
            mssObj=tbl_MSS.objects.get(id=mss_id)
        except:
            pass
            
        
        
        getsub=tbl_subject.objects.filter(standards=mssObj.standard)
            
        
        uniquestud=tbl_student.objects.get(id=para1)
        studname=uniquestud.getName()
            
        data=tbl_subjectMarks.objects.filter(mssId=mssObj.id,hasSession=selected_session)
                    
        '''
        accessing student marks and arranging in required format
        '''
            
        overall=[]
        newoverall=[]
        temp=[]
        existing=[]
        for sub in getsub:
                #overall=[]
            temp=[]
            temp.append(sub.name)
                
                
            for e in exams:
                    
                if data.filter(subject=sub.name,testName=e):
                        
                    ii=data.filter(subject=sub.name,testName=e)[0]
                    marks=eval(ii.marks)
                    details=eval(ii.detail)
                    if marks[int(uniquestud.id)]==-1:
                        temp.append('ab')
                    else:
                        temp.append(marks[uniquestud.id])
                    temp.append(details['max'])
                    if marks[uniquestud.id]==-1:
                        temp.append(int(0)*100/(details['max']))
                    else:
                        temp.append(str(int(marks[uniquestud.id])*100/(details['max']))+'%')
                        #overall.append(temp)
                        #temp=[]
                else:
                    temp.append('NA')
                    temp.append('NA')
                    temp.append('NA')
                        #overall.append(temp)
                        #temp=[]
            overall.append(temp) 
                #newoverall.append(overall)
            #return HttpResponse(existing)
            if len(data)<1:
                errors.append("No data exist!")
                return render_to_response('studyearlydata.html',locals(),context_instance=RequestContext(req))
            performance=[]
            for ff in exams:
                evaluation=[]
                total=0
                obtain=0
                for sub in getsub:
                    for item in data.filter(subject=sub.name,testName=ff):
                        if sub.name==item.subject:
                            marks=eval(item.marks)
                            details=eval(item.detail)
                            total=total+details['max']
                            if marks[uniquestud.id]==-1:
                                obtain=obtain+0
                            else:
                                obtain=obtain+marks[uniquestud.id]
                    
                evaluation.append(obtain)
                evaluation.append(total)
                try:
                    evaluation.append((obtain*100)/total)
                except:
                    evaluation.append('0')
                performance.append(evaluation)
                          

        
        return render_to_response('studyearlydata.html',locals(),context_instance=RequestContext(req))
    
       
        
 

def v_assignRollNo(req):
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'teacher','v'):
        '''
        this will help to assign roll no to student of selected MSS i.e class
        '''
        schoolobj=tbl_school.objects.filter()
        getsession=schoolobj[0].getSession()
        #return HttpResponse(getsession)
        errors=[]
        allMSS=tbl_MSS.objects.filter(isActive=True)
        if req.POST.get('assignRollNo',''):
            getmss=int(req.POST.get('getMSS',''))
            orderby=req.POST.get('orderby','')
            
            if getmss==-1:
                errors.append("Please select the class!")
                return render_to_response('assignRollNo.html',locals(),context_instance=RequestContext(req))
            try:
                cuser=tbl_systemUser.objects.get(username=req.session.get('username'))
                if not cuser.isAdmin:
                    empObj=tbl_employee.objects.get(user=cuser)
                    teacherObj=empObj.ifTeacher
                    if not teacherObj==tbl_MSS.objects.get(id=getmss).classTeacher:
                        
                        errors.append("You don't have permission to assign roll no !")
                        return render_to_response('assignRollNo.html',locals(),context_instance=RequestContext(req))
            except:
                pass
            
            
            
            if not orderby:
                errors.append("Please select the order by!")
                return render_to_response('assignRollNo.html',locals(),context_instance=RequestContext(req))
            mssobj=tbl_MSS.objects.get(id=getmss)
            allstudents=mssobj.students.all()
            if orderby=="1":
                '''
                this will assign roll no in sorted order (by student name)
                '''
                rollList=[d.rollNo for d in allstudents]
                maxStudRollNo=max(rollList)
                getstudents=allstudents.filter(rollNo=None)
                
                if maxStudRollNo==None:
                    
                    i=1
                    for stud in getstudents:
                        stud.rollNo=str(i)
                        stud.save()
                        i=i+1
                    i=1
                    for data in getstudents:
                        for v in getstudents[i:]:
                
                            if data.getname()>v.getname():
                    
                                if int(data.rollNo)<int(v.rollNo):
                                    temp=data.rollNo
                                    data.rollNo=v.rollNo
                                    v.rollNo=temp
                                    data.save()
                                    v.save()
                    
                        
                            else:
                                if int(data.rollNo)>int(v.rollNo):
                    
                                    temp=data.rollNo
                                    data.rollNo=v.rollNo
                                    v.rollNo=temp
                                    data.save()
                                    v.save()
                        i=i+1
                else:
                    
                    maxStudRollNo=int(maxStudRollNo)
                    i=maxStudRollNo+1
                    for stud in getstudents:
                        
                        stud.rollNo=str(i)
                        i=i+1
                        stud.save()
                    i=1
                    for data in getstudents:
                        for v in getstudents[i:]:
                
                            if data.getname()>v.getname():
                    
                                if int(data.rollNo)<int(v.rollNo):
                                    temp=data.rollNo
                                    data.rollNo=v.rollNo
                                    v.rollNo=temp
                                    data.save()
                                    v.save()
                    
                        
                            else:
                                if int(data.rollNo)>int(v.rollNo):
                    
                                    temp=data.rollNo
                                    data.rollNo=v.rollNo
                                    v.rollNo=temp
                                    data.save()
                                    v.save()
                        i=i+1
                for data in getstudents:
                    
                    getunique=tbl_student.objects.get(id=data.studentId)
                    studhistory=getunique.history.filter(session1=getsession)
                    if studhistory:
                        studhistory[0].rollNo=data.rollNo
                        studhistory[0].save()
                    else:
                        newRow=tbl_studentLog()
                        newRow.rollNo=data.rollNo
                        newRow.session1=getsession
                        newRow.mss=mssobj
                        newRow.save()
                        getunique.history.add(newRow)
                        getunique.save()
    
            if orderby=="2":
                '''
                this will assign roll no ordr by its id
                '''
                
                rollList=[d.rollNo for d in allstudents]
                maxStudRollNo=max(rollList)
                getstudents=allstudents.filter(rollNo=None)
                if maxStudRollNo==None:
                    
                    i=1
                    for stud in getstudents:
                        stud.rollNo=str(i)
                        stud.save()
                        i=i+1
                    i=1
                    for data in getstudents:
                        for v in getstudents[i:]:
                
                            if data.studentId()>v.studentId():
                    
                                if int(data.rollNo)<int(v.rollNo):
                                    temp=data.rollNo
                                    data.rollNo=v.rollNo
                                    v.rollNo=temp
                                    data.save()
                                    v.save()
                    
                        
                            else:
                                if int(data.rollNo)>int(v.rollNo):
                    
                                    temp=data.rollNo
                                    data.rollNo=v.rollNo
                                    v.rollNo=temp
                                    data.save()
                                    v.save()
                        i=i+1
                else:
                    
                    maxStudRollNo=int(maxStudRollNo)
                    i=maxStudRollNo+1
                    for stud in getstudents:
                        
                        stud.rollNo=str(i)
                        i=i+1
                        stud.save()
                    i=1
                    for data in getstudents:
                        for v in getstudents[i:]:
                
                            if data.studentId>data.studentId:
                    
                                if int(data.rollNo)<int(v.rollNo):
                                    temp=data.rollNo
                                    data.rollNo=v.rollNo
                                    v.rollNo=temp
                                    data.save()
                                    v.save()
                    
                        
                            else:
                                if int(data.rollNo)>int(v.rollNo):
                    
                                    temp=data.rollNo
                                    data.rollNo=v.rollNo
                                    v.rollNo=temp
                                    data.save()
                                    v.save()
                        i=i+1
                for data in getstudents:
                    
                    getunique=tbl_student.objects.get(id=data.studentId)
                    studhistory=getunique.history.filter(session1=getsession)
                    if studhistory:
                        studhistory[0].rollNo=data.rollNo
                        studhistory[0].save()
                    else:
                        newRow=tbl_studentLog()
                        newRow.rollNo=data.rollNo
                        newRow.session1=getsession
                        newRow.mss=mssobj
                        newRow.save()
                        getunique.history.add(newRow)
                        getunique.save()
                
            return HttpResponse("<script>alert('roll no is successfully assigned to students');location.href='/assignRollNo/';</script>")                    
        return render_to_response('assignRollNo.html',locals(),context_instance=RequestContext(req))
def v_Notice(req):
    '''
    this is used to add new Notice
    '''
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'notice','a'):
        allRows=Notice.objects.filter(isActive=True).order_by('date')
        if req.POST.get('addNotice',''):
            errors=[]
            adddate=req.POST.get('adddate','').strip()
            message=req.POST.get('message','').strip()
            try:
                adddate1=dateformatConvertor(adddate)
            except:
                errors.append("Please enter valid date")
            if not message:
                errors.append("Please enter valid message")
            if errors:
                return render_to_response('addNotice.html',locals(),context_instance=RequestContext(req))
            else:
                newRow=Notice()
                newRow.date=adddate1
                newRow.message=message
                newRow.save()
            return HttpResponseRedirect('/')
        if req.POST.get('editNotice',''):
            for data in allRows:
                if req.POST.get(str(data.id),''):
                    data.isActive=False
                    data.save()
            return HttpResponseRedirect('/')
             
        return render_to_response('addNotice.html',locals(),context_instance=RequestContext(req))
def v_user_detail(req):
    '''
    this will help to change system user information such as password,etc
    '''
    user=tbl_systemUser.objects.get(username=req.session.get('username'))
    
    
    username=user.username
    
    
    
    
    pwd=user.password
    cpwd=user.password
        
    try:  
        imagePath=user.image.url
    except:
        imagePath=''
    if req.POST.get('editUser',''):
        '''
        accessing form elements and validating them
        '''
        errors=[]
        username=req.POST.get('username','').strip()
        pwd=req.POST.get('pwd','').strip()
        cpwd=req.POST.get('cpwd','').strip()
        
        
        
        
            
            #----------------------------------    
        
        if len(pwd)==0:
            errors.append("please enter a password !")
        elif not 5 <= len(pwd) <= 15:
            errors.append("password length should be between 5-15 characters !")
        elif user.password!=pwd and not pwd==cpwd:
            errors.append("both password fields must be match !")
        
        
        
        else:
                
            
            if req.FILES.get('image'):
                imagePath=i_upload(req.FILES['image'],userUDir,username+'.jpeg')
            
        '''
        finally updating database with latest values
        '''
        if not errors:
           
            user.password=pwd
            
            
            user.image=imagePath
            user.save()
            return HttpResponseRedirect('/')
        return render_to_response('editUserAccount.html',locals(),context_instance=RequestContext(req))     
    

    return render_to_response('editUserAccount.html',locals(),context_instance=RequestContext(req))
    