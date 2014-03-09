from django.shortcuts import render_to_response, render
from App.models import tbl_subject, tbl_shortstandard, tbl_medium, tbl_standard,\
    tbl_systemUser
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.template.context import RequestContext
from views.permission import i_hasPermission
def v_subject(req):
    '''
    this method will carry out listing of subjects
    '''
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'subject','v'): 
        rows=tbl_subject.objects.all().order_by('createdOn')
        return render_to_response('subject.html',locals(),context_instance=RequestContext(req))
def v_addsubject(req):
    '''
    this method will add new subjects to database
    '''
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'subject','a'):
        errors=[]
        shortstandards=tbl_shortstandard.objects.filter()
        mediums=tbl_medium.objects.filter(isActive=True)
        getlength=1
        temp=[]
        overall=[]
        if req.POST.get('addSubject',''):
            getBack=True
            
            getlength=int(req.POST.get('getlength',''))
            
            i=1
            while i<=getlength:
                '''
                form validation will be carried out.
                '''
                temp=[]
                name=req.POST.get('subject'+str(i),'').strip()
                medium=req.POST.getlist('medium'+str(i),'')
                if medium:
                    medium=[int(data) for data in medium]
                fromStandard=int(req.POST.get('fromStandard'+str(i),''))
                toStandard=int(req.POST.get('toStandard'+str(i),''))
                
                checkdup=tbl_subject.objects.filter(name=name)
                if not name:
                    errors.append('Please enter subject name !')
                if checkdup:
                    errors.append('Please enter different name.Subject name %s already exists !'%(name))
                if not medium:
                    errors.append("Please select atleast 1 medium")
                if fromStandard==-1:
                    errors.append("Please select From Standard!")
                    
                if toStandard==-1:
                    errors.append("Please select To Standard!")
                    
                if medium==-1:
                    errors.append("Please select the medium!")
                temp.append(name)
                temp.append(medium)
                temp.append(fromStandard)
                temp.append(toStandard)
                overall.append(temp)
                i=i+1
            errors=set(errors)
            if errors:
                return render_to_response('addSubject.html',locals(),context_instance=RequestContext(req))
            errors=[]
            for t in overall:
                     
                stand=range(t[2],t[3]+1)
                listing=[]
                for data in stand:
                    uniq=tbl_shortstandard.objects.get(id=data)
                    
                    for m in t[1]:
                        
                        med=tbl_medium.objects.get(id=m)
                    
                        validation=tbl_standard.objects.filter(medium=med,name=uniq.name)
                    
                        if not validation:
                            errors.append("Please select valid medium and standards")
                            return render_to_response("addSubject.html",locals(),context_instance=RequestContext(req))
                        listing.append(validation[0].id)
                '''
                this will add new row to database table i.e tbl_subject
                '''
            
                p1=tbl_subject()
            
                p1.name=t[0]
                p1.start=t[2]
                p1.end=t[3]
                p1.save()
                for l in listing:
                    obj=tbl_standard.objects.get(id=l)
                    p1.standards.add(obj)
                
                    p1.save()
            return HttpResponseRedirect('/subjects/')
            
            
        return render_to_response('addSubject.html',locals(),context_instance=RequestContext(req))
def v_editsubject(req,para):
    '''
    this method is used for viewing/updating the row of subject table whose id equal to para
    '''
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'subject','u'):
        para=int(para)
        uniquerow=tbl_subject.objects.get(id=para)
        name=uniquerow.name
        getmedstandards=uniquerow.standards.all()
        fromStandard=uniquerow.start
        toStandard=uniquerow.end
        shortstandards=tbl_shortstandard.objects.all()
        abc=getmedstandards.values('medium').distinct()
        getmediums=[]
        mediums=tbl_medium.objects.filter(isActive=True)
        for item in abc:
            for data in mediums:
                if data.id==item['medium']:
                    getmediums.append(data.id)
                    
        
             
        if req.POST.get('editsubject',''):
            '''
            performing form validation
            ''' 
            errors=[]
            name=req.POST.get('name','').strip()
            if not name:
                errors.append("Please enter the name!")
            existedName=tbl_subject.objects.filter(name=name).exclude(id=para)
            if existedName:
                errors.append("Please enter the different subject!")
            if errors:    
                return render_to_response('editSubject.html',locals(),context_instance=RequestContext(req))
            
            getmediums=[]
            
            getmediums=req.POST.getlist('getmediums','')
            getmediums=[int(data) for data in getmediums]
            fromStandard=int(req.POST.get('fromStandard',''))
            toStandard=int(req.POST.get('toStandard',''))
            
            
            
            
            if errors:
                return render_to_response('editSubject.html',locals(),context_instance=RequestContext(req))
            if fromStandard==-1:
                errors.append("Please select from: standard!")
                return render_to_response('editSubject.html',locals(),context_instance=RequestContext(req))
            if toStandard==-1:
                errors.append("Please select to: standard!")
                return render_to_response('editSubject.html',locals(),context_instance=RequestContext(req))
            if len(getmediums)<1:
                errors.append("Please select the medium!")
                return render_to_response('editSubject.html',locals(),context_instance=RequestContext(req))
                
            stand=range(fromStandard,toStandard+1)
            
            listing=[]
            for data in stand:
                uniq=tbl_shortstandard.objects.get(id=data)
                
                for m in getmediums:
                    med=tbl_medium.objects.get(id=m)
                    
                    validation=tbl_standard.objects.filter(medium=med,name=uniq.name)
                    
                    if not validation:
                        errors.append("Please select valid medium and standards")
                        return render_to_response('editSubject.html',locals(),context_instance=RequestContext(req))
                    listing.append(validation[0].id)
            '''
            finally updating the database with new values
            '''
            uniquerow.standards=[]
            
            uniquerow.name=name
            uniquerow.start=fromStandard
            uniquerow.end=toStandard
            uniquerow.save()
            
            for data in listing:
                obj=tbl_standard.objects.get(id=data)
                uniquerow.standards.add(obj)
                
            uniquerow.save()
            
           
            
            return HttpResponseRedirect('/subjects/')
        
        return render_to_response('editSubject.html',locals(),context_instance=RequestContext(req))

