#This file is created for library management system of school
from django.shortcuts import render_to_response
from App.models import tbl_student,\
    tbl_employee, tbl_libItem, tbl_supplier, tbl_itemInfo, tbl_uniqueitemList,\
    tbl_libIssuePeriod, tbl_libMember, tbl_issueItem, tbl_removeLibItems,\
    tbl_systemUser
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from views.student import dateformatConvertor, dateformatReverse,\
    getvalidstudent
from SMS.settings import STUDENTPREFIX, EMPLOYEE_PREFIX, manavPageParameter,\
    LibUDir, MEDIA_ROOT, LIBPREFIX, LIBMEMPREFIX
import datetime
import os
import barcode
from barcode.writer import ImageWriter
from django.utils.dateformat import DateFormat    
    

from django.template.context import RequestContext
from views.permission import i_hasPermission

def getvalidemployee(empid):
    prefix=empid[:len(EMPLOYEE_PREFIX)]
    if prefix.upper()==EMPLOYEE_PREFIX:
        try:
            getid=int(empid[len(EMPLOYEE_PREFIX):])
            uniqueobj=tbl_employee.objects.get(id=getid)
            return uniqueobj 
        except:
            return None





def v_libItems(req):#this method is used for listing of items present in school library
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'library','v'):
   
        allrows=tbl_libItem.objects.filter()
        pagination_parameter=manavPageParameter    #Used for next and previous (i.e pagination)
        
        NEXT=False
        totalRows=len(allrows)
        TO=len(allrows)
        if len(allrows)>pagination_parameter:
            TO=pagination_parameter
            NEXT=True
        FROM=1
        allrows=allrows[:pagination_parameter]
        
        
        
        return render_to_response('libItems.html',locals(),context_instance=RequestContext(req))

def v_NextlibItems(req,para):# this method helps to access next rows from database
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'library','v'):
        para=int(para)
        FROM=para+1
        pagination_parameter=manavPageParameter
        
        pagination_parameter=pagination_parameter+para
        
        allrows=tbl_libItem.objects.filter()
        totalRows=len(allrows)
        NEXT=False
        TO=len(allrows)
        if len(allrows)>pagination_parameter:
            TO=pagination_parameter
            NEXT=True
        allrows=allrows[para:pagination_parameter]
        PREV="True"
        back=para
        return render_to_response('libItems.html',locals(),context_instance=RequestContext(req))
    
def v_PrevlibItems(req,para):# this method helps to access previous rows from database
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'library','v'):
        para=int(para)
        TO=para
        pagination_parameter=manavPageParameter
        back=para-pagination_parameter
        
        allrows=tbl_libItem.objects.filter()
        totalRows=len(allrows)
        NEXT=False
        FROM=back+1
        if len(allrows)>back:
            NEXT=True
        allrows=allrows[back:para]
        if back==0:
            PREV=False
        else:
            PREV=True
        
        return render_to_response('libItems.html',locals(),context_instance=RequestContext(req))
