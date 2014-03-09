from django.db import models
import datetime
from SMS.settings import uploadFolder, djangoUpload, schoolUDir, STUDENTPREFIX,\
    EMPLOYEE_PREFIX, LIBMEMPREFIX, LIBPREFIX, TEACHER_PREFIX
    
# Create your models here.
class tbl_product(models.Model):
    purchaseDate=models.DateField(null=True,blank=True)
    agent=models.IntegerField(null=True,blank=True)
    
    schoolName=models.CharField(max_length=250,null=True,blank=True)
    customerName=models.CharField(max_length=250,null=True,blank=True)
    contactNo=models.CharField(max_length=30,null=True,blank=True)
    address=models.TextField(null=True,blank=True)
    email=models.CharField(max_length=250,null=True,blank=True)
    
    sid=models.IntegerField(null=True,blank=True)
    lastAccess=models.DateField(null=True,blank=True)
    expireDate=models.DateField(null=True,blank=True)
    key=models.CharField(max_length=250,null=True,blank=True) 

class tbl_location(models.Model):
    name=models.CharField(max_length=100)
    pid=models.IntegerField(null=True,blank=True)
    type=models.CharField(max_length=2,null=True,blank=True)
    
    def __unicode__(self):
        return "%s-%s-%s"%(self.id,self.name,self.pid)



class tbl_school(models.Model):
    name=models.TextField(null=True,blank=True)
    address=models.TextField(null=True,blank=True)
    city=models.ForeignKey(tbl_location,null=True,blank=True)
    contactNo=models.BigIntegerField(null=True,blank=True)
    affiliatedBy=models.TextField(null=True,blank=True)
    openingDate=models.DateField(null=True,blank=True)
    logoImage=models.ImageField(upload_to=schoolUDir,null=True,blank=True)
    website=models.TextField(null=True,blank=True)
    
    paydate=models.DateField(null=True,blank=True)
    amount=models.IntegerField(default=0)
    reciptno=models.CharField(max_length="25",null=True,blank=True)
    paymode=models.CharField(max_length="10",null=True,blank=True)
    bankname=models.CharField(max_length="50",null=True,blank=True)
    chequeno=models.CharField(max_length="25",null=True,blank=True)
    chequedate=models.DateField(null=True,blank=True)
    session1=models.CharField(max_length="100",null=True,blank=True)
    #chequeDepoDate=models.DateField(null=True,blank=True)
    #chequeClearDate=models.DateField(null=True,blank=True)
    createdOn=models.DateField(default=datetime.date.today())
    def getPaymentMode(self):
        if self.paymode=='c':
            return "Cash"
        elif self.paymode=='d':
            return "Draft"
        elif self.paymode=='chq':
            return "Cheque"
        elif self.paymode=='a':
            return "NEFT"
        elif self.paymode=='o':
            return "Online"
        else:
            return ''
    def getstatename(self):
        state=tbl_location.objects.get(id=self.city.pid)
        return state.name
    def getcityname(self):
        
        return self.city.name
    def getimageurl(self):
        if self.logoImage:
            return self.logoImage.url
        else:
            return ""
    def __unicode__(self):
        return u'%s-%s-%s'%(self.id,self.name,self.address)
    def getPayDate(self):
        if self.paydate:
            x=datetime.datetime.strptime(str(self.paydate), '%Y-%m-%d')
            return x.strftime('%d-%m-%Y')
        else:
            return ''
    def getChequeDate(self):
        if self.chequedate:
            x=datetime.datetime.strptime(str(self.chequedate), '%Y-%m-%d')
            return x.strftime('%d-%m-%Y')
        else:
            return ''
    def getSession(self):
        try:
            sessiondict=eval(self.session1)
            startmonth=sessiondict['startsession']
            endmonth=sessiondict['endsession']
            curDate=datetime.date.today()
            if curDate.month<=endmonth:
                startyear=curDate.year-1
                endyear=curDate.year
            else:
                startyear=curDate.year
                endyear=curDate.year+1
            return str(startyear)+'-'+str(endyear)
        except:
            return ''


            
class tbl_medium(models.Model):
    name=models.CharField(max_length='100',null=True,blank=True)
    isActive=models.BooleanField(default=False)
    createdOn=models.DateField(default=datetime.date.today())
    def __unicode__(self):
        return u"%s-%s"%(self.id,self.name)
    #createdOn=models.DateField(default=datetime.date.today())




class tbl_class(models.Model):
    name=models.CharField(max_length='100',null=True,blank=True)
    isActive=models.BooleanField(default=False)
    #standard=models.ForeignKey(tbl_standard,null=True,blank=True)
    #medium=models.ForeignKey(tbl_medium,null=True,blank=True)
   
    createdOn=models.DateField(default=datetime.date.today())
    
    def __unicode__(self):
        return u"ID%s-%s"%(self.id,self.name)
    
    
    
