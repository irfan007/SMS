from django.shortcuts import render_to_response, render
from App.models import tbl_medium, tbl_systemUser
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.template.context import RequestContext


from django.template.context import RequestContext
from views.permission import i_hasPermission
def v_medium(req):
    '''
    this will help to add new medium and also to show listing of mediums.
    '''
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'medium','v'): 
        errors=[]
        rows=tbl_medium.objects.all().order_by('-createdOn') #accessing all row from database to show listing of mediums
        if req.POST.get('addMedium',''):
            if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'medium','a'):
                '''
                form validation will be carried out
                '''
                name=req.POST.get('name','').strip()
                status=(req.POST.get('status',''))
                checkdup=tbl_medium.objects.filter(name=name)
                if not name:
                    errors.append('Please enter the name !')
                if checkdup:
                    errors.append('Please enter different name !')
                if errors:
                    return render_to_response('addMedium.html',locals(),context_instance=RequestContext(req))
                '''
                inserting new medium into database
                '''
                p1=tbl_medium()
                
                p1.name=name
                p1.isActive=int(status)
                p1.save()
                return HttpResponseRedirect('/mediums/')
            else:
                errors.append("You don't have the rights to add the medium!")
        return render_to_response('addMedium.html',locals(),context_instance=RequestContext(req))


def v_editMedium(req,para):
    '''
    this method will carry out editing of medium whose id is equal to para
    '''
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'medium','u'):
        para=int(para)
        
       
        row=tbl_medium.objects.get(id=para)
        name=row.name
        status=row.isActive
        rows=tbl_medium.objects.all().order_by('-createdOn')
        #return HttpResponse(status) 
        if req.POST.get('editMedium',''):
            '''
            form validation will be carried out
            '''
            errors=[]
            name=req.POST.get('name','').strip()
            status=int(req.POST.get('status',''))
            if not name:
                errors.append("Please enter the name!")
            existedName=tbl_medium.objects.filter(name=name).exclude(id=para)
            if existedName:
                errors.append("Please enter the different medium!")
            
            if errors:    
                return render_to_response('editMedium.html',locals(),context_instance=RequestContext(req))
            '''
            updating database with new values
            '''
            item=tbl_medium.objects.get(id=para)
            item.name=name
            item.isActive=int(status)
            item.save()
            
            return HttpResponseRedirect('/mediums/')
        
            
            
            
        return render_to_response('editMedium.html',locals(),context_instance=RequestContext(req))
    