def v_addLibItem(req):# this method helps to purchase new item from supplier
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'library','a'):
        listitem=['Book','CD-DVD','Magazine','Other']
        paymodelist=['Cash','Draft','Cheque']
        errors=[]
        if req.POST.get('addLibItem',''):# accessing form elements and performing validation on them
            itemname=req.POST.get('itemname','').strip()
            itemcode=req.POST.get('itemcode','').strip()
            itemtype=req.POST.get('itemtype','')
            quantity=req.POST.get('quantity','').strip()
            edition=req.POST.get('edition','').strip()
            author=req.POST.get('author','').strip()
            publication=req.POST.get('publication','').strip()
            price=req.POST.get('price','').strip()
            suppliername=req.POST.get('suppliername','').strip()
            suppliercontact=req.POST.get('suppliercontact','').strip()
            supplieraddress=req.POST.get('supplieraddress','').strip()
            totalcost=req.POST.get('totalcost','').strip()
            paymentmode=req.POST.get('paymentmode','')
            date=req.POST.get('date','').strip()
            reciptno=req.POST.get('reciptno','').strip()
            donor=req.POST.get('donor','')
            if not itemname:
                errors.append("Please enter the item name!")
                return render_to_response('addLibItem.html',locals(),context_instance=RequestContext(req))
            if not itemcode:
                errors.append("Please enter the code!")
                return render_to_response('addLibItem.html',locals(),context_instance=RequestContext(req))
            try:
                quantity=int(quantity)
            except:
                errors.append("Please enter the valid quantity!")
                return render_to_response('addLibItem.html',locals(),context_instance=RequestContext(req))
            if not price:
                errors.append("Please enter the price!")
                return render_to_response('addLibItem.html',locals(),context_instance=RequestContext(req))
            try:
                date1=dateformatConvertor(date)
            except:
                errors.append("Please enter the valid date !")
                return render_to_response('addLibItem.html',locals(),context_instance=RequestContext(req))
            if quantity>500:
                
                errors.append("You can add maximum of 500 items at a time !")
                return render_to_response('addLibItem.html',locals(),context_instance=RequestContext(req))
            if not suppliername:
                errors.append("Please enter the supplier name!")
                return render_to_response('addLibItem.html',locals(),context_instance=RequestContext(req))
            if tbl_libItem.objects.filter(itemCode=itemcode):
                errors.append("Please enter different code.This code already exist!")
                return render_to_response('addLibItem.html',locals(),context_instance=RequestContext(req))
            
            if quantity==0:
                errors.append("Quantity cannot be 0!")
                return render_to_response('addLibItem.html',locals(),context_instance=RequestContext(req))
            if suppliercontact:
                if len(suppliercontact)<6:
                    errors.append("Please enter valid supplier ContactNo!")
                    return render_to_response('addLibItem.html',locals(),context_instance=RequestContext(req))
            price=int(price)
    
            if suppliercontact:
                suppliercontact=int(suppliercontact)
            if totalcost:
                totalcost=int(totalcost)
            if not os.path.exists(MEDIA_ROOT+'library'):
                os.makedirs(MEDIA_ROOT+'library')
            if donor=="1":
                totalcost=0
                paymentmode=''
                reciptno=''
            #finally saving data to database 
            p1=tbl_libItem()
            p1.itemName=itemname
            p1.itemCode=itemcode
            p1.type=itemtype
            p1.author=author
            p1.publisher=publication
            p1.save()
            if not os.path.exists(MEDIA_ROOT+'library/'+str(p1.id)):
                os.makedirs(MEDIA_ROOT+'library/'+str(p1.id))
            
            x=MEDIA_ROOT+'library/'+str(p1.id)+'/'
            p3=tbl_itemInfo()
            p3.mrpprice=price
            p3.edition=edition
            
            p3.save()
            
            
            p2=tbl_supplier()
            p2.name=suppliername
            p2.address=supplieraddress
            p2.paymentMode=paymentmode
            p2.recipt=reciptno
            p2.quantity=quantity
            if suppliercontact:
                p2.contact=suppliercontact
            if totalcost:
                p2.billamt=totalcost
            p2.date=date1
            p2.info=p3
            p2.save()
            p1.suppliers.add(p2)
            i=1
            while i<=quantity:
                p5=tbl_uniqueitemList()
                p5.save()
                ean = barcode.get('ean13','9876'+str(p1.id)+str(p5.id))
                #filename = ean.save(MEDIA_ROOT+'library/'+str(p1.id)+'/'+str(i))
                
                #p5.barcodeImage='library/'+str(p1.id)+'/'+str(i)
                p5.barcodeNo=ean.get_fullcode()
                p5.info=p3
                
                p5.save()
                p1.totalquantity.add(p5)
                i=i+1
            p1.save()
            return HttpResponseRedirect('/libItems/')
                
        return render_to_response('addLibItem.html',locals(),context_instance=RequestContext(req))
def v_editLibItem(req,para):# this will help to edit row present in database
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'library','u'):
        para=int(para)
        uniqueitem=tbl_libItem.objects.get(id=para)
        listitem=['Book','CD-DVD','Magazine','Other']
        
        errors=[]
        #accessing data from database
        itemname=uniqueitem.itemName
        itemcode=uniqueitem.itemCode
        itemtype=uniqueitem.type
        quantity=uniqueitem.gettotalquantity()
        edition=uniqueitem.getedition()
        price=uniqueitem.getmrp()
        author=uniqueitem.getauthor()
        publication=uniqueitem.getpublisher()
        
        if req.POST.get('editLibItem',''):#acessing and validating form elements  
            itemname=req.POST.get('itemname','').strip()
            itemcode=req.POST.get('itemcode','').strip()
            itemtype=req.POST.get('itemtype','')
            quantity=req.POST.get('quantity','').strip()
            edition=req.POST.get('edition','').strip()
            author=req.POST.get('author','').strip()
            publication=req.POST.get('publication','').strip()
            price=req.POST.get('price','').strip()
            
            if not itemname:
                errors.append("Please enter the item name!")
                return render_to_response('editLibItem.html',locals(),context_instance=RequestContext(req))
            if not itemcode:
                errors.append("Please enter the code!")
                return render_to_response('editLibItem.html',locals(),context_instance=RequestContext(req))
            
            if not price:
                errors.append("Please enter the price!")
                return render_to_response('editLibItem.html',locals(),context_instance=RequestContext(req))
            
            
            if tbl_libItem.objects.filter(itemCode=itemcode).exclude(id=para):
                errors.append("Please enter different code.This code already exist!")
                return render_to_response('editLibItem.html',locals(),context_instance=RequestContext(req))
            
            
            price=int(price)
            
            #finally updating database with new values
            uniqueitem.itemName=itemname
            uniqueitem.itemCode=itemcode
            uniqueitem.type=itemtype
            uniqueitem.publisher=publication
            uniqueitem.author=author
            uniqueitem.save()
            
            
            
            obj=uniqueitem.suppliers.all()[0]
            obj.info.mrpprice=price
            obj.info.edition=edition
            
            obj.info.save()
            
            
            
            
            
            obj.save()
            
            
            uniqueitem.save()
            return HttpResponseRedirect('/libItems/')
        
        return render_to_response('editLibItem.html',locals(),context_instance=RequestContext(req))