class tbl_standard(models.Model):
    name=models.CharField(max_length='100',null=True,blank=True)
    medium=models.ForeignKey(tbl_medium,null=True,blank=True)
    period=models.IntegerField(null=True,blank=True)
    sections=models.ManyToManyField(tbl_class,null=True,blank=True)
    timePeriod=models.IntegerField(default=0,null=True,blank=True)
    isActive=models.BooleanField(default=False)
    createdOn=models.DateField(default=datetime.date.today())
    def __unicode__(self):
        return u"%s-%s"%(self.id,self.name)
    def createMSS(self,teacherId):
        for data in self.sections.all():
            if tbl_MSS.objects.filter(medium=self.medium,standard=self,section=data):
                obj=tbl_MSS.objects.filter(medium=self.medium,standard=self,section=data)[0]
                if teacherId==-1:
                    pass
                else:
                    tobj=tbl_teacher.objects.get(id=teacherId)
                    obj.classTeacher=tobj
                    tobj.ifCT=1
                    tobj.save()
                obj.isActive=True
                obj.save()
            else:
                p1=tbl_MSS()
                p1.medium=self.medium
                p1.standard=self
                p1.section=data
                if teacherId==-1:
                    pass
                else:
                    tobj=tbl_teacher.objects.get(id=teacherId)
                    p1.classTeacher=tobj
                    tobj.ifCT=1
                    tobj.save()
                p1.isActive=True    
                p1.save()
    def getMSS(self):
        getmss=[]
        for data in self.sections.filter(isActive=True):
            
            getmss.append(tbl_MSS.objects.get(medium=self.medium,standard=self,section=data,isActive=True))
        return getmss
    def createshortstandard(self):
        getobj=tbl_shortstandard.objects.filter(name=self.name)
        if getobj:
            pass
        else:
            p1=tbl_shortstandard()
            p1.name=self.name
            p1.save()


class tbl_subject(models.Model):
    name=models.CharField(max_length='200',null=True,blank=True)
    standards=models.ManyToManyField(tbl_standard,null=True,blank=True)
    start=models.IntegerField(null=True,blank=True)
    end=models.IntegerField(null=True,blank=True)
    isActive=models.BooleanField(default=False)
    #standard=models.ForeignKey(tbl_standard,null=True,blank=True)
    createdOn=models.DateField(default=datetime.date.today())
    def __unicode__(self):
        return u"%s-%s"%(self.id,self.name)    
    
    
    def getStartStandard(self):
        try:
            return tbl_shortstandard.objects.get(id=self.start).name
        except:
            return ''
    def getEndStandard(self):
        try:
            return tbl_shortstandard.objects.get(id=self.end).name
        except:
            return ''


class tbl_doc(models.Model):
    '''
    docs will upload at different location based on which category they belongs to
    each category has upload directory defined in settings.py file.
    
    
    NOTE:to maintain project upload heirarchy file should not be uploaded through django panel if it is uploaded 
    it will be at djangoUpload directory defined in settings.py  
    
    pkid hold id of person to which doc belongs
    '''
    belong=(('u','user'),('s','student'),('t','teacher'),('sc','school'))
    pkid=models.IntegerField(null=True,blank=True)
    name=models.CharField(max_length=100,null=True,blank=True)
    belongTo=models.CharField(max_length=2,choices=belong,null=True,blank=True)
    file=models.FileField(upload_to=djangoUpload,null=True,blank=True)
    
    createdOn=models.DateField(default=datetime.date.today())
    def getImageURL(self):
        if self.file:
            return uploadFolder+self.file.url


class tbl_empPersonalDetail(models.Model):
    title_choice=(('m','Mr.'),('f','Mrs.'),('ms','Miss'))
    sex_choice=(('m','Male'),('f','Female'))
    
    title=models.CharField(max_length=5,choices=title_choice,null=True,blank=True)
    fName=models.CharField(max_length=100,null=True,blank=True)
    lName=models.CharField(max_length=100,null=True,blank=True)
    age=models.IntegerField(null=True,blank=True)
    sex=models.CharField(max_length=1,choices=sex_choice,null=True,blank=True)
    dob=models.DateField(null=True,blank=True)
    email=models.CharField(max_length=150,null=True,blank=True)
    
    lAdd=models.CharField(max_length=500,null=True,blank=True)
    lCity=models.ForeignKey(tbl_location,null=True,blank=True,related_name='l1')
    lpin=models.CharField(max_length=15,null=True,blank=True)
    lMobile=models.CharField(max_length=15,null=True,blank=True)
    lLandline=models.CharField(max_length=20,null=True,blank=True)
    
    pAdd=models.CharField(max_length=500,null=True,blank=True)
    pCity=models.ForeignKey(tbl_location,null=True,blank=True,related_name='p2')
    ppin=models.CharField(max_length=15,null=True,blank=True)
    pMobile=models.CharField(max_length=15,null=True,blank=True)
    pLandline=models.CharField(max_length=20,null=True,blank=True)
    
    image=models.ImageField(upload_to=djangoUpload,null=True,blank=True)
    
    createdOn=models.DateField(default=datetime.date.today())
    
    def getURL(self):
        if self.image:
            return uploadFolder+self.image.url
    
    def __unicode__(self):
        return "%s-%s" %(self.fName,self.lName)




