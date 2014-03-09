from django.shortcuts import render_to_response
from App.models import tbl_school, tbl_location, tbl_medium, tbl_systemUser
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from SMS.settings import schoolUDir, MEDIA_ROOT, uploadFolder
from views.student import dateformatConvertor
from django.template.context import RequestContext
from views.permission import i_hasPermission
def v_school(req):
    '''
    this method will help to view or add school details
    '''
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'setting','v'): 
        schoolobj=tbl_school.objects.filter()
        if not schoolobj:
            return HttpResponseRedirect('/school/add/')
        image=schoolobj[0].getimageurl()
        image=uploadFolder+image
        return render_to_response('school.html',locals(),context_instance=RequestContext(req))
def v_addSchool(req):
    '''
    this method will help to add school details
    '''
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'setting','a'):
        medLength=1
        states=tbl_location.objects.filter(pid=1).order_by('name')
        months=['jan','feb','mar','apr','may','june','july','aug','sept','oct','nov','dec']
        errors=[]
        if req.POST.get('addSchool',''):
            '''
            performing form validation 
            '''
            getBack=True
            
            temp=[]
            
            medLength=int(req.POST.get('getMedLength',''))
            name=req.POST.get('name','').strip()
            board=req.POST.get('board1','').strip()
            startsession=req.POST.get('startsession','')
            endsession=req.POST.get('endsession','')
            
            #return HttpResponse(startsession+endsession)
            address=req.POST.get('address','').strip()
            contact=req.POST.get('contact','').strip()
            
            i=1
            while(i<=medLength):
                data=req.POST.get('medium'+str(i),'').strip()
                
                temp.append(data)
                i=i+1
            if not name:
                errors.append("Please enter the name!")
            try:
                startsession=int(startsession)
                endsession=int(endsession)
            except:
                errors.append("Please select the starting and ending month of session!")
                return render_to_response('addschoolinfo.html',locals(),context_instance=RequestContext(req))
            if not address:
                errors.append("Please enter the address!")
            if len(contact)<6:
                errors.append("Please enter the valid contact no!")
                return render_to_response('addschoolinfo.html',locals(),context_instance=RequestContext(req))
            try:
                contact=int(contact)
            except:
                errors.append("Please enter the valid contact no!")
                return render_to_response('addschoolinfo.html',locals(),context_instance=RequestContext(req))
            
                
            if errors:
                return render_to_response('addschoolinfo.html',locals(),context_instance=RequestContext(req))
                
            getlstate=int(req.POST.get('lstate',''))
            
            
            lcities=tbl_location.objects.filter(pid=getlstate).order_by('name')
            getlcity=int(req.POST.get('lcity',''))
            if getlstate==-1:
                errors.append("Please select the state!")
                return render_to_response('addschoolinfo.html',locals(),context_instance=RequestContext(req))
            if getlcity==-1:
                errors.append("Please select the city!")
                return render_to_response('addschoolinfo.html',locals(),context_instance=RequestContext(req))
            website=req.POST.get('website','').strip()
            amount=req.POST.get('amount','').strip()
            if amount:
                try:
                    amount=int(amount)
                except:
                    errors.append("Please enter the valid amount")
                    return render_to_response('addschoolinfo.html',locals(),context_instance=RequestContext(req))
            
            date1=req.POST.get('date1','').strip()
             
            paymode=req.POST.get('paymode','')
            bank=req.POST.get('bank','').strip()
            chequeno=req.POST.get('chequeno','').strip()
            chequedate=req.POST.get('chequedate','')
           
            reciptno=req.POST.get('reciptno','').strip()
            if date1:
                try:
                    date=dateformatConvertor(date1)
                except:
                    errors.append("Please enter valid date in payment details ")
                    return render_to_response('addschoolinfo.html',locals(),context_instance=RequestContext(req))
            if chequedate:
                try:
                    chequedate1=dateformatConvertor(chequedate)
                except:
                    errors.append("Please enter the valid date in payment sections")
                    return render_to_response('addschoolinfo.html',locals(),context_instance=RequestContext(req))
            
            if amount:
                if not date1:
                    errors.append("Please enter date in payment details")
                    return render_to_response('addschoolinfo.html',locals(),context_instance=RequestContext(req))
                if paymode=="-1":
                    errors.append("Please select payment mode in payment details")
                    return render_to_response('addschoolinfo.html',locals(),context_instance=RequestContext(req))
                if not reciptno:
                    errors.append("Please enter recipt no in payment details")
                    return render_to_response('addschoolinfo.html',locals(),context_instance=RequestContext(req))
                if paymode=='chq':
                    if not chequeno:
                        errors.append("Please enter the cheque no in payment details")
                        return render_to_response('addschoolinfo.html',locals(),context_instance=RequestContext(req))
                if paymode=='d':
                    if not chequeno:
                        errors.append("Please enter the draft no in payment details")
                        return render_to_response('addschoolinfo.html',locals(),context_instance=RequestContext(req))
                    
                
            if errors:
                return render_to_response('addschoolinfo.html',locals(),context_instance=RequestContext(req))
            
                    
            '''
            adding new record to database table
            '''
            session1={}
            session1['startsession']=startsession
            session1['endsession']=endsession
            
            p1=tbl_school()
            p1.name=name
            p1.address=address
            p1.city=tbl_location.objects.get(id=getlcity)
            p1.affiliatedBy=board
            p1.contactNo=contact
            p1.session1=str(session1)
            
            p1.website=website
            p1.paymode=paymode
            for data in temp:
                #return HttpResponse(data)
                if len(str(data))>=1:
                    getmedlist=tbl_medium.objects.filter(name=data)
                    if not getmedlist:
                        p3=tbl_medium()
                        p3.name=data
                        p3.isActive=True
                        p3.save()
            if amount:
                p1.amount=amount
            
            p1.reciptno=reciptno
            p1.bankname=bank
            p1.chequeno=chequeno
            if date1:
                p1.paydate=date
            if chequedate:
                
                p1.chequedate=chequedate1
            
            
            if req.FILES.get('logoImage',''):
            
                imagePath=uploadlogo(req.FILES['logoImage'])
                
                p1.logoImage=imagePath
                
            p1.save()    
            return HttpResponseRedirect('/school/')
        return render_to_response('addschoolinfo.html',locals(),context_instance=RequestContext(req))