def v_libItemViewAll(req,para):#accessing all values of item from database
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'library','v'): 
        para=int(para)
        uniquerow=tbl_libItem.objects.get(id=para)
        rows=uniquerow.totalquantity.filter(remove=False).order_by('-status')
        return render_to_response('viewalllibitem.html',locals(),context_instance=RequestContext(req))
def v_getPersonDetail(req):
    
    if req.GET.get('ptypeid',''):# returning person details using ajax 
        getlist=req.GET.get('ptypeid','').split(':')
        
        rows=tbl_libIssuePeriod.objects.filter(type=getlist[0])
        
        if rows:
            days=str(rows[0].days)
        else:
            days=''
        
        if getlist[0]=='student':#this help to access students details
            try:
                uniquestudent=getvalidstudent(getlist[1])
                #=tbl_student.objects.get(id=int(getlist[1][len(STUDENTPREFIX):]))
                template="<div class='section'>\n\
                <label>Name</label><div>\n\
                <input type='text' name='personname' value='"+uniquestudent.getName()+"' readonly >\n\
                </div></div>\n\
                <div class='section' >\n\
                <label>Contact No</label>\n\
                <div> <input type='text' readonly maxlength='12' name='contact' value='"+uniquestudent.getContactNo()+"' onkeypress='return isNumberKey(event)' >\n\
                </div></div>\n\
                <div class='section' >\n\
                <label>Address</label><div><input type='text' name='address' value='"+uniquestudent.perDetail.lAdd+"' readonly >\n\
                </div></div>\n\
                <div class='section' >\n\
                <label>Issue Period<sup>*</sup></label><div><input type='text' placeholder='days' name='issuePeriod' onkeypress='return isNumberKey(event)'  maxlength='4' value='"+days+"' >\n\
                </div></div>"
                return HttpResponse(template)
            except:
                template="<div class='section'>\n\
                <label>Name</label><div>\n\
                <input type='text' name='personname' value='' readonly >\n\
                </div></div>\n\
                <div class='section' >\n\
                <label>Contact No</label>\n\
                <div> <input type='text' name='contact' value='' readonly maxlength='12' onkeypress='return isNumberKey(event)' >\n\
                </div></div>\n\
                <div class='section' >\n\
                <label>Address</label><div><input type='text' name='address' value='' readonly >\n\
                </div></div>\n\
                <div class='section' >\n\
                <label>Issue Period<sup>*</sup></label><div><input type='text' name='issuePeriod' placeholder='days' onkeypress='return isNumberKey(event)' maxlength='4' value='"+days+"' >\n\
                </div></div>"
                return HttpResponse(template)
        if getlist[0]=='staff':# this will help to access teacher details
            try:
                
                uniqueemployee=getvalidemployee(getlist[1])
                template="<div class='section'>\n\
                <label>Name</label><div>\n\
                <input type='text' name='personname' readonly value='"+uniqueemployee.getEMPName()+"' >\n\
                </div></div>\n\
                <div class='section' >\n\
                <label>Contact No</label>\n\
                <div> <input type='text' readonly name='contact' maxlength='12' value='"+uniqueemployee.getEMPContact()+"' onkeypress='return isNumberKey(event)' >\n\
                </div></div>\n\
                <div class='section' >\n\
                <label>Address</label><div><input type='text' name='address' value='"+uniqueemployee.getEMPAdd()+"' readonly >\n\
                </div></div>\n\
                <div class='section' >\n\
                <label>Issue Period<sup>*</sup></label><div><input type='text' maxlength='4' placeholder='days' name='issuePeriod' value='"+days+"' >\n\
                </div></div>"
                return HttpResponse(template)
            except:
                template="<div class='section'>\n\
                <label>Name</label><div>\n\
                <input type='text' name='personname' value='' readonly >\n\
                </div></div>\n\
                <div class='section' >\n\
                <label>Contact No</label>\n\
                <div> <input type='text' name='contact' value='' readonly onkeypress='return isNumberKey(event)' >\n\
                </div></div>\n\
                <div class='section' >\n\
                <label>Address</label><div><input type='text' readonly name='address' value='' >\n\
                </div></div>\n\
                <div class='section' >\n\
                <label>Issue Period</label><div><input type='text' maxlength='4' placeholder='days' name='issuePeriod' value='"+days+"' >\n\
                </div></div>"
                return HttpResponse(template)
        
        return HttpResponse(req.GET.get('ptypeid',''))
    
    if req.GET.get('lastDate',''):
        data=req.GET.get('lastDate','').split(":")
        
        
        Date = datetime.datetime.strptime(data[1], "%d-%m-%Y")
        period=tbl_libMember.objects.get(id=int(data[0][len(LIBMEMPREFIX):])).period.days
        EndDate=Date+datetime.timedelta(days=period)
        abc=DateFormat(EndDate).format('d-m-Y')
        #return HttpResponse(date.strftime('%d-%m-%Y'))
        template="<input type='text' name='lastdate' readonly style='text-align:left;width:150px;' value='"+str(abc)+"'  />"
        return HttpResponse(template)
    
    
