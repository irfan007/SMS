from django.shortcuts import render_to_response
from django.template.context import RequestContext
from App.models import   tbl_employee, tbl_teacher, tbl_location,\
    tbl_teaEducationalDetail, tbl_experienceDetail, tbl_empPersonalDetail,\
    tbl_doc , tbl_MSS, tbl_subjectAndTeacher, tbl_subject, tbl_systemUser,\
    tbl_role, tbl_examType, tbl_classStudent, tbl_student,\
    tbl_subjectMarks, tbl_school
from SMS.settings import TEACHER_PREFIX, EMPLOYEE_PREFIX, teacherUDir,\
    uploadFolder
from django.http import  HttpResponseRedirect
from App.pp import i_upload
from datetime import datetime
from django.utils.dateformat import DateFormat
from views.permission import i_hasPermission


def v_studPerformance(req):
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'teacher','v'):
        allSession=tbl_subjectMarks.objects.values_list('hasSession').distinct()
        classes=tbl_MSS.objects.filter(isActive=True)
        exams=tbl_examType.objects.filter()
        if not allSession:
            errors=['No data to compute performance, please upload marks first !']
            return render_to_response('studentperf.html',locals(),context_instance=RequestContext(req))
        if req.POST.get('result',''):
            
            errors=[]
            selected_session=req.POST.get('selected_session','-1')
            if selected_session=='-1':
                errors.append("Please select session !")
                return render_to_response('studentperf.html',locals(),context_instance=RequestContext(req))
            
            mss_id=int(req.POST.get('mss_id',-1))
            classStudent_id=int(req.POST.get('classStudent_id',-1))
            try:
                mssObj=tbl_MSS.objects.get(id=mss_id)
            except:
                errors.append("Please select the class")
                return render_to_response('studentperf.html',locals(),context_instance=RequestContext(req))
            students=mssObj.students.all()
        
            getsub=tbl_subject.objects.filter(standards=mssObj.standard)
            
            try:
                getstud=tbl_classStudent.objects.get(id=classStudent_id)
            except:
                errors.append("Please select student id !")
            if errors:
                return render_to_response('studentperf.html',locals(),context_instance=RequestContext(req))
            uniquestud=tbl_student.objects.get(id=getstud.studentId)
            studname=getstud.getname()
            
            data=tbl_subjectMarks.objects.filter(mssId=mssObj.id,hasSession=selected_session)
            
            '''getename=data.values('testName').distinct()
            for data in getename:
                exams.append(data['testName'])'''
            
            #tbl_subjectMarks.objects
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
                return render_to_response('studentperf.html',locals(),context_instance=RequestContext(req))
            performance=[]
            
            for ff in exams:
                evaluation=[]
                total=0
                obtain=0
                for sub in getsub:
                    for item in data.filter(subject=sub.name,testName=ff):
                        if sub.name.lower()==item.subject.lower():
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
                #return HttpResponse(str(evaluation))          
            
                    
            
            
            return render_to_response('studentperf.html',locals(),context_instance=RequestContext(req))
        return render_to_response('studentperf.html',locals(),context_instance=RequestContext(req))


def isUser(usrname):
    try:
        if tbl_systemUser.objects.get(username=usrname):
            return True
    except:
        return False


def v_viewMarksList(req,sAtid):
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'teacher','v'):
        
        subjectMarks=tbl_subjectAndTeacher.objects.get(id=sAtid).subjectResults.all()
        subject=tbl_subjectAndTeacher.objects.get(id=sAtid).subject
        return render_to_response('subjectMarksList.html',locals(),context_instance=RequestContext(req))
    

def v_viewMarks_p1(req):
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'teacher','v'):
#        inputSession=tbl_school.objects.all()[0].getSession()
#        session_start=inputSession.split('-')[0]
#        session_end=inputSession.split('-')[1]
        classes=tbl_MSS.objects.filter(isActive=True)
        subjects=None
        if req.POST.get('viewMarks_p1',''):
            errors=[]
            mss_id=int(req.POST.get('mss_id'))
            subject_id=int(req.POST.get('subject_id'))
            try:
                subjects=tbl_subject.objects.filter(standards=tbl_MSS.objects.get(id=int(req.POST.get('mss_id',''))).standard)
            except:
                pass
            
            if mss_id==-1:
                errors.append("please select one class !")
            elif subject_id==-1:
                errors.append("please select one subject !")
            else:
                try:
                    tbl_subjectAndTeacher.objects.get(mssId=mss_id,subject=tbl_subject.objects.get(id=subject_id).name)
                except:
                    errors.append("Teacher for Subject for this class is not assigned, please assign first !")
            
            if not errors:
                sAtObj=tbl_subjectAndTeacher.objects.get(mssId=mss_id,subject=tbl_subject.objects.get(id=subject_id).name) 
                if sAtObj.subjectResults.all():
                    return HttpResponseRedirect('/teacher/view/marks/'+str(sAtObj.id))
                else:
                    errors.append("marks not uploded !")
            return render_to_response('viewMarks_p1.html',locals(),context_instance=RequestContext(req))
        return render_to_response('viewMarks_p1.html',locals(),context_instance=RequestContext(req))



