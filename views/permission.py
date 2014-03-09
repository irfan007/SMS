from App.models import tbl_permission, tbl_contentType

def i_hasPermission(forEmployee,forContent,ofType='v'):
    
    '''
    
    * if user not exist it will return false 
    * if content not exist it will return false
    * if ofType not exist it will return false
     
    ofType can be
    
    for view:ofType='v'
    for add:ofType='a'
    for update:ofType='u'
    for delete:ofType='d'
    
    default ofType is 'v'
    '''
    
    
    if not forEmployee:
        return False
    elif forEmployee.isAdmin:
        return True
    
    
    permissionQuerySet=forEmployee.role.permissions
    try:
        forContent=tbl_contentType.objects.get(name=forContent)
    except:
        forContent=None
        
        
    if ofType=='v':
        try:
            return permissionQuerySet.get(content=forContent).view
        except tbl_permission.DoesNotExist:
            return False
    elif ofType=='a':
        try:
            return permissionQuerySet.get(content=forContent).add
        except tbl_permission.DoesNotExist:
            return False
    elif ofType=='u':
        try:
            return permissionQuerySet.get(content=forContent).update
        except tbl_permission.DoesNotExist:
            return False
    elif ofType=='d':
        try:
            return permissionQuerySet.get(content=forContent).delete
        except tbl_permission.DoesNotExist:
            return False
    else:
        return False

#su=tbl_systemUser.objects.get(id=2)
#
#print i_hasPermission(su,'user','u')