def v_libMembers(req):# this method will help to access rows from database
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'library','v'):
        allrows=tbl_libMember.objects.filter()
        pagination_parameter=manavPageParameter    #Used for next and previous (i.e pagination)
        
        NEXT=False
        totalRows=len(allrows)
        TO=len(allrows)
        if len(allrows)>pagination_parameter:
            TO=pagination_parameter
            NEXT=True
        FROM=1
        allrows=allrows[:pagination_parameter]
        
        return render_to_response('libMembers.html',locals(),context_instance=RequestContext(req))

def v_nextlibMembers(req,para):# used to find next list of members having rows equal to manavPageParameter
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'library','v'):
        para=int(para)
        FROM=para+1
        pagination_parameter=manavPageParameter
        
        pagination_parameter=pagination_parameter+para
        allrows=tbl_libMember.objects.filter()
        
        totalRows=len(allrows)
        NEXT=False
        TO=len(allrows)
        if len(allrows)>pagination_parameter:
            TO=pagination_parameter
            NEXT=True
        allrows=allrows[para:pagination_parameter]
        PREV="True"
        back=para
        
        return render_to_response('libMembers.html',locals(),context_instance=RequestContext(req))

def v_prevlibMembers(req,para):#used to find previous list of members having rows equal to manavPageParameter
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'library','v'):
        para=int(para)
        TO=para
        pagination_parameter=manavPageParameter
        back=para-pagination_parameter
        
        allrows=tbl_libMember.objects.filter()
        totalRows=len(allrows)
        NEXT=False
        FROM=back+1
        if len(allrows)>back:
            NEXT=True
        allrows=allrows[back:para]
        if back==0:
            PREV=False
        else:
            PREV=True
        
        return render_to_response('libMembers.html',locals(),context_instance=RequestContext(req))