class tbl_stdPersonalDetail(models.Model):
    title_choice=(('m','Mr.'),('f','Mrs.'),('ms','Miss'))
    sex_choice=(('m','Male'),('f','Female'))
   
    title=models.CharField(max_length=5,choices=title_choice,null=True,blank=True)
    fName=models.CharField(max_length=100,null=True,blank=True)
    lName=models.CharField(max_length=100,null=True,blank=True)
    age=models.IntegerField(null=True,blank=True)
    sex=models.CharField(max_length=1,choices=sex_choice,null=True,blank=True)
    dob=models.DateField(null=True,blank=True)
    #email=models.CharField(max_length=150,unique=True)
   
    lAdd=models.CharField(max_length=500,null=True,blank=True)
    lCity=models.ForeignKey(tbl_location,null=True,blank=True,related_name='l')
    lpin=models.CharField(max_length=25,null=True,blank=True)
    lMobile=models.CharField(max_length=25,null=True,blank=True)
    lLandline=models.CharField(max_length=25,null=True,blank=True)
   
    pAdd=models.CharField(max_length=500,null=True,blank=True)
    pCity=models.ForeignKey(tbl_location,null=True,blank=True,related_name='p')
    ppin=models.CharField(max_length=25,null=True,blank=True)
    pMobile=models.CharField(max_length=25,null=True,blank=True)
    pLandline=models.CharField(max_length=25,null=True,blank=True)
   
    image=models.ImageField(upload_to=djangoUpload,null=True,blank=True)
   
   
    fatherName=models.CharField(max_length=100,null=True,blank=True)
    fAge=models.IntegerField(null=True,blank=True)
    fOccupation=models.CharField(max_length=100,null=True,blank=True)
    fSalary=models.BigIntegerField(null=True,blank=True)
    fOfficeNo=models.CharField(max_length=25,null=True,blank=True)
    fMobile=models.CharField(max_length=25,null=True,blank=True)
   
    motherName=models.CharField(max_length=100,null=True,blank=True)
    mAge=models.IntegerField(null=True,blank=True)
    mOccupation=models.CharField(max_length=100,null=True,blank=True)
    mSalary=models.BigIntegerField(null=True,blank=True)
    mOfficeNo=models.CharField(max_length=20,null=True,blank=True)
    mMobile=models.CharField(max_length=20,null=True,blank=True)
    '''
    below details will be used for emergency purpose
    '''
    personName=models.CharField(max_length=100,null=True,blank=True)
    contactNo=models.CharField(max_length=20,null=True,blank=True)
    relation=models.CharField(max_length=100,null=True,blank=True)
   
    createdOn=models.DateField(default=datetime.date.today())
    
    def getName(self):
        return self.fName+" "+self.lName

    def __unicode__(self):
        try:
            return u'%s-%s'%(self.id,self.getName())
        except:
            return ''


class tbl_teaEducationalDetail(models.Model):
    '''
    for now type will be
    
    master:1,2
    bachelor:3,4
    12th=5
    10th=6
    diploma=7
    '''
    qualification=models.CharField(max_length=150,null=True,blank=True)
    percentage=models.BigIntegerField(null=True,blank=True)
    pYear=models.BigIntegerField(null=True,blank=True)
    institute=models.CharField(max_length=500,null=True,blank=True)
    city=models.CharField(max_length=100,null=True,blank=True)
    doc=models.ForeignKey(tbl_doc,null=True,blank=True)
    type=models.IntegerField(null=True,blank=True)
    
    createdOn=models.DateField(default=datetime.date.today())
    
    def __unicode__(self):
        return '%s-%s'%(self.qualification,self.city) 
    
    




class tbl_sibling(models.Model):
    studentId=models.IntegerField(null=True,blank=True)
    isActive=models.BooleanField(default=False)
    '''
    below field is redundant taken for quick access
    '''
    name=models.CharField(max_length=100,null=True,blank=True)
    standard=models.ForeignKey(tbl_standard,null=True,blank=True)
    def getsibid(self):
        return STUDENTPREFIX+str(self.studentId)
    def getsibname(self):
        try:
            return tbl_student.objects.get(id=self.studentId).perDetail.fName+" "+tbl_student.objects.get(id=self.studentId).perDetail.lName
        except:
            return ''
    def __unicode__(self):
        return u'%s-SIBLINGID-%s'%(self.id,self.studentId)
    

class  tbl_stdEducationalDetail(models.Model):
    '''
    student Previous school educational details
    '''
    oldAdmission=models.CharField(max_length=25,null=True,blank=True)
    rollNo=models.CharField(max_length=25,null=True,blank=True)
    school=models.CharField(max_length=500,null=True,blank=True)
    standard=models.CharField(max_length=100,null=True,blank=True)
    pYear=models.IntegerField(null=True,blank=True)
    percentage=models.IntegerField(null=True,blank=True)
    medium=models.CharField(max_length=100,null=True,blank=True)
    docs=models.ManyToManyField(tbl_doc,null=True,blank=True)
   
    createdOn=models.DateField(default=datetime.date.today())
    def __unicode__(self):
        try:
            return u'%s-%s'%(self.id,self.school)
        except:
            return u'%s'%(self.id)

class tbl_experienceDetail(models.Model):
    '''
    for now type will be 
    1 for 1st section 
    2     2nd 
    3     3rd
    '''
    standard=models.CharField(max_length=100,null=True,blank=True)
    subject=models.CharField(max_length=100,null=True,blank=True)
    institute=models.CharField(max_length=500,null=True,blank=True)
    city=models.CharField(max_length=100,null=True,blank=True)
    start=models.DateField(default=datetime.date.today())
    end=models.DateField(default=datetime.date.today())
    doc=models.ForeignKey(tbl_doc,null=True,blank=True)
    type=models.IntegerField(null=True,blank=True)
    createdOn=models.DateField(default=datetime.date.today())
    
    def __unicode__(self):
        return 'ID:%s - %s-%s'%(self.id,self.institute,self.city) 
    
class tbl_contentType(models.Model):
    category=models.CharField(max_length=100)
    name=models.CharField(max_length=100,unique=True)
    isActive=models.BooleanField(default=False)
    
    def __unicode__(self):
        return '%s %s %s'%(self.id,self.category,self.name) 
    

