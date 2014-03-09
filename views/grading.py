from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

from django.http import HttpResponse
from App.models import tbl_grades, tbl_systemUser


from django.template.context import RequestContext
from views.permission import i_hasPermission
def getrange():
    '''
    this will return overall range of grades added in database
    '''
    overall=[]
    data=tbl_grades.objects.all()
    for v in data:
        if v.end<v.start:
            
            list1=range(v.end,v.start)
        else:
            list1=range(v.start,v.end)
        
        for x in list1:
            overall.append(x)
    return overall
def v_grading(req):
    '''
    this method helps to show listing of grading
    '''
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'grades','v'):
        allrows=tbl_grades.objects.filter().order_by('-start')
        return render_to_response('grading.html',locals(),context_instance=RequestContext(req))
def v_addGrades(req):
    '''
    this will add new grades to database
    '''
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'grades','a'): 
        getlength=1
        temp=[]
        overall=[]
        errors=[]
        checkrange=getrange()
        if req.POST.get('addGrade',''):
            '''
            accessing form elements and validating them all
            '''
            getBack=True
            getlength=int(req.POST.get('getlength',''))
            
            i=1
            while(i<=getlength):
                '''
                Loop will help to access and add many grades at a single time
                '''
                temp=[]
                grade=req.POST.get('grade'+str(i),'').strip()
                startrange=req.POST.get('startrange'+str(i),'').strip()
                endrange=req.POST.get('endrange'+str(i),'').strip()
                
                if not grade:
                    errors.append("Please enter the grade")
                if grade:
                    data=tbl_grades.objects.filter(name=grade)
                    if data:
                        errors.append("Grade %s already exist"% grade)
                    
                        
            
                if not startrange or not endrange:
                    errors.append("Please specify all the percentages correctly")
                try:
                    startrange=int(startrange)
                    endrange=int(endrange)
                except:
                    errors.append("Please specify all the percentages correctly")
                temp.append(grade)
                temp.append(startrange)
                temp.append(endrange)
                overall.append(temp)
                i=i+1
            errors=set(errors)
            if errors:
                return render_to_response('addGrades.html',locals(),context_instance=RequestContext(req))
            errors=[]
            for data in overall:
                if int(data[1])>int(data[2]):
                    listing=range(data[2],data[1])
                else:
                    listing=range(data[1],data[2])
                for v in listing:
                    if v in checkrange:
                        errors.append("Invalid grading system!")
                    else:
                        checkrange.append(v)
            errors=set(errors)
            if errors:
                return render_to_response('addGrades.html',locals(),context_instance=RequestContext(req))
            errors=[]
            i=0
            while(i<=99):
                if i in checkrange:
                    pass
                else:
                    errors.append('Invalid grading system!')
                    break
                i=i+1
            
            errors=set(errors)
            if errors:
                return render_to_response('addGrades.html',locals(),context_instance=RequestContext(req))
            for data in overall:
                '''
                adding new grades to database
                '''
                p1=tbl_grades()
                if data[1]>data[2]:
                    p1.name=data[0]
                    p1.start=data[1]
                    p1.end=data[2]
                    p1.save()
                else:
                    p1.name=data[0]
                    p1.start=data[2]
                    p1.end=data[1]
                    p1.save()
                
            
            return HttpResponseRedirect('/grading/')
        return render_to_response('addGrades.html',locals(),context_instance=RequestContext(req))
def v_editGrades(req):
    '''
    this will help to edit  all the grades present in database.We can edit all at single time only 
    '''
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'grades','u'): 
        allrows=tbl_grades.objects.filter().order_by('-start')
        errors=[]
        temp=[]
        overall=[]
        checkrange=[]
        if req.POST.get('editGrade',''):
            
            i=1
            for data in allrows:
                temp=[]
                grade=req.POST.get('grade'+str(data.id),'').strip()
                startrange=req.POST.get('startrange'+str(data.id),'').strip()
                endrange=req.POST.get('endrange'+str(data.id),'').strip()
                
                if not grade:
                    errors.append("Please enter the grade")
                if grade:
                    dup=tbl_grades.objects.filter(name=grade).exclude(id=data.id)
                    if dup:
                        errors.append("Grade %s already exist"% grade)
                    
                        
            
                if not startrange or not endrange:
                    errors.append("Please specify all the percentages correctly")
                try:
                    startrange=int(startrange)
                    endrange=int(endrange)
                except:
                    errors.append("Please specify all the percentages correctly")
                temp.append(grade)
                temp.append(startrange)
                temp.append(endrange)
                temp.append(data.id)
                overall.append(temp)
                i=i+1
            errors=set(errors)
            if errors:
                return render_to_response('editGrades.html',locals(),context_instance=RequestContext(req))
            errors=[]
            for data in overall:
                if int(data[1])>int(data[2]):
                    listing=range(data[2],data[1])
                else:
                    listing=range(data[1],data[2])
                for v in listing:
                    if v in checkrange:
                        errors.append("Invalid grading system!")
                    else:
                        checkrange.append(v)
            errors=set(errors)
            if errors:
                return render_to_response('editGrades.html',locals(),context_instance=RequestContext(req))
            errors=[]
            i=0
            while(i<=99):
                if i in checkrange:
                    pass
                else:
                    
                    errors.append('Invalid grading system!')
                    break
                i=i+1    
            errors=set(errors)
            if errors:
                return render_to_response('editGrades.html',locals(),context_instance=RequestContext(req))
            for data in overall:
                gradeobj=tbl_grades.objects.get(id=data[3])
                
                if data[1]>data[2]:
                    gradeobj.name=data[0]
                    gradeobj.start=data[1]
                    gradeobj.end=data[2]
                    gradeobj.save()
                else:
                    gradeobj.name=data[0]
                    gradeobj.start=data[2]
                    gradeobj.end=data[1]
                    gradeobj.save()
                
            
            return HttpResponseRedirect('/grading/')
        return render_to_response('editGrades.html',locals(),context_instance=RequestContext(req))
            
        
    