def v_addLibMember(req):# this will help to add new row to lib member database 
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'library','a'):
        perTypes=['student','staff']
        errors=[]
        if req.POST.get('addLibMember',''):#accessing and validating form elements
            date=req.POST.get('date','').strip()
            
            persontype=req.POST.get('persontype','')
            personId=req.POST.get('personId','').strip()
            
            personname=req.POST.get('personname','').strip()
            contact=req.POST.get('contact','').strip()
            address=req.POST.get('address','').strip()
            issuePeriod=req.POST.get('issuePeriod','').strip()
            month=req.POST.get('month','').strip()
            try:
                date1=dateformatConvertor(str(date))
            except:
                errors.append("Please enter the valid date!")
                return render_to_response('addLibMember.html',locals(),context_instance=RequestContext(req))
            if persontype=="student":
                try:
                    uniquestudent=tbl_student.objects.get(id=int(personId[len(STUDENTPREFIX):]))
                except:
                    errors.append("Please enter valid person id")
                    return render_to_response('addLibMember.html',locals(),context_instance=RequestContext(req))
            if persontype=="staff":
                try:
                    uniqueemployee=tbl_employee.objects.get(id=int(personId[len(EMPLOYEE_PREFIX):]))
                except:
                    errors.append("Please enter valid person id")
                    return render_to_response('addLibMember.html',locals(),context_instance=RequestContext(req))
            
            if tbl_libMember.objects.filter(personId=personId):
                errors.append("This person is already a member")
                return render_to_response('addLibMember.html',locals(),context_instance=RequestContext(req))
            try:
                issuePeriod=int(issuePeriod)
            except:
                errors.append("Please enter the issue period!")
                return render_to_response('addLibMember.html',locals(),context_instance=RequestContext(req))
            if month:
                month=int(month)
            # adding new row to database 
            p1=tbl_libMember()
            p1.personId=personId
            p1.type=persontype
            rows=tbl_libIssuePeriod.objects.filter(type=persontype)
            if rows:
                obj=rows[0]
                obj.days=issuePeriod
                obj.save()
            else:
                obj=tbl_libIssuePeriod()
                obj.type=persontype
                obj.days=issuePeriod
                obj.save()
            p1.period=obj
            if month:
                p1.memberTenure=month
            p1.date=date1
            if req.FILES.get('personImage'):
                
                imagePath=uploadX(req.FILES['personImage'],str(personId))
                p1.image=imagePath
            p1.save()
            return HttpResponseRedirect('/libMembers/')
        return render_to_response('addLibMember.html',locals(),context_instance=RequestContext(req))
def v_editLibMember(req,para):#this will help to update database row with new values
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'library','u'):
        para=int(para)
        perTypes=['student','staff']
        errors=[]
        #accessing row data from database
        uniquerow=tbl_libMember.objects.get(id=para)
        date=dateformatReverse(str(uniquerow.date))
        persontype=uniquerow.type
        personname=uniquerow.getPersonName()
        personId=uniquerow.personId
        address=uniquerow.getPersonAdd()
        contact=uniquerow.getPersonContact()
        issuePeriod=uniquerow.period.days
        month=uniquerow.memberTenure
        if uniquerow.isActive==True:
            status="1"
        if uniquerow.image:
            imageadd=uniquerow.getimageurl()
        if req.POST.get('editLibMember',''):#accessing and validating form elements
            status=req.POST.get('status','')
            issuePeriod=req.POST.get('issuePeriod','').strip()
            month=req.POST.get('month','').strip()
            
            try:
                issuePeriod=int(issuePeriod)
            except:
                errors.append("Please enter the issue period!")
                return render_to_response('editLibMember.html',locals(),context_instance=RequestContext(req))
            if month:
                month=int(month)
            
           
            rows=tbl_libIssuePeriod.objects.filter(type=persontype)
            if rows:
                obj=rows[0]
                obj.days=issuePeriod
                obj.save()
            else:
                obj=tbl_libIssuePeriod()
                obj.type=persontype
                obj.days=issuePeriod
                obj.save()
            uniquerow.period=obj
            if month:
                uniquerow.memberTenure=month
            if status=="1":
                uniquerow.isActive=True
            else:
                uniquerow.isActive=False
            if req.FILES.get('personImage'):
                
                imagePath=uploadX(req.FILES['personImage'],str(personId))
                uniquerow.image=imagePath
            uniquerow.save()
            return HttpResponseRedirect('/libMembers/')
            
            
        return render_to_response('editLibMember.html',locals(),context_instance=RequestContext(req))
    
def uploadX(fileObj,name):#this method is written to carry out jpeg image upload
    import os
    subDirectory=LibUDir
    try:
        with open(MEDIA_ROOT+subDirectory+'/'+str(name)+'image'+".jpeg", 'w') as destination:
            for chunk in fileObj.chunks():
                destination.write(chunk)
        return subDirectory+'/'+name+'image'+".jpeg"
    except IOError:
        if not os.path.exists(MEDIA_ROOT+subDirectory):
            os.makedirs(MEDIA_ROOT+subDirectory)
        
        with open(MEDIA_ROOT+subDirectory+'/'+str(name)+'image'+".jpeg", 'w') as destination:
            for chunk in fileObj.chunks():
                destination.write(chunk)
        return subDirectory+'/'+name+'image'+".jpeg"
def v_libmanagestock(req):# used to carry out listing of lib items 
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'library','v'):
    
   
        allrows=tbl_libItem.objects.filter()
        pagination_parameter=manavPageParameter    #Used for next and previous (i.e pagination)
        
        NEXT=False
        totalRows=len(allrows)
        TO=len(allrows)
        if len(allrows)>pagination_parameter:
            TO=pagination_parameter
            NEXT=True
        FROM=1
        allrows=allrows[:pagination_parameter]
        
        return render_to_response('managestock.html',locals(),context_instance=RequestContext(req))