def v_uploadMarks_p1(req):
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'teacher','v'):
        
        classes=tbl_MSS.objects.filter(isActive=True)
        subjects=None
        if req.POST.get('uploadMarks_p1',''):
            errors=[]
            mss_id=int(req.POST.get('mss_id'))
            subject_id=int(req.POST.get('subject_id'))
            try:
                subjects=tbl_subject.objects.filter(standards=tbl_MSS.objects.get(id=int(req.POST.get('mss_id',''))).standard)
            except:
                pass
            
            if mss_id==-1:
                errors.append("please select one class !")
            elif subject_id==-1:
                errors.append("please select one subject !")
            else:
                try:
                    tbl_subjectAndTeacher.objects.get(mssId=mss_id,subject=tbl_subject.objects.get(id=subject_id).name)
                except:
                    errors.append("Teacher for Subject for this class is not assigned, please assign first !")
                
                
                try:
                    cuser=tbl_systemUser.objects.get(username=req.session.get('username'))
                    if not cuser.isAdmin:
                        empObj=tbl_employee.objects.get(user=cuser)
                        teacherObj=empObj.ifTeacher
                        if not teacherObj==tbl_MSS.objects.get(id=mss_id).classTeacher:
                            if not tbl_subjectAndTeacher.objects.get(mssId=mss_id,subject=tbl_subject.objects.get(id=subject_id).name,tid=teacherObj.id):
                                errors.append("You don't have permission to upload a marks for class !")
                except:
                    pass
            if not errors:
                sAtObj=tbl_subjectAndTeacher.objects.get(mssId=mss_id,subject=tbl_subject.objects.get(id=subject_id).name)
                cmss=tbl_MSS.objects.get(id=sAtObj.mssId)
                if not tbl_school.objects.all():
                    errors.append("Please specify session in ( configuration > setting ) first !")
                elif not cmss.students.all():
                    errors.append("Please add students in class first !")
                elif cmss.students.all()[0].rollNo==None:
                    errors.append("Please assign students roll No. of class first !")
                else:
                    return HttpResponseRedirect('/add/marks/'+str(sAtObj.id))
            return render_to_response('uploadMarks_p1.html',locals(),context_instance=RequestContext(req))
        return render_to_response('uploadMarks_p1.html',locals(),context_instance=RequestContext(req))
    



def v_teacher(req):
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'teacher','v'):
        tPrefix=TEACHER_PREFIX
        ePrefix=EMPLOYEE_PREFIX
        employees=tbl_employee.objects.filter(desig='teacher').order_by('ifTeacher__id')
        return render_to_response('teacherList.html',locals(),context_instance=RequestContext(req))