def uploadlogo(fileObj):
    '''
    help to upload school logo
    '''
    import os
    subDirectory=schoolUDir
    try:
        with open(MEDIA_ROOT+subDirectory+'/'+'school'+".jpeg", 'w') as destination:
            for chunk in fileObj.chunks():
                destination.write(chunk)
        return subDirectory+'/'+'school'+'.jpeg'
    except IOError:
        if not os.path.exists(MEDIA_ROOT+subDirectory):
            os.makedirs(MEDIA_ROOT+subDirectory)
        
        with open(MEDIA_ROOT+subDirectory+'/'+'school'+".jpeg", 'w') as destination:
            for chunk in fileObj.chunks():
                destination.write(chunk)
        return subDirectory+'/'+'school'+'.jpeg'
def v_editSchool(req,para):
    '''
    will help to display/update school information
    '''
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'setting','u'):
        months=['jan','feb','mar','apr','may','june','july','aug','sept','oct','nov','dec']
        para=int(para)
        schoolobj=tbl_school.objects.get(id=para)
        name=schoolobj.name
        address=schoolobj.address
        getlcity=schoolobj.city.id
        states=tbl_location.objects.filter(pid=1).order_by('name')
        getlstate=schoolobj.city.pid
        lcities=tbl_location.objects.filter(pid=getlstate).order_by('name')
        contact=schoolobj.contactNo
        board1=schoolobj.affiliatedBy
        website=schoolobj.website
        getPayDate=schoolobj.getPayDate()
        amount=schoolobj.amount
        paymode=schoolobj.getPaymentMode()
        bank=schoolobj.bankname
        session1=schoolobj.session1
        sessiondict=eval(session1)
        startsession=sessiondict['startsession']
        endsession=sessiondict['endsession']
        
        
        reciptno=schoolobj.reciptno
        chequeno=schoolobj.chequeno
        chequedate=schoolobj.getChequeDate()
        errors=[]
        if req.POST.get('editSchool',''):
            '''
            performing form validation and accessing different values
            '''
            name=req.POST.get('name','').strip()
            address=req.POST.get('address','').strip()
            board1=req.POST.get('board1','').strip()
            startsession=req.POST.get('startsession','')
            endsession=req.POST.get('endsession','')
            contact=req.POST.get('contact','').strip()
            getlstate=int(req.POST.get('lstate',''))
            website=req.POST.get('website','').strip()
            
            lcities=tbl_location.objects.filter(pid=getlstate).order_by('name')
            getlcity=int(req.POST.get('lcity',''))
            if not name:
                errors.append("Please enter the name!")
            try:
                startsession=int(startsession)
                endsession=int(endsession)
            except:
                errors.append("Please select the starting and ending month of session!")
                return render_to_response('editschoolinfo.html',locals(),context_instance=RequestContext(req))
            if not address:
                errors.append("Please enter the address!")
            if len(contact)<6:
                errors.append("Please enter the valid contact no!")
                return render_to_response('editschoolinfo.html',locals(),context_instance=RequestContext(req))
            try:
                contact=int(contact)
            except:
                errors.append("Please enter the valid contact no!")
                return render_to_response('editschoolinfo.html',locals(),context_instance=RequestContext(req))
            
                
            if errors:
                return render_to_response('editschoolinfo.html',locals(),context_instance=RequestContext(req))
                
            
            if getlstate==-1:
                errors.append("Please select the state!")
                return render_to_response('editschoolinfo.html',locals(),context_instance=RequestContext(req))
            if getlcity==-1:
                errors.append("Please select the city!")
                return render_to_response('editschoolinfo.html',locals(),context_instance=RequestContext(req))
            '''
            updating row with new values
            '''
            session1={}
            session1['startsession']=startsession
            session1['endsession']=endsession 
            schoolobj.name=name
            schoolobj.address=address
            schoolobj.website=website
            schoolobj.affiliatedBy=board1
            schoolobj.session1=str(session1)
            schoolobj.city=tbl_location.objects.get(id=getlcity)
            schoolobj.contactNo=contact
            
            if req.FILES.get('logoImage',''):
            
                imagePath=uploadlogo(req.FILES['logoImage'])
                
                schoolobj.logoImage=imagePath
            schoolobj.save()    
            return HttpResponseRedirect('/school/')
            
        return render_to_response('editschoolinfo.html',locals(),context_instance=RequestContext(req))
    