def v_Prevlibmanagestock(req,para):# used for previous listing of data
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'library','v'):
        para=int(para)
        TO=para
        pagination_parameter=manavPageParameter
        back=para-pagination_parameter
        
        allrows=tbl_libItem.objects.filter()
        totalRows=len(allrows)
        NEXT=False
        FROM=back+1
        if len(allrows)>back:
            NEXT=True
        allrows=allrows[back:para]
        if back==0:
            PREV=False
        else:
            PREV=True
        
        return render_to_response('managestock.html',locals(),context_instance=RequestContext(req))
def v_Nextlibmanagestock(req,para):#used to access the next elements
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'library','v'):
        para=int(para)
        FROM=para+1
        pagination_parameter=manavPageParameter
        
        pagination_parameter=pagination_parameter+para
        
        allrows=tbl_libItem.objects.filter()
        totalRows=len(allrows)
        NEXT=False
        TO=len(allrows)
        if len(allrows)>pagination_parameter:
            TO=pagination_parameter
            NEXT=True
        allrows=allrows[para:pagination_parameter]
        PREV="True"
        back=para
        
        return render_to_response('managestock.html',locals(),context_instance=RequestContext(req))
def v_libstockmodify(req,para):# helps to modify the library stock by adding or removing quantity of element whose id is para
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'library','a'):
        para=int(para)
        uniqueobj=tbl_libItem.objects.get(id=para)
        getitems=uniqueobj.totalquantity.filter(status=True,remove=False)
        
        paymodelist=['Cash','Cheque','Draft']
        errors=[]
        if req.POST.get('modifyLibStock',''):# this will add quantity
            # accessing and validating form elements
            quantity=req.POST.get('quantity','').strip()
            edition=req.POST.get('edition','').strip()
            
            price=req.POST.get('price','').strip()
            suppliername=req.POST.get('suppliername','').strip()
            suppliercontact=req.POST.get('suppliercontact','').strip()
            supplieraddress=req.POST.get('supplieraddress','').strip()
            totalcost=req.POST.get('totalcost','').strip()
            paymentmode=req.POST.get('paymentmode','')
            date=req.POST.get('date','').strip()
            reciptno=req.POST.get('reciptno','').strip()
            donor=req.POST.get('donor','')
            
            try:
                quantity=int(quantity)
            except:
                errors.append("Please enter the valid quantity!")
                return render_to_response('libStockModify.html',locals(),context_instance=RequestContext(req))
            if not price:
                errors.append("Please enter the price!")
                return render_to_response('libStockModify.html',locals(),context_instance=RequestContext(req))
            try:
                date1=dateformatConvertor(date)
            except:
                errors.append("Please enter the valid date !")
                return render_to_response('libStockModify.html',locals(),context_instance=RequestContext(req))
            if not suppliername:
                errors.append("Please enter the supplier name!")
                return render_to_response('libStockModify.html',locals(),context_instance=RequestContext(req))
            
            
            if quantity==0:
                errors.append("Quantity cannot be 0!")
                return render_to_response('libStockModify.html',locals(),context_instance=RequestContext(req))
            if quantity>500:
                errors.append("Please enter the quantity less than 500!")
                return render_to_response('libStockModify.html',locals(),context_instance=RequestContext(req))
            price=int(price)
            if suppliercontact:
                suppliercontact=int(suppliercontact)
            if totalcost:
                totalcost=int(totalcost)
            
            if donor=="1":
                totalcost=0
                paymentmode=''
                reciptno=''
            #finally adding quantity to database
            
            p3=tbl_itemInfo()
            p3.mrpprice=price
            p3.edition=edition
            
            p3.save()
            
                
            i=0
            while i<quantity:
                p5=tbl_uniqueitemList()
                p5.save()
                ean = barcode.get('ean13','9876'+str(uniqueobj.id)+str(p5.id))
                #filename = ean.save(MEDIA_ROOT+'library/'+str(uniqueobj.id)+'/'+str(i))
                
                #p5.barcodeImage='library/'+str(uniqueobj.id)+'/'+str(i)
                p5.barcodeNo=ean.get_fullcode()
                p5.info=p3
                
                p5.save()
                uniqueobj.totalquantity.add(p5)
                i=i+1
                
                
                
                
                
                
            uniqueobj.save()
            
            
            
            
            # adding supplier information
            p2=tbl_supplier()
            p2.name=suppliername
            p2.address=supplieraddress
            p2.paymentMode=paymentmode
            p2.recipt=reciptno
            p2.quantity=quantity
            if suppliercontact:
                p2.contact=suppliercontact
            if totalcost:
                p2.billamt=totalcost
            p2.date=date1
            p2.info=p3
            p2.save()
            uniqueobj.suppliers.add(p2)
            uniqueobj.save()
            return HttpResponseRedirect('/manageStocks/')
        if req.POST.get('removestock',''):# this will help to deduct the item stock
            remark=req.POST.get('remark','').strip()
            remdate1=req.POST.get('remdate1','').strip()
            getids=""
            try:
                rdate=dateformatConvertor(remdate1)
            except:
                errors.append("Please enter valid date!")
                return render_to_response('libStockModify.html',locals(),context_instance=RequestContext(req))
            
            
            for data in getitems:
                
                if req.POST.get(str(data.id),''):
                    
                    getids=getids+data.getItemId()+'/'
                    data.remove=True
                    data.save()
            if getids=="":
                errors.append("Please select atleast one item to deduct!")
                return render_to_response('libStockModify.html',locals(),context_instance=RequestContext(req))
            #updating the database
            p1=tbl_removeLibItems()
            p1.ids=getids
            p1.date=rdate
            p1.remark=remark
            p1.save()
            uniqueobj.remove.add(p1)
            uniqueobj.save()
            return HttpResponseRedirect('/manageStocks/')
        return render_to_response('libStockModify.html',locals(),context_instance=RequestContext(req))