class tbl_permission(models.Model):
    content=models.ForeignKey(tbl_contentType)
    view=models.BooleanField(default=False)
    add=models.BooleanField(default=False)
    update=models.BooleanField(default=False)
    delete=models.BooleanField(default=False)
    
    createdOn=models.DateField(default=datetime.date.today())
    updatedOn=models.DateField(default=datetime.date.today())
    def validate_unique(self, exclude=None):
        models.Model.validate_unique(self, exclude=exclude)
        self.updatedOn=datetime.date.today()
    def __unicode__(self):
        return "%s-%s- View/%s - Add/%s - Update/%s - Delete/%s "%(self.id,self.content,self.view,self.add,self.update,self.delete)

class tbl_role(models.Model):
    name=models.CharField(max_length=100,unique=True)
    description=models.TextField(null=True,blank=True)
    permissions=models.ManyToManyField(tbl_permission,null=True,blank=True)
    assignedBy=models.IntegerField(null=True,blank=True)
    
    isActive=models.BooleanField(default=False)
    createdOn=models.DateField(default=datetime.date.today())
    updatedOn=models.DateField(default=datetime.date.today())
    def validate_unique(self, exclude=None):
        models.Model.validate_unique(self, exclude=exclude)
        self.updatedOn=datetime.date.today()
    def __unicode__(self):
        return "%s-%s"%(self.id,self.name)

#class tbl_smsUser(models.Model):
class tbl_classStudent(models.Model):
    studentId=models.IntegerField(null=True,blank=True)
    rollNo=models.CharField(max_length=200,null=True,blank=True)
    def __unicode__(self):
        return "%s-roll No.%s-StudentID%s"%(self.id,self.rollNo,self.studentId)
    def getname(self):
        return tbl_student.objects.get(id=self.studentId).getName()
    def getstudentId(self):
        return STUDENTPREFIX+str(self.studentId)


class tbl_subjectMarks(models.Model):
    '''
    store details of single subject test
     
    marks will contain records of test marks of students in a class in form 
    "{class Student Id:subject marks,....}"
    
    
    NOTE:students which are absent will have (-1) in marks field
    mssId a unique class ID in  school
    tid teacher Id
    
    detail is used to store aggregate details of a subject test in form with some common details like MAX marks ,MIN marks
    
    total=total No.of student in class
    pass=no.of student pass
    fail=no.of student fail
    absent=no.of student absent
    MAX=maximum marks of test
    MIN=passing marks for test
    
    "{'total':100,'pass':75,'fail':23},'absent':2,'max':100,'min':35"}
     
    '''
    
    hasSession=models.CharField(max_length=50,null=True,blank=True)
    mssId=models.IntegerField(null=True,blank=True)
    tid=models.IntegerField(null=True,blank=True)
    subject=models.CharField(max_length=200,null=True,blank=True)
    testName=models.CharField(max_length=100,null=True,blank=True)
    testDate=models.DateField(null=True,blank=True)
    marks=models.TextField(null=True,blank=True)
    
    detail=models.CharField(max_length=500,null=True,blank=True)
    createdOn=models.DateField(default=datetime.date.today())
    
    def __unicode__(self):
        return "ID:%s-%s"%(self.id,self.subject)


class tbl_subjectAndTeacher(models.Model):
    '''
    ifCT=ifclass teacher
    '''
    hasSession=models.CharField(max_length=50,null=True,blank=True)
    mssId=models.IntegerField(null=True,blank=True)
    tid=models.IntegerField(null=True,blank=True)
    subject=models.CharField(max_length=200,null=True,blank=True)
    subjectResults=models.ManyToManyField(tbl_subjectMarks,null=True,blank=True)
    #ifCT=models.BooleanField(default=False)
    
    def __unicode__(self):
        return "ID:%s-%s"%(self.id,self.subject)


class  tbl_examResult(models.Model):
    '''
    detail is used to store aggregate details of all subject result in form with some common details like MAX marks ,MIN marks
    "{'total(total No.of student in class)':100,'pass(no.of student pass)':75,'fail(no.of student fail)':23},'absent(no.of student absent)':2,'MAX':100,'MIN':35"} 
    '''
    examName=models.CharField(max_length=100,null=True,blank=True,unique=True)
    examDate=models.DateField(null=True,blank=True)
    allSubjectMarks=models.ManyToManyField(tbl_subjectMarks,null=True,blank=True)
    
    detail=models.CharField(max_length=500,null=True,blank=True)
    
#class tbl_classTeacher(models.Model):
#    mssId=models.IntegerField(null=True,blank=True)
#    tid=models.IntegerField(null=True,blank=True)
#    subject=models.CharField(max_length=200,null=True,blank=True)
#    subjectResults=models.ManyToManyField(tbl_subjectMarks,null=True,blank=True)
    def __unicode__(self):
        return u'%s-%s'%(self.examName,self.examDate)


class tbl_teacher(models.Model):
    '''
    empId is redundant field taken for quick access
    ifCT  if teacher is class teacher then id of MSS  
    '''
    empId=models.IntegerField(null=True,blank=True)
    eduDetails=models.ManyToManyField(tbl_teaEducationalDetail,null=True,blank=True)
    expDetails=models.ManyToManyField(tbl_experienceDetail,null=True,blank=True)
    ifCT=models.IntegerField(null=True,blank=True)
    isActive=models.BooleanField(default=False)
    createdOn=models.DateField(default=datetime.date.today())
    
    def __unicode__(self):
        return "TID:%s-    EMPID:%s"%(self.id,self.empId)
    
    def getFullName(self):
        try:
            emp=tbl_employee.objects.get(id=self.empId).perDetail
            return emp.fName+" "+emp.lName
        except:
            pass
    def getTeacherId(self):
        return EMPLOYEE_PREFIX+str(self.empId)   
        
