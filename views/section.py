from django.shortcuts import render_to_response, render
from App.models import tbl_class, tbl_systemUser
from django.http import HttpResponseRedirect
from django.http import HttpResponse

from django.template.context import RequestContext
from views.permission import i_hasPermission
def v_section(req):
    '''
    this method is used for listing of various sections in database
    ''' 
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'section','v'): 
        rows=tbl_class.objects.all().order_by('-createdOn')
        errors=[]
        if req.POST.get('addSection',''):
            if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'section','a'):
                '''
                form validation will be carried out
                '''
                name=req.POST.get('name','').strip()
                status=(req.POST.get('status',''))
                checkdup=tbl_class.objects.filter(name=name)
                if not name:
                    errors.append('Please enter the name !')
                if checkdup:
                    errors.append('Please enter different name !')
                if errors:
                    return render_to_response('addSection.html',locals(),context_instance=RequestContext(req))
                '''
                inserting new row  into database table
                '''
                p1=tbl_class()
                
                p1.name=name
                p1.isActive=int(status)
                p1.save()
                return HttpResponseRedirect('/sections/')
            else:
                
                errors.append("You don't have the rights to add the section!")
        return render_to_response('addSection.html',locals(),context_instance=RequestContext(req))

def v_editsection(req,para):
    '''
    this method will carry out editing of section whose id is equal to para
    '''
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'section','u'):
    
        para=int(para)
        
       
        row=tbl_class.objects.get(id=para)
        name=row.name
        status=row.isActive
        rows=tbl_class.objects.all().order_by('-createdOn')
       
        
        if req.POST.get('editsection',''):
            '''
            form validation will be carried out
            '''
            errors=[]
            name=req.POST.get('name','').strip()
            status=int(req.POST.get('status',''))
            if not name:
                errors.append("Please enter the name!")
            existedName=tbl_class.objects.filter(name=name).exclude(id=para)
            if existedName:
                errors.append("Please enter the different section!")
            
            if errors:    
                return render_to_response('editSection.html',locals(),context_instance=RequestContext(req))
            '''
            updating database with new values
            '''
            item=tbl_class.objects.get(id=para)
            item.name=name
            item.isActive=int(status)
            item.save()
            
            return HttpResponseRedirect('/sections/')
        
            
        return render_to_response('editSection.html',locals(),context_instance=RequestContext(req))

