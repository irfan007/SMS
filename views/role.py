from django.shortcuts import render_to_response
from django.template.context import RequestContext
from App.models import tbl_role, tbl_contentType, tbl_permission, tbl_systemUser
from django.http import HttpResponseRedirect
from views.permission import i_hasPermission



def v_role(req):
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'role','v'):
        roles=tbl_role.objects.filter()
        return render_to_response('roleList.html',locals(),context_instance=RequestContext(req))

 
def v_addRole(req):
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'role','a'):
        
        MAP=[]
        oldcat=None
        for c in tbl_contentType.objects.filter(isActive=True).order_by('category'):
            if c.category==oldcat:
                MAP.append(['',c.name,0,0,0,0])
            else:
                MAP.append([c.category,c.name,0,0,0,0])
                oldcat=c.category
        
        
        if req.POST.get('addRole',''):
            errors=[]
            name=req.POST.get('name',None).strip()
            desc=req.POST.get('desc','').strip()
            active=req.POST.get('active',False)
            
            if not name:
                errors.append("please enter role name !")
            elif name and tbl_role.objects.filter(name=name):
                errors.append("Role with this name already exist !")
            
            for i,row in enumerate(MAP):
                MAP[i][2]=int(req.POST.get(row[1]+'_v',0))
                MAP[i][3]=int(req.POST.get(row[1]+'_a',0))
                MAP[i][4]=int(req.POST.get(row[1]+'_u',0))
                MAP[i][5]=int(req.POST.get(row[1]+'_d',0))
                
                
    #            if not [r for r in MAP if r[2]==1 or r[3]==1 or r[4]==1 or r[5]==1 ]:
    #                errors.append("please check at least one check box !")        
            
            if not errors:
                #return HttpResponse((tbl_systemUser.objects.get(username=req.session['username']).id))
                role=tbl_role.objects.create(name=name,description=desc,assignedBy=(tbl_systemUser.objects.get(username=req.session['username']).id),isActive=bool(active))
                for r in [r for r in MAP if r[2]==1 or r[3]==1 or r[4]==1 or r[5]==1 ]:
                    c=tbl_contentType.objects.get(name=r[1])
                    p=tbl_permission.objects.create(content=c,view=r[2],add=r[3],update=r[4],delete=r[5])
                    role.permissions.add(p)            
                return HttpResponseRedirect('/role')
            return render_to_response('addRole.html',locals(),context_instance=RequestContext(req))
        return render_to_response('addRole.html',locals(),context_instance=RequestContext(req))
            
def v_editRole(req,_id):
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'role','u'):
        
        MAP=[]
        oldcat=None
        roleObj=tbl_role.objects.get(id=_id)
        name=roleObj.name
        desc=roleObj.description
        active=roleObj.isActive
        
        for c in tbl_contentType.objects.filter(isActive=True).order_by('category'):
            if c.category==oldcat:
                v=a=u=d=0
                try:
                    if roleObj.permissions.get(content=tbl_contentType.objects.get(name=c.name)):
                        x=roleObj.permissions.get(content=tbl_contentType.objects.get(name=c.name))
                        v=x.view
                        a=x.add
                        u=x.update
                        d=x.delete
                except:
                    pass
                MAP.append(['',c.name,v,a,u,d])    
            else:
                v=a=u=d=0
                try:
                    if roleObj.permissions.get(content=tbl_contentType.objects.get(name=c.name)):
                        x=roleObj.permissions.get(content=tbl_contentType.objects.get(name=c.name))
                        v=x.view
                        a=x.add
                        u=x.update
                        d=x.delete
                except:
                    pass
                MAP.append([c.category,c.name,v,a,u,d])
                oldcat=c.category
        
        if req.POST.get('editRole',''):
            errors=[]
            name=req.POST.get('name',None).strip()
            desc=req.POST.get('desc','').strip()
            active=req.POST.get('active',False)
            
            if not name:
                errors.append("please enter role name !")
            elif name and name!=roleObj.name and tbl_role.objects.filter(name=name):
                errors.append("Role with this name already exist !")
            else:
                for i,row in enumerate(MAP):
                    MAP[i][2]=int(req.POST.get(row[1]+'_v',0))
                    MAP[i][3]=int(req.POST.get(row[1]+'_a',0))
                    MAP[i][4]=int(req.POST.get(row[1]+'_u',0))
                    MAP[i][5]=int(req.POST.get(row[1]+'_d',0))
                
                
    #            if not [r for r in MAP if r[2]==1 or r[3]==1 or r[4]==1 or r[5]==1 ]:
    #                errors.append("please check at least one check box !")        
            
            if not errors:
                roleObj.name=name
                roleObj.description=desc
                roleObj.isActive=bool(active)
                
                roleObj.permissions.filter(content__isActive=True).delete()
                for r in [r for r in MAP if r[2]==1 or r[3]==1 or r[4]==1 or r[5]==1 ]:
                    c=tbl_contentType.objects.get(name=r[1])
                    p=tbl_permission.objects.create(content=c,view=r[2],add=r[3],update=r[4],delete=r[5])
                    roleObj.permissions.add(p)
                
                roleObj.save()            
                return HttpResponseRedirect('/role')
                #return HttpResponseRedirect('/role/edit/'+str(roleObj.id))
            return render_to_response('editRole.html',locals(),context_instance=RequestContext(req))
        return render_to_response('editRole.html',locals(),context_instance=RequestContext(req))
            
                    