def v_libstockhistory(req,para):# this will help to access the history of library item purchase
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'library','v'):
        para=int(para)
        uniqueobj=tbl_libItem.objects.get(id=para)
        allrows=uniqueobj.suppliers.all()
        getrows=uniqueobj.remove.all()
        return render_to_response('stockhistory.html',locals(),context_instance=RequestContext(req))
def v_libdeducthistory(req,para):
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'library','v'):
        para=int(para)
        uniqueobj=tbl_removeLibItems.objects.get(id=para)
        list=uniqueobj.ids.split('/')
        
        overall=[]
        for item in list[:-1]:
            temp=[]
            uniquerow=tbl_uniqueitemList.objects.get(id=int(item[len(LIBPREFIX):]))
            temp.append(item)
            temp.append(uniquerow.barcodeNo)
            temp.append(uniquerow.info.edition)
            temp.append(uniquerow.info.mrpprice)
            overall.append(temp)
        
        return render_to_response('deducthistory.html',locals(),context_instance=RequestContext(req)) 
def v_itemIssues(req):
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'library','v'):
    
        allrows=tbl_issueItem.objects.filter().order_by('-issueDate')
        pagination_parameter=manavPageParameter    #Used for next and previous (i.e pagination)
        
        NEXT=False
        totalRows=len(allrows)
        TO=len(allrows)
        if len(allrows)>pagination_parameter:
            TO=pagination_parameter
            NEXT=True
        FROM=1
        allrows=allrows[:pagination_parameter]
        
        return render_to_response('issueItem.html',locals(),context_instance=RequestContext(req))
def v_nextitemIssues(req,para):# used to find next list of students having rows equal to manavPageParameter
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'library','v'):
        para=int(para)
        FROM=para+1
        pagination_parameter=manavPageParameter
        
        pagination_parameter=pagination_parameter+para
        
        allrows=tbl_issueItem.objects.filter().order_by('-issueDate')
        totalRows=len(allrows)
        NEXT=False
        TO=len(allrows)
        if len(allrows)>pagination_parameter:
            TO=pagination_parameter
            NEXT=True
        allrows=allrows[para:pagination_parameter]
        PREV="True"
        back=para
        
        return render_to_response('issueItem.html',locals(),context_instance=RequestContext(req))

def v_previtemIssues(req,para):#used to find previous list of students having rows equal to manavPageParameter
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'library','v'):
        para=int(para)
        TO=para
        pagination_parameter=manavPageParameter
        back=para-pagination_parameter
        
        allrows=tbl_issueItem.objects.filter().order_by('-issueDate')
        totalRows=len(allrows)
        NEXT=False
        FROM=back+1
        if len(allrows)>back:
            NEXT=True
        allrows=allrows[back:para]
        if back==0:
            PREV=False
        else:
            PREV=True
        
        return render_to_response('issueItem.html',locals(),context_instance=RequestContext(req))







