from SMS.settings import  MEDIA_ROOT
from App.models import tbl_systemUser

def i_upload(file_,subDirectory,name):
    import os
    try:
        with open(MEDIA_ROOT+subDirectory+'/'+str(name), 'w') as destination:
            for chunk in file_.chunks():
                destination.write(chunk)
        return subDirectory+'/'+name
    except IOError:
        if not os.path.exists(MEDIA_ROOT+subDirectory):
            os.makedirs(MEDIA_ROOT+subDirectory)
        with open(MEDIA_ROOT+subDirectory+'/'+str(name), 'w') as destination:
            for chunk in file_.chunks():
                destination.write(chunk)
        return subDirectory+'/'+name
    
def i_getUser(pkid):
    try:
        return tbl_systemUser.objects.get(id=pkid)
    except:
        return None



def i_decompose(strList):
    import hashlib
    h= hashlib.new('SHA1')
    for x in strList:
        h.update(x)
    return h.hexdigest()
#
#
#def i_hasPermission(forEmployee,forContent,type='v'):
#    
#    '''
#    
#    * if user not exist it will return false 
#    * if content not exist it will return false
#    * if type not exist it will return false
#     
#    type can be
#    
#    for view:type='v'
#    for add:type='a'
#    for update:type='u'
#    for delete:type='d'
#    
#    default type is 'v'
#    '''
#    if not forEmployee:
#        return False
#    elif forEmployee.isAdmin:
#        return True
#    elif type=='v':
#        try:
#            return forEmployee.role.permissions.get(content=forContent).view
#        except tbl_permission.DoesNotExist:
#            return False
#    elif type=='a':
#        try:
#            return forEmployee.role.permissions.get(content=forContent).add
#        except tbl_permission.DoesNotExist:
#            return False
#    elif type=='u':
#        try:
#            return forEmployee.role.permissions.get(content=forContent).update
#        except tbl_permission.DoesNotExist:
#            return False
#    elif type=='d':
#        try:
#            return forEmployee.role.permissions.get(content=forContent).delete
#        except tbl_permission.DoesNotExist:
#            return False
#    else:
#        return False