class tbl_systemUser(models.Model):
    username=models.CharField(max_length=30,unique=True)
    password=models.CharField(max_length=30)
    email=models.CharField(max_length=150)
    role=models.ForeignKey(tbl_role,null=True,blank=True)
    image=models.ImageField(upload_to=djangoUpload,null=True,blank=True)
    
    isActive=models.BooleanField(default=False)
    isAdmin=models.BooleanField(default=False)
    isSuper=models.BooleanField(default=False)#super user is admin who's right can not be removed (only single super user exist for whole system),isSuper will hide admin from userlist and edit  
    createdOn=models.DateField(default=datetime.date.today())
    def __unicode__(self):
        return "EMP ID:%s"%(self.id)
    def getImageURL(self):
        if self.image:
            return uploadFolder+self.image.url

class tbl_employee(models.Model):
    user=models.ForeignKey(tbl_systemUser,null=True,blank=True)
    joinDate=models.DateField(blank=True,null=True)
    desig=models.CharField(max_length=100,null=True,blank=True)
    perDetail=models.ForeignKey(tbl_empPersonalDetail,null=True,blank=True)
    ifTeacher=models.ForeignKey(tbl_teacher,null=True,blank=True)
    salary=models.BigIntegerField(null=True,blank=True)
    totalExp=models.BigIntegerField(null=True,blank=True)
    
    isActive=models.BooleanField(default=False)
    createdOn=models.DateField(default=datetime.date.today())
    
    def getEMPId(self):
        return EMPLOYEE_PREFIX+str(self.id)
    def getEMPName(self):
        return self.perDetail.fName+' '+self.perDetail.lName
    def getEMPAdd(self):
        return self.perDetail.lAdd
    def getEMPContact(self):
        if self.perDetail.lMobile:
            return str(self.perDetail.lMobile)
        if self.perDetail.lLandline:
            return str(self.perDetail.lLandline)

class tbl_MSS(models.Model):
    
    ''' 
    MSS(Medium Standard Section) represent unique class in school,it contains all details of a class
    '''
    classTeacher=models.ForeignKey(tbl_teacher,null=True,blank=True)
    medium=models.ForeignKey(tbl_medium,null=True,blank=True)
    standard=models.ForeignKey(tbl_standard,null=True,blank=True)
    section=models.ForeignKey(tbl_class,null=True,blank=True)
    
    students=models.ManyToManyField(tbl_classStudent,null=True,blank=True)
    subjectAndTeachers=models.ManyToManyField(tbl_subjectAndTeacher,null=True,blank=True)
    #classTeacher=models.ForeignKey(tbl_classTeacher,null=True,blank=True)
    examResults=models.ManyToManyField(tbl_examResult,null=True,blank=True)
    
    isActive=models.BooleanField(default=True)
    createdOn=models.DateField(default=datetime.date.today())
    def __unicode__(self):
        return "ID:%s -%s"%(self.id,self.getName())
    def getName(self):
        return "%s-%s ( %s )"%(self.standard.name,self.section.name,self.medium.name)


class tbl_studentLog(models.Model):
    mss=models.ForeignKey(tbl_MSS,null=True,blank=True)
    session1=models.CharField(max_length="25",null=True,blank=True)
    rollNo=models.CharField(max_length="25",null=True,blank=True)
    def __unicode__(self):
        return "ID%s-%s-%s"%(self.id,self.mss.id,self.session1)
    
    
class tbl_feetype(models.Model):
    name=models.CharField(max_length=25,null=True,blank=True)
    types=models.CharField(max_length=25,null=True,blank=True)
    month=models.CharField(max_length=50,null=True,blank=True)
    facility=models.BooleanField(default=False)
    def gettype(self):
        if self.types=='y':
            return 'yearly'
        elif self.types=='m':
            return 'monthly'
        elif self.types=='q':
            return 'quarterly'
        else: 
            return 'halfyearly'
    def __unicode__(self):
        return u'%s-%s-%s'%(self.id,self.name,self.types)

   
class tbl_studentFacility(models.Model):
    facility=models.ForeignKey(tbl_feetype,null=True,blank=True)

class tbl_student(models.Model):
    perDetail=models.ForeignKey(tbl_stdPersonalDetail,null=True,blank=True)
    eduDetail=models.ForeignKey(tbl_stdEducationalDetail,null=True,blank=True)
    siblings=models.ManyToManyField(tbl_sibling,null=True,blank=True)
    standard=models.ForeignKey(tbl_standard,null=True,blank=True)
    section=models.ForeignKey(tbl_class,null=True,blank=True)
    history=models.ManyToManyField(tbl_studentLog,null=True,blank=True)
    isActive=models.BooleanField(default=False)
    facilities=models.ManyToManyField(tbl_studentFacility,null=True,blank=True)
    createdOn=models.DateField(default=datetime.date.today())

    def __unicode__(self):
        return "ID%s-%s"%(self.id,self.getName())
    def getName(self):
        try:
            return self.perDetail.fName+" "+self.perDetail.lName
        except:
            return ''
    def getSTUDid(self):
        try:
            return STUDENTPREFIX+str(self.id)
        except:
            return ''
    def getContactNo(self):
        try:
            if self.perDetail.lMobile:
                return str(self.perDetail.lMobile)
            if self.perDetail.lLandline:
                return str(self.perDetail.lLandline)
        except:
            return ''
    
class tbl_shortstandard(models.Model):
    name=models.CharField(max_length=20,null=True,blank=True)
    def __unicode__(self):
        return "%s-%s"%(self.id,self.name)