def v_libItemSearch(req):
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'library','v'):
        types=['Book','CD-DVD','Magazine','Other']
        if req.POST.get('Search',''):
            getdata=True
            type=req.POST.get('type','').strip()
            itemname=req.POST.get('itemname','').strip()
            itemcode=req.POST.get('itemcode','').strip()
            author=req.POST.get('author','').strip()
            publisher=req.POST.get('publisher','').strip()
            allrows=tbl_libItem.objects.filter(itemName__contains=itemname,itemCode__contains=itemcode,author__contains=author,publisher__contains=publisher,type=type)
            
        return render_to_response('searchitem.html',locals(),context_instance=RequestContext(req))
def v_addIssue(req,para):
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'library','a'):
        para=int(para)
        getdata=True
        uniquerow=tbl_libItem.objects.get(id=para)
        
        allrows=uniquerow.totalquantity.filter(remove=False).order_by('-status')
        itemname=uniquerow.itemName
        itemcode=uniquerow.itemCode
        errors=[]
        if req.POST.get('issue',''):
            itemname=req.POST.get('itemname','').strip()
            itemcode=req.POST.get('itemcode','').strip()
            itemid=req.POST.get('itemid','').strip()
            memberid=req.POST.get('memberid','').strip()
            issuedate=req.POST.get('issuedate','').strip()
            lastdate=req.POST.get('lastdate','').strip()
            try:
                itemobj=tbl_uniqueitemList.objects.get(id=int(itemid[len(LIBPREFIX):]))
            except:
                errors.append("Please enter the valid Item Id!")
                return render_to_response('addIssue.html',locals(),context_instance=RequestContext(req))
            if not itemobj in allrows:
                errors.append("The Item Id which you have entered does not belong to selected item!")
                return render_to_response('addIssue.html',locals(),context_instance=RequestContext(req))
            if itemobj.status==False:
                errors.append("The Item Id which you have entered is not available!")
                return render_to_response('addIssue.html',locals(),context_instance=RequestContext(req))
            try:
                memberobj=tbl_libMember.objects.get(id=int(memberid[len(LIBMEMPREFIX):]))
            except:
                errors.append("Please enter valid MemberId")
                return render_to_response('addIssue.html',locals(),context_instance=RequestContext(req))
            try:
                date1=dateformatConvertor(issuedate)
            except:
                errors.append("Please enter issue date in valid format dd-mm-yyyy!")
                return render_to_response('addIssue.html',locals(),context_instance=RequestContext(req))
            
            date2=dateformatConvertor(lastdate)
            
            
            p1=tbl_issueItem()
            p1.itemType=uniquerow.type
            p1.itemCode=uniquerow.itemCode
            p1.itemId=itemid
            p1.personId=memberid
            p1.issueDate=date1
            p1.expiryDate=date2
            itemobj.status=False
            itemobj.save()
            p1.save()
            return HttpResponseRedirect('/Issues/')
        return render_to_response('addIssue.html',locals(),context_instance=RequestContext(req))
def v_editIssue(req,para):
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'library','u'):
        para=int(para)
        uniquerow=tbl_issueItem.objects.get(id=para)
        itemname=uniquerow.getitemName()
        itemcode=uniquerow.itemCode
        itemid=uniquerow.itemId
        memberid=uniquerow.personId
        issuedate=uniquerow.getIssueDate()
        lastdate=uniquerow.getLastDate()
        returndate=uniquerow.getReturnDate()
        errors=[]
        if req.POST.get('SaveIssue',''):
            reissuedate=req.POST.get('reissuedate','').strip()
            returndate=req.POST.get('returndate','').strip()
            lastdate=req.POST.get('lastdate','').strip()
            if reissuedate:
                try:
                    date1=dateformatConvertor(reissuedate)
                except:
                    errors.append("Please enter valid re-issue date!")
                    return render_to_response('editIssue.html',locals(),context_instance=RequestContext(req))
            
            if returndate:
                try:
                    date2=dateformatConvertor(returndate)
                except:
                    errors.append("Please enter valid return date!")
                    return render_to_response('editIssue.html',locals(),context_instance=RequestContext(req))
            if not reissuedate:
                if not returndate:
                    errors.append("Please enter either Re-IssueDate or Return Date! ")
                    return render_to_response('editIssue.html',locals(),context_instance=RequestContext(req))
            date3=dateformatConvertor(lastdate)
            if reissuedate:
                
                uniquerow.issueDate=date1
            if returndate:
                uniquerow.dateofReturn=date2
            else:
                uniquerow.dateofReturn=None
            uniquerow.expiryDate=date3
            uniquerow.save()
            return HttpResponseRedirect('/Issues/')
        return render_to_response('editIssue.html',locals(),context_instance=RequestContext(req))
    