def v_addTeacher(req):
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'teacher','a'):
        empPrefix=EMPLOYEE_PREFIX
        tPrefix=TEACHER_PREFIX
        empid=(tbl_employee.objects.count()+1)
        tid=(tbl_teacher.objects.count()+1)
        states=tbl_location.objects.filter(pid=1).order_by('name')
        states2=states
        
        
        if req.POST.get('addTeacher',''):
            errors=[]
            eduDetails=[]
            expDetails=[]
            
            title=req.POST.get('title','')
            fname=req.POST.get('fname','').strip()
            lname=req.POST.get('lname','').strip()
            dob=req.POST.get('dob',None).strip()
            age=req.POST.get('age','').strip()
            email=req.POST.get('email','').strip()
            joindate=req.POST.get('joindate',None).strip()
            totalExp=req.POST.get('totalExp','').strip()
            
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
            qual_1=req.POST.get('qual_1')
            percent_1=req.POST.get('percent_1')
            pyear_1=req.POST.get('pyear_1')
            institute_1=req.POST.get('institute_1')
            city_1=req.POST.get('city_1')
            
            
            qual_2=req.POST.get('qual_2')
            percent_2=req.POST.get('percent_2')
            pyear_2=req.POST.get('pyear_2')
            institute_2=req.POST.get('institute_2')
            city_2=req.POST.get('city_2')
            
            
            qual_3=req.POST.get('qual_3')
            percent_3=req.POST.get('percent_3')
            pyear_3=req.POST.get('pyear_3')
            institute_3=req.POST.get('institute_3')
            city_3=req.POST.get('city_3')
            
            
            qual_4=req.POST.get('qual_4')
            percent_4=req.POST.get('percent_4')
            pyear_4=req.POST.get('pyear_4')
            institute_4=req.POST.get('institute_4')
            city_4=req.POST.get('city_4')
            
            
            qual_5=req.POST.get('qual_5')
            percent_5=req.POST.get('percent_5')
            pyear_5=req.POST.get('pyear_5')
            institute_5=req.POST.get('institute_5')
            city_5=req.POST.get('city_5')
            
            
            qual_6=req.POST.get('qual_6')
            percent_6=req.POST.get('percent_6')
            pyear_6=req.POST.get('pyear_6')
            institute_6=req.POST.get('institute_6')
            city_6=req.POST.get('city_6')
            
            
            qual_7=req.POST.get('qual_7')
            percent_7=req.POST.get('percent_7')
            pyear_7=req.POST.get('pyear_7')
            institute_7=req.POST.get('institute_7')
            city_7=req.POST.get('city_7')
            
            
            
            ex_standard_1=req.POST.get('ex_standard_1')
            ex_subject_1=req.POST.get('ex_subject_1')
            ex_institute_1=req.POST.get('ex_institute_1')
            ex_city_1=req.POST.get('ex_city_1')
            ex_from_1=req.POST.get('ex_from_1')
            ex_to_1=req.POST.get('ex_to_1')
            ex_doc_1=req.POST.get('ex_doc_1')
            
            ex_standard_2=req.POST.get('ex_standard_2')
            ex_subject_2=req.POST.get('ex_subject_2')
            ex_institute_2=req.POST.get('ex_institute_2')
            ex_city_2=req.POST.get('ex_city_2')
            ex_from_2=req.POST.get('ex_from_2')
            ex_to_2=req.POST.get('ex_to_2')
            ex_doc_2=req.POST.get('ex_doc_2')
            
            ex_standard_3=req.POST.get('ex_standard_3')
            ex_subject_3=req.POST.get('ex_subject_3')
            ex_institute_3=req.POST.get('ex_institute_3')
            ex_city_3=req.POST.get('ex_city_3')
            ex_from_3=req.POST.get('ex_from_3')
            ex_to_3=req.POST.get('ex_to_3')
            ex_doc_3=req.POST.get('ex_doc_3')      
            
            
            
            username=req.POST.get('username','').strip()
            pwd=req.POST.get('pwd','').strip()
            cpwd=req.POST.get('cpwd','').strip()
            active=req.POST.get('active',False)
           
            if title=='-1':
                errors.append("please select at least one title !")
            elif not fname:
                errors.append("please enter first name !")
            elif not lname:
                errors.append("please enter last name !")
            elif not email:
                errors.append("please enter email Id !")
            elif '@' and '.' not in email:
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
            elif len(username)==0:
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
            
            else:
                if dob:
                    try:
                        datetime.strptime(dob,'%d-%m-%Y')
                    except:
                        errors.append("please enter valid date of birth !")
                
                
                    
                if joindate:        
                    try:
                        datetime.strptime(joindate,'%d-%m-%Y')
                    except:
                        errors.append("please enter valid joining date !")
                
                which={1:'1st Master',2:'2nd Master',3:'1st Bachelor',4:'2nd Bachelor',5:'12th',6:'10th',7:'diploma'}
                for x in range(1,8):
                    field=['qual_','percent_','pyear_','institute_','city_']
                
                    checkIt=False
                    for item in field:
                        if req.POST.get(item+str(x)):
                            checkIt=True
                        if req.FILES.get('doc_'+str(x)):
                            checkIt=True
                            
                    if checkIt and not req.POST.get('qual_'+str(x)):
                        errors.append('please enter qualification of '+which[x]+' Details !')
                    if checkIt and not req.POST.get('percent_'+str(x)):
                        errors.append('please enter percent of '+which[x]+' Details !')
                    if checkIt and not req.POST.get('pyear_'+str(x)):
                        errors.append('please enter passed out year of '+which[x]+' Details !')
                    if checkIt and not req.POST.get('institute_'+str(x)):
                        errors.append('please enter institute of '+which[x]+' Details !')
                    if checkIt and not req.POST.get('city_'+str(x)):
                        errors.append('please enter city of '+which[x]+' Details !')
                    if checkIt and not req.FILES.get('doc_'+str(x)):
                        errors.append('please attach doc of '+which[x]+' Details !')
                    if not errors and checkIt:
                        eduDetails.append((x,tbl_teaEducationalDetail(type=x,qualification=req.POST.get('qual_'+str(x)).strip(),percentage=int(req.POST.get('percent_'+str(x)).strip()),pYear=int(req.POST.get('pyear_'+str(x)).strip()),institute=req.POST.get('institute_'+str(x)).strip(),city=req.POST.get('city_'+str(x)).strip())))
                
                if not errors:
                    which={1:'1st',2:'2nd',3:'3rd'}
                    for x in range(1,4):
                        field=['ex_standard_','ex_subject_','ex_institute_','ex_city_','ex_from_','ex_to_']
                        checkIt=False
                        for item in field:
                            if req.POST.get(item+str(x)):
                                checkIt=True
                            if req.FILES.get('ex_doc_'+str(x)):
                                checkIt=True
                        
                        if checkIt and not req.POST.get('ex_standard_'+str(x)):
                            errors.append('please enter standard of '+which[x]+' experience !')
                        if checkIt and not req.POST.get('ex_subject_'+str(x)):
                            errors.append('please enter subject of '+which[x]+' experience !')
                        if checkIt and not req.POST.get('ex_institute_'+str(x)):
                            errors.append('please enter institute of '+which[x]+' experience !')
                        if checkIt and not req.POST.get('ex_city_'+str(x)):
                            errors.append('please enter city of '+which[x]+' experience !')
                        if checkIt and not req.POST.get('ex_from_'+str(x)):
                            errors.append("please enter 'from' field of "+which[x]+" experience !")
                        if checkIt and not req.POST.get('ex_to_'+str(x)):
                            errors.append("please enter 'to' field of "+which[x]+" experience !")
                        if checkIt and not req.FILES.get('ex_doc_'+str(x)):
                            errors.append('please attach certificate of '+which[x]+' experience !')
                        if checkIt and req.POST.get('ex_from_'+str(x)):
                            try:
                                datetime.strptime(req.POST.get('ex_from_'+str(x)),'%d-%m-%Y')
                            except:
                                errors.append("please enter date in format of dd-mm-yyyy of "+which[x]+' experience !')
                        if checkIt and req.POST.get('ex_to_'+str(x)):
                            try:
                                datetime.strptime(req.POST.get('ex_to_'+str(x)),'%d-%m-%Y')
                            except:
                                errors.append("please enter date in format of dd-mm-yyyy of "+which[x]+' experience !')
                        if not errors and checkIt:
                            expDetails.append((x,tbl_experienceDetail(standard=req.POST.get('ex_standard_'+str(x)).strip(),
                                                                   subject=req.POST.get('ex_subject_'+str(x)).strip(),
                                                                   institute=req.POST.get('ex_institute_'+str(x)).strip(),
                                                                   city=req.POST.get('ex_city_'+str(x)).strip(),
                                                                   start=datetime.strptime(req.POST.get('ex_from_'+str(x)),'%d-%m-%Y'),
                                                                   end=datetime.strptime(req.POST.get('ex_to_'+str(x)),'%d-%m-%Y'),
                                                                   type=x
                                                                   )))
                if not req.FILES.get('tphoto'):
                    errors.append("please attach teacher photo !")    
            
            
            if not errors:
                findsex={'m':'m','f':'f','ms':'f'}
                empObj=tbl_employee.objects.create(desig='teacher',isActive=True,joinDate=None)
                teacherObj=tbl_teacher.objects.create(isActive=True,empId=empObj.id)
                fdir=teacherUDir+'/'+empPrefix+str(empObj.id)
                for num,ed in eduDetails:
                    ed.doc=tbl_doc.objects.create(name=ed.qualification,belongTo='t',pkid=teacherObj.id,file=i_upload(req.FILES.get('doc_'+str(num)),fdir,'EDU_OF_'+ed.qualification+'.jpg'))
                    ed.save()
                    teacherObj.eduDetails.add(ed)
                for num,ex in expDetails:
                    ex.doc=tbl_doc.objects.create(name=ex.institute,belongTo='t',pkid=teacherObj.id,file=i_upload(req.FILES.get('ex_doc_'+str(num)),fdir,'EXP_OF_'+str(ex.institute)+'.jpg'))
                    ex.save()
                    teacherObj.expDetails.add(ex)
                
                
                tper=tbl_empPersonalDetail.objects.create(title=title,
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
                                                          image=i_upload(req.FILES.get('tphoto'),fdir,fname+'.jpg')
                                                          )
                empObj.perDetail=tper
                empObj.ifTeacher=teacherObj
                
                if totalExp:
                    empObj.totalExp=int(totalExp)
                if joindate:
                    empObj.joinDate=datetime.strptime(joindate,'%d-%m-%Y')
                if dob:
                    empObj.perDetail.dob=datetime.strptime(dob,'%d-%m-%Y')
                if age:
                    empObj.perDetail.age=int(age)
                
                empObj.perDetail.save()
                
                
                
                role=None
                if not tbl_role.objects.filter(name='for teachers'):
                    role=tbl_role.objects.create(name='for teachers',description='this role has created by system automatically and \n will be used as default role for all teachers !',assignedBy=1,isActive=bool(active))
                else:
                    role=tbl_role.objects.get(name='for teachers')
                loginAsUser=tbl_systemUser.objects.create(username=username,
                                            password=pwd,
                                            email=email,
                                            role=role,
                                            isActive=active,
                                            isAdmin=False,
                                            image=None
                                            )
                empObj.user=loginAsUser
                empObj.save()
                return HttpResponseRedirect('/teacher')
            return render_to_response('addTeacher.html',locals(),context_instance=RequestContext(req))
        return render_to_response('addTeacher.html',locals(),context_instance=RequestContext(req))