class tbl_examType(models.Model):
    name=models.CharField(max_length=100,null=True,blank=True)
    def __unicode__(self):
        return "%s"%(self.name)
    
    
class tbl_markAttendence(models.Model):
    employee=models.ForeignKey(tbl_employee,null=True,blank=True)
    timein=models.TimeField(null=True,blank=True)
    timeout=models.TimeField(null=True,blank=True)
    absent=models.BooleanField(default=False)
    
    def __unicode__(self):
        return u'%s-%s'%(self.id,self.employee.getEMPName())
    
    def gettime(self):
        if self.absent==True:
            return 'A'
        else:
            if self.timein:
                if self.timeout:
                    return str(self.timein)[:5]+' '+str(self.timeout)[:5]
                else:
                    return str(self.timein)[:5]
            else:
                return ''
    def getempID(self):
        return EMPLOYEE_PREFIX+str(self.id)
    def gettimeinMin(self):
        if self.timein:
            return str(self.timein)[3:5]
        else:
            return ''
    def gettimeinHour(self):
        if self.timein:
            return str(self.timein)[0:2]
        else:
            return ''
        
    def gettimeoutMin(self):
        if self.timeout:
            return str(self.timeout)[3:5]
        else:
            return ''
    def gettimeoutHour(self):
        if self.timeout:
            return str(self.timeout)[0:2]
        else:
            return ''
    
        
class tbl_attendence(models.Model):
    date=models.DateField(null=True,blank=True)
    marking=models.ManyToManyField(tbl_markAttendence)
    session1=models.CharField(max_length=25,null=True,blank=True)
    def rdate(self):
        x=datetime.datetime.strptime(str(self.date), '%Y-%m-%d')
        return x.strftime('%d-%m-%Y')
    def getday(self):
        x=datetime.datetime.strptime(str(self.date), '%Y-%m-%d')
        return x.strftime('%d')
        
    def __unicode__(self):
        return u'%s-%s'%(self.id,self.date)


class tbl_holiday(models.Model):
    session1=models.CharField(max_length=25,null=True,blank=True)
    date=models.DateField(null=True,blank=True)  
    festival=models.CharField(max_length=50,null=True,blank=True)
    def getdate(self):
        x=datetime.datetime.strptime(str(self.date), '%Y-%m-%d')
        return x.strftime('%d-%m-%Y')
    
    def __unicode__(self):
        return u'%s-%s-%s'%(self.id,self.date,self.festival) 


class tbl_taskList(models.Model):
    username=models.ForeignKey(tbl_employee,null=True,blank=True)
    completedDate=models.DateTimeField(default=datetime.datetime.today())
    description=models.TextField(null=True,blank=True)
    isActive=models.BooleanField(default=True)
    def __unicode__(self):
        return "%s-%s"%(self.id,self.description)






class tbl_feeParameter(models.Model):
    name=models.CharField(max_length=25,null=True,blank=True)
    amt=models.IntegerField(null=True,blank=True)
    def __unicode__(self):
        return u'%s-%s'%(self.id,self.name)

class tbl_fees(models.Model):
    standard=models.ForeignKey(tbl_standard,null=True,blank=True)
    month=models.IntegerField(null=True,blank=True)
    session1=models.CharField(max_length=25,null=True,blank=True)
    amount=models.IntegerField(default=0)
    feesparameter=models.ManyToManyField(tbl_feeParameter,null=True,blank=True)
    def getmonthname(self):
        mondict={1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'June',7:'July',8:'Aug',9:'Sept',10:'Oct',11:'Nov',12:'Dec'}
        return mondict[self.month]
    def __unicode__(self):
        return u'%s-%s'%(self.id,self.month)

class tbl_tempFees(models.Model):
    standard=models.ForeignKey(tbl_standard,null=True,blank=True)
    parameter=models.TextField(null=True,blank=True)
    
    def __unicode__(self):
        return u'%s-%s'%(self.id,self.standard.name)
    
class tbl_feePayment(models.Model):
    studid=models.ForeignKey(tbl_student,null=True,blank=True)
    month=models.IntegerField(null=True,blank=True)
    session1=models.CharField(max_length=25,null=True,blank=True)
    date=models.DateField(null=True,blank=True)
    reciptno=models.CharField(max_length="25",null=True,blank=True)
    paymode=models.CharField(max_length="10",null=True,blank=True)
    bankname=models.CharField(max_length="50",null=True,blank=True)
    chequeno=models.CharField(max_length="25",null=True,blank=True)
    chequedate=models.DateField(null=True,blank=True)
    chequeDepoDate=models.DateField(null=True,blank=True)
    chequeClearDate=models.DateField(null=True,blank=True)
    def __unicode__(self):
        return u'%s-%s'%(self.id,self.studid.id)
    def getPaymentMode(self):
        if self.paymode=='c':
            return "Cash"
        elif self.paymode=='d':
            return "Draft"
        elif self.paymode=='chq':
            return "Cheque"
        elif self.paymode=='a':
            return "NEFT"
        elif self.paymode=='o':
            return "Online"
    def rdate(self):
        x=datetime.datetime.strptime(str(self.date), '%Y-%m-%d')
        return x.strftime('%d-%m-%Y')
    def rchequedate(self):
        if self.chequedate:
            x=datetime.datetime.strptime(str(self.chequedate), '%Y-%m-%d')
            return x.strftime('%d-%m-%Y')
        else:
            return ''    
    def rdepositedate(self):
        if self.chequeDepoDate:
            x=datetime.datetime.strptime(str(self.chequeDepoDate), '%Y-%m-%d')
            return x.strftime('%d-%m-%Y')
        else:
            return ''
    def rcleardate(self):
        if self.chequeClearDate:
            x=datetime.datetime.strptime(str(self.chequeClearDate), '%Y-%m-%d')
            return x.strftime('%d-%m-%Y')
        else:
            return ''
    def getMonth(self):
        dictMonth={1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'June',7:'July',8:'Aug',9:'Sept',10:'Oct',11:'Nov',12:'Dec'}
        return dictMonth[self.month]




