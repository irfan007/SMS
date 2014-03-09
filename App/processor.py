from App.models import tbl_systemUser, Notice, tbl_school

def currentUser(req):
    share={}
    defaultURL={
                  'role':'/role/',
                  'user':'/user/',
                  'setting':'/school/add/',
                  'staff':'/staff/',
                  'medium':'/mediums/',
                  'section':'/sections/',
                  'standard':'/standards/',
                  'subject':'/subjects/',
                  'holiday':'/holidays/',
                  'grades':'/grading/',
                  'exam':'/examType/',
                  
    }
    try:
        if req.session.get('username'):
            cu=tbl_systemUser.objects.get(username=req.session['username'])
            share['CU']=cu
            
            if cu.isAdmin:
                share['isAdmin']=True
                share['config']=True
                share['config_default_url']=defaultURL['user']
                
                share['allNotice']=Notice.objects.filter(isActive=True)
                try:
                    share['schoolTitle']=tbl_school.objects.all()[0].name
                except:
                    pass
            
            else:
                cuper={}
                for p in cu.role.permissions.all():
                    perm={}
                    if p.view:
                        perm['v']=True
                    if p.add:
                        perm['a']=True    
                    if p.update:
                        perm['u']=True
                    if p.delete:
                        perm['d']=True
                    cuper[p.content.name]=perm
                share['CUP']=cuper
                share['allNotice']=Notice.objects.filter(isActive=True)
                config=['role','user','staff','medium','section','standard','subject','holiday','setting','grades','exam']
                anyConfig=[key for key in share['CUP'].iterkeys() if key in config]
                if anyConfig:
                    share['config']=True
                    share['config_default_url']=defaultURL[anyConfig[0]]
                    
                
                try:
                    share['schoolTitle']=tbl_school.objects.all()[0].name
                except:
                    pass
    except:
        pass
    
    
    
    return share
        
