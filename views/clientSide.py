from django.shortcuts import render_to_response
from django.http import HttpResponse
from App.models import tbl_product
from SMS.settings import SECRET_KEY, TRIAL_PERIOD_DAYS


def i_makeHash(strList):
    import hashlib,datetime
    h= hashlib.new('SHA1')
    for x in strList:
        h.update(x)
    return h.hexdigest()



def v_activate(req):
    if req.POST.get("activate"):
        errors=[]
        name=req.POST.get('name')
        contact_no=req.POST.get('contact_no')
        email=req.POST.get('email')
        school_name=req.POST.get('school_name')
        address=req.POST.get('address')
        username=req.POST.get('username')
        pwd=req.POST.get('pwd')
        postfix=SECRET_KEY
        
        
        if not name:
            errors.append('please enter customer name !')
        elif not contact_no:
            errors.append('please enter customer contact no. !')
        elif not email:
            errors.append('please enter customer email ID !')
        elif not school_name:
            errors.append('please enter school Name !')
        elif not address:
            errors.append('please enter address !')
        elif not username:
            errors.append('please enter agent username !')
        elif not pwd:
            errors.append('please enter agent password !')
        else:
            if contact_no:
                try:
                    int(contact_no)
                    if len(contact_no)<10:
                        errors.append('please enter contact no. of valid length !')
                except ValueError:
                    errors.append('please enter valid contact no. !')
            if '@' and '.' not in email:
                errors.append('please enter valid email ID !')
                
                    
        if not errors:
            import httplib
            from django.http import HttpResponse
            host='localhost:8001'
            pre=name.replace(' ','+')+':'+contact_no+':'+email+':'+school_name.replace(' ','+')+':'+address.replace('\r\n','%0D%').replace(' ','+')+':'+username+':'+pwd+':'+postfix
            #return HttpResponse(pre)
            path='/purchase/?activate='+pre
            conn = httplib.HTTPConnection(host)
            conn.request("POST", path)
            data=conn.getresponse().read()
            conn.close()
            #return HttpResponse(str(data))
            if data=='000':
                return HttpResponse('!! ACTIVATION FAILED !!')
            else:
                import datetime
                splitData=data.split(":")
                #return HttpResponse(splitData[3])
                d=splitData[3].split('-')
                tbl_product.objects.create(sid=splitData[0],agent=splitData[1],key=splitData[2],purchaseDate=datetime.date(int(d[0]),int(d[1]),int(d[2])),schoolName=school_name,customerName=name,contactNo=contact_no,address=address,email=email)
                temp='''/
                <script>
                    alert("Your product key has generated ,restart your computer system to activate it.");
                    location.href = '/done/';
                </script>
                '''
                
                return HttpResponse(temp)
            #except Exception,e:
            #    return HttpResponse("ACTIVATION FAILED!")
            
            
            #return HttpResponse(temp)
        return render_to_response("activating.html",locals())
    return render_to_response("activating.html")


def v_trial(req):
    '''
    trial key can be same for different user if they have same secret_key version of settings.py and purchase date 
    '''
    
    if not tbl_product.objects.filter(id=1):
        import datetime
        trialproduct=tbl_product.objects.create(sid=0,agent=0,purchaseDate=datetime.date.today(),expireDate=datetime.date.today()+datetime.timedelta(days=TRIAL_PERIOD_DAYS))
        hashKey=i_makeHash([str(0),str(0),str(trialproduct.purchaseDate),str(trialproduct.expireDate),SECRET_KEY])
        trialproduct.key=hashKey
        trialproduct.save()
        temp='''
        <script>
            alert("Your trial key has generated ,restart your computer system to activate it.");
            location.href = '/done/';
        </script>
        '''
        return HttpResponse(temp)
    else:
        temp='''
        <script>
            alert("Your trial key has expired .");
            location.href = '/done/';
        </script>
        '''
        return HttpResponse(temp)