class tbl_timeTable(models.Model):
    '''
    if subject not passed from form still row will be created with subject has value '-1' and teacher as None
    day start from Monday as (1),tue (2),...
    '''
    mss=models.ForeignKey(tbl_MSS,null=True,blank=True)
    day=models.IntegerField(null=True,blank=True)
    period=models.IntegerField(null=True,blank=True)
    subject=models.CharField(max_length=200,null=True,blank=True)
    teacher=models.ForeignKey(tbl_teacher,null=True,blank=True)
    
    def __unicode__(self):
        return "ID:%s - MSS:%s - DAY:%s: - PERIOD:%s - SUBJECT:%s"%(self.id,self.mss.id,self.day,self.period,self.subject)
    
class tbl_itemInfo(models.Model):
    mrpprice=models.IntegerField(null=True,blank=True)
    edition=models.CharField(max_length=100,null=True,blank=True)
    
    def __unicode__(self):
        return u'%s-%s'%(self.id,self.mrpprice)
class tbl_uniqueitemList(models.Model):
    barcodeNo=models.BigIntegerField(null=True,blank=True)
    barcodeImage=models.ImageField(upload_to=djangoUpload,null=True,blank=True)
    info=models.ForeignKey(tbl_itemInfo,null=True,blank=True)
    status=models.BooleanField(default=True)
    remove=models.BooleanField(default=False)
    def getItemId(self):
        return LIBPREFIX+str(self.id)
    def __unicode__(self):
        return u'%s-%s'%(self.id,self.barcodeNo)
    
class tbl_supplier(models.Model):
    name=models.CharField(max_length=100,null=True,blank=True)
    address=models.CharField(max_length=100,null=True,blank=True)
    contact=models.BigIntegerField(null=True,blank=True)
    billamt=models.IntegerField(null=True,blank=True)
    info=models.ForeignKey(tbl_itemInfo,null=True,blank=True)
    date=models.DateField(default=datetime.datetime.today())
    recipt=models.CharField(max_length=25,null=True,blank=True)
    paymentMode=models.CharField(max_length=25,null=True,blank=True)
    quantity=models.IntegerField(null=True,blank=True)
    def __unicode__(self):
        return u'%s-%s'%(self.id,self.name)
    def getdate(self):
        date=self.date
        
        x=datetime.datetime.strptime(str(date), '%Y-%m-%d')
        return x.strftime('%d-%m-%Y')
    def getbillamt(self):
        if self.billamt:
            return self.billamt
        else:
            return '----'
    def getPaymentMode(self):
        if self.paymentMode:
            return self.paymentMode
        else:
            return '----'
    def getrecipt(self):
        if self.recipt:
            return self.recipt
        else:
            return '----'
class tbl_removeLibItems(models.Model):
    ids=models.TextField(null=True,blank=True)
    date=models.DateField(null=True,blank=True)
    remark=models.CharField(max_length="75",null=True,blank=True)
    def getremark(self):
        if self.remark:
            return self.remark
        else:
            return '----'
    def getdate(self):
        date=self.date
        
        x=datetime.datetime.strptime(str(date), '%Y-%m-%d')
        return x.strftime('%d-%m-%Y')
    def __unicode__(self):
        return u'%s-%s'%(self.id,self.ids)
        
class tbl_libItem(models.Model):
    itemName=models.CharField(max_length=100,null=True,blank=True)
    itemCode=models.CharField(max_length=100,null=True,blank=True)
    
    totalquantity=models.ManyToManyField(tbl_uniqueitemList,null=True,blank=True)
    type=models.CharField(max_length='15',null=True,blank=True)
    publisher=models.CharField(max_length=100,null=True,blank=True)
    author=models.CharField(max_length=100,null=True,blank=True)
    
    suppliers=models.ManyToManyField(tbl_supplier,null=True,blank=True)
    remove=models.ManyToManyField(tbl_removeLibItems,null=True,blank=True)
    def __unicode__(self):
        return u'%s-%s-%s'%(self.id,self.itemName,self.itemCode)
    def gettotalquantity(self):
        x=0
        for values in self.remove.all():
            x=x+len(values.ids.split('/')[:-1])
        return len(self.totalquantity.all())-x
    def getedition(self):
        return self.suppliers.all()[0].info.edition
    def getauthor(self):
        return self.author
    def getpublisher(self):
        return self.publisher
    def getmrp(self):
        return self.suppliers.all()[0].info.mrpprice
    def getdate(self):
        date=self.suppliers.all()[0].date
        
        x=datetime.datetime.strptime(str(date), '%Y-%m-%d')
        return x.strftime('%d-%m-%Y')
    def getsuppname(self):
        return self.suppliers.all()[0].name
    def getsuppcontact(self):
        return self.suppliers.all()[0].contact
    def getbillamt(self):
        return self.suppliers.all()[0].billamt
    def getPaymentMode(self):
        return self.suppliers.all()[0].paymentMode
    def getrecipt(self):
        return self.suppliers.all()[0].recipt
    def getaddress(self):
        return self.suppliers.all()[0].address