def v_editTeacher(req,_id):
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'teacher','u'):
        
        empPrefix=EMPLOYEE_PREFIX
        tPrefix=TEACHER_PREFIX
        empObj=tbl_employee.objects.get(id=_id)
        empid=empObj.id
        tid=empObj.ifTeacher.id
        states=tbl_location.objects.filter(pid=1).order_by('name')
        states2=states
        if empObj.joinDate:
            joindate=DateFormat(empObj.joinDate).format('d-m-Y')
        
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
        edus=empObj.ifTeacher.eduDetails.all()
        #return HttpResponse(edus)
        qual_1=qual_2=qual_3=qual_4=qual_5=qual_6=qual_7=''
        percent_1=percent_2=percent_3=percent_4=percent_5=percent_6=percent_7=''
        pyear_1=pyear_2=pyear_3=pyear_4=pyear_5=pyear_6=pyear_7=''
        institute_1=institute_2=institute_3=institute_4=institute_5=institute_6=institute_7=''
        city_1=city_2=city_3=city_4=city_5=city_6=city_7=''
        doc_1=doc_2=doc_3=doc_4=doc_5=doc_6=doc_7=''
        
        
        for e in edus:
            if e.type==1:
                qual_1=e.qualification
                percent_1=e.percentage
                pyear_1=e.pYear
                institute_1=e.institute
                city_1=e.city
                doc_1=e.doc
            if e.type==2:
                qual_2=e.qualification
                percent_2=e.percentage
                pyear_2=e.pYear
                institute_2=e.institute
                city_2=e.city
                doc_2=e.doc
            if e.type==3:
                qual_3=e.qualification
                percent_3=e.percentage
                pyear_3=e.pYear
                institute_3=e.institute
                city_3=e.city
                doc_3=e.doc
            if e.type==4:
                qual_4=e.qualification
                percent_4=e.percentage
                pyear_4=e.pYear
                institute_4=e.institute
                city_4=e.city
                doc_4=e.doc
            if e.type==5:
                qual_5=e.qualification
                percent_5=e.percentage
                pyear_5=e.pYear
                institute_5=e.institute
                city_5=e.city
                doc_5=e.doc
            if e.type==6:
                qual_6=e.qualification
                percent_6=e.percentage
                pyear_6=e.pYear
                institute_6=e.institute
                city_6=e.city
                doc_6=e.doc
            if e.type==7:
                qual_7=e.qualification
                percent_7=e.percentage
                pyear_7=e.pYear
                institute_7=e.institute
                city_7=e.city
                doc_7=e.doc
        
        exps=empObj.ifTeacher.expDetails.all()
        
        ex_standard_1=ex_standard_2=ex_standard_3=''
        ex_subject_1=ex_subject_2=ex_subject_3=''
        ex_institute_1=ex_institute_2=ex_institute_3=''
        ex_city_1=ex_city_2=ex_city_3=''
        ex_from_1=ex_from_2=ex_from_3=''
        ex_to_1=ex_to_2=ex_to_3=''
        ex_doc_1=ex_doc_2=ex_doc_3=''
        
        for index,ex in enumerate(exps):
            if (index+1)==1:
                ex_standard_1=ex.standard
                ex_subject_1=ex.subject
                ex_institute_1=ex.institute
                ex_city_1=ex.city
                ex_from_1=DateFormat(ex.start).format('d-m-Y')
                ex_to_1=DateFormat(ex.end).format('d-m-Y')
                ex_doc_1=ex.doc
            if (index+1)==2:
                ex_standard_2=ex.standard
                ex_subject_2=ex.subject
                ex_institute_2=ex.institute
                ex_city_2=ex.city
                ex_from_2=DateFormat(ex.start).format('d-m-Y')
                ex_to_2=DateFormat(ex.end).format('d-m-Y')
                ex_doc_2=ex.doc
            if (index+1)==3:
                ex_standard_3=ex.standard
                ex_subject_3=ex.subject
                ex_institute_3=ex.institute
                ex_city_3=ex.city
                ex_from_3=DateFormat(ex.start).format('d-m-Y')
                ex_to_3=DateFormat(ex.end).format('d-m-Y')
                ex_doc_3=ex.doc
        
        username=empObj.user.username
        pwd=empObj.user.password
        cpwd=empObj.user.password
        #active=empObj.user.isActive
        
        if req.POST.get('editTeacher',''):
            errors=[]
            eduDetails=[]
            expDetails=[]
            fdir=teacherUDir+'/'+empPrefix+str(empObj.id)
            
            title=req.POST.get('title','')
            fname=req.POST.get('fname','').strip()
            lname=req.POST.get('lname','').strip()
            dob=req.POST.get('dob','').strip()
            age=req.POST.get('age','').strip()
            email=req.POST.get('email','').strip()
            joindate=req.POST.get('joindate','').strip()
            totalExp=req.POST.get('totalExp','').strip()
            
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
            
            qual_1=req.POST.get('qual_1')
            percent_1=req.POST.get('percent_1')
            pyear_1=req.POST.get('pyear_1')
            institute_1=req.POST.get('institute_1')
            city_1=req.POST.get('city_1')
            
            
            qual_2=req.POST.get('qual_2')
            percent_2=req.POST.get('percent_2')
            pyear_2=req.POST.get('pyear_2')
            institute_2=req.POST.get('institute_2')
            city_2=req.POST.get('city_2')
            
            
            qual_3=req.POST.get('qual_3')
            percent_3=req.POST.get('percent_3')
            pyear_3=req.POST.get('pyear_3')
            institute_3=req.POST.get('institute_3')
            city_3=req.POST.get('city_3')
            
            
            qual_4=req.POST.get('qual_4')
            percent_4=req.POST.get('percent_4')
            pyear_4=req.POST.get('pyear_4')
            institute_4=req.POST.get('institute_4')
            city_4=req.POST.get('city_4')
            
            
            qual_5=req.POST.get('qual_5')
            percent_5=req.POST.get('percent_5')
            pyear_5=req.POST.get('pyear_5')
            institute_5=req.POST.get('institute_5')
            city_5=req.POST.get('city_5')
            
            
            qual_6=req.POST.get('qual_6')
            percent_6=req.POST.get('percent_6')
            pyear_6=req.POST.get('pyear_6')
            institute_6=req.POST.get('institute_6')
            city_6=req.POST.get('city_6')
            
            
            qual_7=req.POST.get('qual_7')
            percent_7=req.POST.get('percent_7')
            pyear_7=req.POST.get('pyear_7')
            institute_7=req.POST.get('institute_7')
            city_7=req.POST.get('city_7')
            
            
            
            ex_standard_1=req.POST.get('ex_standard_1')
            ex_subject_1=req.POST.get('ex_subject_1')
            ex_institute_1=req.POST.get('ex_institute_1')
            ex_city_1=req.POST.get('ex_city_1')
            ex_from_1=req.POST.get('ex_from_1')
            ex_to_1=req.POST.get('ex_to_1')
            
            
            ex_standard_2=req.POST.get('ex_standard_2')
            ex_subject_2=req.POST.get('ex_subject_2')
            ex_institute_2=req.POST.get('ex_institute_2')
            ex_city_2=req.POST.get('ex_city_2')
            ex_from_2=req.POST.get('ex_from_2')
            ex_to_2=req.POST.get('ex_to_2')
            
            
            ex_standard_3=req.POST.get('ex_standard_3')
            ex_subject_3=req.POST.get('ex_subject_3')
            ex_institute_3=req.POST.get('ex_institute_3')
            ex_city_3=req.POST.get('ex_city_3')
            ex_from_3=req.POST.get('ex_from_3')
            ex_to_3=req.POST.get('ex_to_3')
                  
            
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
            elif not empObj.perDetail.image and not req.FILES.get('tphoto'):
                errors.append("please attach teacher photo !")
            else:
                try:
                    if email!='' and tbl_empPersonalDetail.objects.filter(email=email)[0].email!=empObj.perDetail.email:
                        errors.append("email Id already exist !")
                except:
                    pass
                
                
                if dob:
                    try:
                        datetime.strptime(dob,'%d-%m-%Y')
                    except:
                        errors.append("please enter valid date of birth !")
                
                if joindate:        
                    try:
                        datetime.strptime(joindate,'%d-%m-%Y')
                    except:
                        errors.append("please enter valid joining date !")
                        
                which={1:'1st Master',2:'2nd Master',3:'1st Bachelor',4:'2nd Bachelor',5:'12th',6:'10th',7:'diploma'}
                for x in range(1,8):
                    field=['qual_','percent_','pyear_','institute_','city_']
                
                    checkIt=False
                    for item in field:
                        if req.POST.get(item+str(x)):
                            checkIt=True
                        if req.FILES.get('doc_'+str(x)):
                            checkIt=True
                            
                    if checkIt and not req.POST.get('qual_'+str(x)):
                        errors.append('please enter qualification of '+which[x]+' Details !')
                    if checkIt and not req.POST.get('percent_'+str(x)):
                        errors.append('please enter percent of '+which[x]+' Details !')
                    if checkIt and not req.POST.get('pyear_'+str(x)):
                        errors.append('please enter passed out year of '+which[x]+' Details !')
                    if checkIt and not req.POST.get('institute_'+str(x)):
                        errors.append('please enter institute of '+which[x]+' Details !')
                    if checkIt and not req.POST.get('city_'+str(x)):
                        errors.append('please enter city of '+which[x]+' Details !')
                    if (not hasDoc(edus,x)) and checkIt and not req.FILES.get('doc_'+str(x)):
                        errors.append('please attach doc of '+which[x]+' Details !')
                    if not errors and checkIt:
                        if getEDU(edus,x):
                            er=getEDU(edus,x)
                            er.qualification=req.POST.get('qual_'+str(x))
                            er.percentage=int(req.POST.get('percent_'+str(x)).strip())
                            er.pYear=int(req.POST.get('pyear_'+str(x)).strip())
                            er.institute=req.POST.get('institute_'+str(x)).strip()
                            er.city=req.POST.get('city_'+str(x)).strip()
                            
                            if req.FILES.get('doc_'+str(x)):
                                er.doc.file=i_upload(req.FILES.get('doc_'+str(x)),fdir,'EDU_OF_'+req.POST.get('qual_'+str(x))+'.jpg')
                                er.doc.save()
                                #return HttpResponse(er.doc.getImageURL())
                            er.save()
                        else:
                            eduDetails.append((x,tbl_teaEducationalDetail(type=x,qualification=req.POST.get('qual_'+str(x)).strip(),percentage=int(req.POST.get('percent_'+str(x)).strip()),pYear=int(req.POST.get('pyear_'+str(x)).strip()),institute=req.POST.get('institute_'+str(x)).strip(),city=req.POST.get('city_'+str(x)).strip())))
                            
                
                if not errors:
                    which={1:'1st',2:'2nd',3:'3rd'}
                    for x in range(1,4):
                        field=['ex_standard_','ex_subject_','ex_institute_','ex_city_','ex_from_','ex_to_']
                        checkIt=False
                        change=False
                        for item in field:
                            if req.POST.get(item+str(x)):
                                checkIt=True
                            if req.FILES.get('ex_doc_'+str(x)):
                                checkIt=True
                        
                        if checkIt and not req.POST.get('ex_standard_'+str(x)):
                            errors.append('please enter standard of '+which[x]+' experience !')
                        if checkIt and not req.POST.get('ex_subject_'+str(x)):
                            errors.append('please enter subject of '+which[x]+' experience !')
                        if checkIt and not req.POST.get('ex_institute_'+str(x)):
                            errors.append('please enter institute of '+which[x]+' experience !')
                        if checkIt and not req.POST.get('ex_city_'+str(x)):
                            errors.append('please enter city of '+which[x]+' experience !')
                        if checkIt and not req.POST.get('ex_from_'+str(x)):
                            errors.append("please enter 'from' field of "+which[x]+" experience !")
                        if checkIt and not req.POST.get('ex_to_'+str(x)):
                            errors.append("please enter 'to' field of "+which[x]+" experience !")
                        if (not hasDoc(exps,x)) and checkIt and not req.FILES.get('ex_doc_'+str(x)):
                            errors.append('please attach certificate of '+which[x]+' experience !')
                        if checkIt and req.POST.get('ex_from_'+str(x)):
                            try:
                                datetime.strptime(req.POST.get('ex_from_'+str(x)),'%d-%m-%Y')
                            except:
                                errors.append("please enter date in format of dd-mm-yyyy of "+which[x]+' experience !')
                        if checkIt and req.POST.get('ex_to_'+str(x)):
                            try:
                                datetime.strptime(req.POST.get('ex_to_'+str(x)),'%d-%m-%Y')
                            except:
                                errors.append("please enter date in format of dd-mm-yyyy of "+which[x]+' experience !')
                        if not errors and checkIt:
                            if getEDU(exps,x):
                                xr=getEDU(exps,x)
                                xr.standard=req.POST.get('ex_standard_'+str(x)).strip()
                                xr.subject=req.POST.get('ex_subject_'+str(x)).strip()
                                xr.institute=req.POST.get('ex_institute_'+str(x)).strip()
                                xr.city=req.POST.get('ex_city_'+str(x)).strip()
                                xr.start=datetime.strptime(req.POST.get('ex_from_'+str(x)),'%d-%m-%Y')
                                xr.end=datetime.strptime(req.POST.get('ex_to_'+str(x)),'%d-%m-%Y')
                                if req.FILES.get('ex_doc_'+str(x)):
                                    xr.doc.file=i_upload(req.FILES.get('ex_doc_'+str(x)),fdir,'EXP_OF_'+str(xr.institute)+'.jpg')
                                    xr.doc.save()
                                xr.save()
                            else:
                                expDetails.append((x,tbl_experienceDetail(type=x,standard=req.POST.get('ex_standard_'+str(x)).strip(),
                                                                   subject=req.POST.get('ex_subject_'+str(x)).strip(),
                                                                   institute=req.POST.get('ex_institute_'+str(x)).strip(),
                                                                   city=req.POST.get('ex_city_'+str(x)).strip(),
                                                                   start=datetime.strptime(req.POST.get('ex_from_'+str(x)),'%d-%m-%Y'),
                                                                   end=datetime.strptime(req.POST.get('ex_to_'+str(x)),'%d-%m-%Y')
                                                                   )))
            if not errors:
                findsex={'m':'m','f':'f','ms':'f'}
                teacherObj=empObj.ifTeacher
                
                for num,ed in eduDetails:
                    ed.doc=tbl_doc.objects.create(name=ed.qualification,belongTo='t',pkid=teacherObj.id,file=i_upload(req.FILES.get('doc_'+str(num)),fdir,'EDU_OF_'+ed.qualification+'.jpg'))
                    ed.save()
                    teacherObj.eduDetails.add(ed)
                for num,ex in expDetails:
                    ex.doc=tbl_doc.objects.create(name=ex.institute,belongTo='t',pkid=teacherObj.id,file=i_upload(req.FILES.get('ex_doc_'+str(num)),fdir,'EXP_OF_'+str(ex.institute)+'.jpg'))
                    ex.save()
                    teacherObj.expDetails.add(ex)
                    
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
                
                empObj.perDetail.email=email
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
                if req.FILES.get('tphoto'):
                    empObj.perDetail.image=i_upload(req.FILES.get('tphoto'),fdir,fname+'.jpg')
                
                empObj.ifTeacher=teacherObj
                
                if totalExp:
                    empObj.totalExp=int(totalExp)
                if joindate:
                    empObj.joinDate=datetime.strptime(joindate,'%d-%m-%Y')
                else:
                    empObj.joinDate=None
                    
                empObj.perDetail.save()
                empObj.ifTeacher.save()
                empObj.save()
                return HttpResponseRedirect('/teacher/edit/'+str(empObj.id))
            return render_to_response('editTeacher.html',locals(),context_instance=RequestContext(req))
        return render_to_response('editTeacher.html',locals(),context_instance=RequestContext(req))
    


def hasDoc(_list,_type):
    try:
        if _list.get(type=_type):
            return True
    except:
        return False
            
def getEDU(allEdu,_type):
    try:
        return allEdu.get(type=_type)
    except:
        pass
    