class tbl_libIssuePeriod(models.Model):
    type=models.CharField(max_length="15",null=True,blank=True)
    days=models.IntegerField(null=True,blank=True)
    def __unicode__(self):
        return u'%s-%s-%s'%(self.id,self.type,self.days)

class tbl_libMember(models.Model):
    personId=models.CharField(max_length="25",null=True,blank=True)
    type=models.CharField(max_length="15",null=True,blank=True)
    image=models.ImageField(upload_to=djangoUpload,null=True,blank=True)
    period=models.ForeignKey(tbl_libIssuePeriod,null=True,blank=True)
    memberTenure=models.IntegerField(null=True,blank=True)
    date=models.DateField(default=datetime.datetime.today())
    isActive=models.BooleanField(default=True)
    def __unicode__(self):
        return u'%s-%s-%s'%(self.id,self.type,self.personId)
    def getPersonName(self):
        if self.type=="student":
            studobj=tbl_student.objects.get(id=int(self.personId[len(STUDENTPREFIX):]))
            return studobj.getName()
        else:
            empobj=tbl_employee.objects.get(id=int(self.personId[len(EMPLOYEE_PREFIX):]))
            return empobj.getEMPName()
    def getPersonAdd(self):
        if self.type=="student":
            studobj=tbl_student.objects.get(id=int(self.personId[len(STUDENTPREFIX):]))
            return studobj.perDetail.lAdd
        else:
            empobj=tbl_employee.objects.get(id=int(self.personId[len(EMPLOYEE_PREFIX):]))
            return empobj.perDetail.lAdd
    def getPersonContact(self):
        if self.type=="student":
            studobj=tbl_student.objects.get(id=int(self.personId[len(STUDENTPREFIX):]))
            return studobj.getContactNo()
        else:
            empobj=tbl_employee.objects.get(id=int(self.personId[len(EMPLOYEE_PREFIX):]))
            return empobj.getEMPContact()
    def getimageurl(self):
        if self.image:
            return uploadFolder+self.image.url
    def getMemberId(self):
        return LIBMEMPREFIX+str(self.id)


class tbl_issueItem(models.Model):
    itemType=models.CharField(max_length=25,null=True,blank=True)
    itemCode=models.CharField(max_length=25,null=True,blank=True)
    itemId=models.CharField(max_length=25,null=True,blank=True)
    personId=models.CharField(max_length=25,null=True,blank=True)
    issueDate=models.DateField(default=datetime.datetime.today())
    expiryDate=models.DateField(default=datetime.datetime.today())
    dateofReturn=models.DateField(null=True,blank=True)
    status=models.CharField(max_length=25,null=True,blank=True)
    
    def __unicode__(self):
        return u'%s-%s-%s'%(self.id,self.itemCode,self.itemId)
    
    def getPersonId(self):
        try:
            return tbl_libMember.objects.get(id=int(self.personId[len(LIBMEMPREFIX):])).personId
        except:
            return None
    def getPersonName(self):
        try:
            memobj=tbl_libMember.objects.get(id=int(self.personId[len(LIBMEMPREFIX):]))
            if memobj.type=='teacher':
                unique=tbl_employee.objects.get(id=int(memobj.personId[len(TEACHER_PREFIX):]))
                return unique.getEMPName()
            if memobj.type=='student':
                unique=tbl_student.objects.get(id=int(memobj.personId[len(STUDENTPREFIX):]))
                return unique.getName()
        except:
            return None
    def getIssueDate(self):
        
        if self.issueDate:
            x=datetime.datetime.strptime(str(self.issueDate), '%Y-%m-%d')
            return x.strftime('%d-%m-%Y')
        else:
            return ''
    def getitemName(self):
        try:
            getrow=tbl_libItem.objects.filter(itemCode=self.itemCode)
            return getrow[0].itemName
        except:
            return None
    def getLastDate(self):
        
        if self.expiryDate:
            x=datetime.datetime.strptime(str(self.expiryDate), '%Y-%m-%d')
            return x.strftime('%d-%m-%Y')
        else:
            return ''
    def getReturnDate(self):
        
        if self.dateofReturn:
            x=datetime.datetime.strptime(str(self.dateofReturn), '%Y-%m-%d')
            return x.strftime('%d-%m-%Y')
        else:
            return ''

class tbl_grades(models.Model):
    name=models.CharField(max_length="15",null=True,blank=True)
    start=models.IntegerField(default=0)
    end=models.IntegerField(default=0)
    def getRange(self):
        if self.start>self.end:
            return str(self.start)+'-'+str(self.end)
        else:
            return str(self.end)+'-'+str(self.start)
        
        

class Notice(models.Model):
    message=models.TextField(null=True,blank=True)
    isActive=models.BooleanField(default=True)
    date=models.DateField(default=datetime.date.today())
    standard=models.ForeignKey(tbl_standard,null=True,blank=True)
    def getDate(self):
        if self.date:
            x=datetime.datetime.strptime(str(self.date), '%Y-%m-%d')
            return x.strftime('%d-%m-%Y')
        else:
            return ''

class tbl_events(models.Model):
    username=models.CharField(max_length=25)
    event=models.TextField(null=True,blank=True)
    startDate=models.DateTimeField(null=True,blank=True)
    endDate=models.DateTimeField(null=True,blank=True)
    fgColor=models.CharField(max_length=10)
    bgColor=models.CharField(max_length=10)
    
    createdOn=models.DateTimeField(default=datetime.datetime.today())
    def __unicode__(self):
        return "%s-%s"%(self.username,self.event)