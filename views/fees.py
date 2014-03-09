from django.shortcuts import render_to_response
from django.http import HttpResponse
from App.models import tbl_medium, tbl_shortstandard, tbl_standard,\
    tbl_taskList, tbl_systemUser, tbl_fees, tbl_feeParameter, tbl_school,\
    tbl_student, tbl_feePayment, tbl_tempFees, tbl_MSS
from cStringIO import StringIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from SMS.settings import STUDENTPREFIX, manavPageParameter, MEDIA_ROOT
from views.student import dateformatConvertor
from xlwt.Style import easyxf
from xlwt import Workbook
from django.core.servers.basehttp import FileWrapper
from xlwt.Formatting import Font
from django.template.context import RequestContext
from views.permission import i_hasPermission

'''


from django.http import HttpResponseRedirect
from django.template.context import RequestContext


def v_moreList(req):
    workfortoDoList(req)
    alltask=v_allTaskList(req)
    
    try:
        uncompletedTask=tbl_taskList.objects.filter(isActive=True,username=tbl_systemUser.objects.get(username=req.session1['username']))
        completedTask=tbl_taskList.objects.filter(isActive=False,username=tbl_systemUser.objects.get(username=req.session1['username']))
    except:
        pass    
    return render_to_response("MoreList.html",locals(),context_instance=RequestContext(req))
def workfortoDoList(req):
    try:
        empobj=tbl_systemUser.objects.get(username=req.session1['username'])
        alltask=tbl_taskList.objects.filter(isActive=True,username=empobj)
        if req.POST.get('Submitlist',''):
            for item in alltask:
                if req.POST.get('xxx'+str(item.id),''):
                    item.isActive=False
                    item.completedDate=datetime.datetime.today()
                    item.save()
            description=req.POST.get('tododescription','').strip()
            
            if description:
                
                p1=tbl_taskList(description=description,username=tbl_systemUser.objects.get(username=req.session1['username']))
                p1.save()  
    except:
        pass

def v_allTaskList(req):
    try:
        empobj=tbl_systemUser.objects.get(username=req.session1['username'])
        alltasklist=tbl_taskList.objects.filter(isActive=True,username=empobj)
        return alltasklist
    except:
        pass
'''
from App.models import tbl_feetype
from django.http import HttpResponseRedirect
import datetime
def v_feeCategory(req):
    '''
    this method helps to see listing of feetypes
    '''
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'fees','v'): 
        rows=tbl_feetype.objects.filter()
        return render_to_response('feeCategory.html',locals(),context_instance=RequestContext(req))

def v_AddfeeCategory(req):
    '''
    this method helps to add fee type
    '''
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'fees','a'): 
        months=['January','February','March','April','May','June','July','August','September','October','November','December']
        errors=[]
        if req.POST.get('addFeeCategory',''):
            '''
            accessing and performing form elements validation
            ''' 
            name=req.POST.get('name','').strip()
            types=req.POST.get('types','')
            i=1
            m=[]
            while i<13:
                if req.POST.get(str(i),''):
                    m.append(int(req.POST.get(str(i),'')))
                i=i+1
            facility=req.POST.get('facility','')
            if not name:
                errors.append("Please enter the name!")
            dup=tbl_feetype.objects.filter(name=name)
            if dup:
                errors.append("Please enter different name!")
                return render_to_response('feeCategoryadd.html',locals(),context_instance=RequestContext(req))
            if len(m)<1:
                errors.append("Please select atleast month!")
            if errors:
                return render_to_response('feeCategoryadd.html',locals(),context_instance=RequestContext(req))
            x=''
            for item in m:
                x=x+str(item)+','
            '''
            inserting the data into database
            '''
            p1=tbl_feetype()
            p1.name=name
            p1.types=types
            p1.month=x
            if facility:
                p1.facility=True
            p1.save()
            return HttpResponseRedirect('/feeCategory/')
               
                
        return render_to_response('feeCategoryadd.html',locals(),context_instance=RequestContext(req))
def v_Editfeecategory(req,para):
    '''
    this method helps to view and edit the fee types
    '''
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'fees','u'): 
        para=int(para)
        months=['January','February','March','April','May','June','July','August','September','October','November','December']
        uniqueobj=tbl_feetype.objects.get(id=para)
        name=uniqueobj.name
        types=uniqueobj.types
        
        mlist=uniqueobj.month.split(',')
        param=[]
        for ml in mlist:
            try:
                
                param.append(int(ml))
            except:
                pass
        facility=uniqueobj.facility
        if facility==True:
            facility="1"
        
        errors=[]
        if req.POST.get('editFeeCategory',''):
            '''
            accessing and performong form elements validations
            '''
            name=req.POST.get('name','').strip()
            types=req.POST.get('types','')
            i=1
            param=[]
            while i<13:
                if req.POST.get(str(i),''):
                    param.append(int(req.POST.get(str(i),'')))
                i=i+1
            facility=req.POST.get('facility','')
            if not name:
                errors.append("Please enter the name!")
            dup=tbl_feetype.objects.filter(name=name).exclude(id=para)
            if dup:
                errors.append("Please enter different name!")
                return render_to_response('EditfeeCategory.html',locals(),context_instance=RequestContext(req))
            if len(param)<1:
                errors.append("Please select atleast month!")
            if errors:
                return render_to_response('EditfeeCategory.html',locals(),context_instance=RequestContext(req))
            
            x=''
            for item in param:
                x=x+str(item)+','
            '''
            updating database row with new values
            '''
            uniqueobj.name=name
            uniqueobj.types=types
            uniqueobj.month=x
            uniqueobj.facility=facility
            
            uniqueobj.save()
            return HttpResponseRedirect('/feeCategory/')
        return render_to_response('EditfeeCategory.html',locals(),context_instance=RequestContext(req))
     
def v_assignFees(req):
    '''
    helps to create list of fees amount month-wise in required tabular format for each standard
    '''
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'fees','v'): 
        schoolobj=tbl_school.objects.filter()
        
        errors=[]
        if not schoolobj:
            errors.append("Please specify the school details in setting of configuration!")
            return render_to_response('assignFees.html',locals(),context_instance=RequestContext(req))
        
        
        temp=tbl_fees.objects.values('session1').distinct()
        sessionlist=[]
        selectsession=schoolobj[0].getSession()
        sessionlist.append(schoolobj[0].getSession())
        for data in temp:
            sessionlist.append(data['session1'])
        sessionlist=set(sessionlist)
        months=['Jan','Feb','Mar','Apr','May','June','July','Aug','Sept','Oct','Nov','Dec']
        temp=[]
        temp.append('Standards')
        for data in months:
            temp.append(data)
        temp.append('Total')
        allstandards=tbl_standard.objects.filter().order_by('name')
        overall=[]
        temp1=[]
        if tbl_fees.objects.filter(session1=schoolobj[0].getSession()):
            for st in allstandards:
            
                temp1=[]
                temp1.append(st)
                i=1
                sum1=0
                for m in months:
                    getFees=tbl_fees.objects.filter(standard=st,month=i,session1=schoolobj[0].getSession())
                    if getFees:
                        sum1=sum1+getFees[0].amount 
                        temp1.append(getFees[0].amount)
                        i=i+1
                    else:
                        sum1=sum1
                        temp1.append('-----')
                        i=i+1
                temp1.append(sum1)
                overall.append(temp1)
        return render_to_response('assignFees.html',locals(),context_instance=RequestContext(req))

    
def v_addassignFees(req):
    '''
    helps to define fee amount structure as per month and year wise
    '''
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'fees','a'):
        schoolobj=tbl_school.objects.filter()
        
        errors=[]
        if not schoolobj:
            errors.append("Please specify the school details in setting of configuration!")
            return render_to_response('addassignFees.html',locals(),context_instance=RequestContext(req))
        allstandards=tbl_standard.objects.filter().order_by('name')
        allfeetype=tbl_feetype.objects.filter()
        temp=[]
        temp1=[]
        overall=[]
        temp2=[]
        temp.append('Standards')
        errors=[]
        for fee in allfeetype:
            temp.append(fee.name)
        
        for st in allstandards:
            try:
                temp1.append(st)
                
                getobj=tbl_tempFees.objects.get(standard=st)
                
                fparam=eval(getobj.parameter)
                
                for fee in allfeetype:
                    
                    temp2.append(str(st.id)+str(fee.name))
                    temp2.append(fparam[fee.name])
                    temp1.append(temp2)
                    temp2=[]
            except:
                temp2=[]
                temp1=[]
                temp1.append(st)
                for fp in allfeetype:
                    temp2.append(str(st.id)+str(fp.name))
                    temp2.append('')
                    temp1.append(temp2)
                    temp2=[]
            overall.append(temp1)
            
            temp1=[]
        
        overall1=[]
        
        temp1=[]
        if req.POST.get('addassignFees',''):
            temp2=[]
            getBack=True
            for o in overall:
                
                
                temp2.append(o[0])
                for f in allfeetype:
                    feeamount=req.POST.get(str(o[0].id)+f.name,'').strip()
                    
                    temp1.append(str(o[0].id)+str(f.name))
                    temp1.append(feeamount)
                    if not feeamount:
                        errors.append("Please specify the fees amount for all the standards!")
                    temp2.append(temp1)
                    temp1=[]
                overall1.append(temp2)
                
                temp1=[]
                temp2=[]
            errors=set(errors)
            
            
            if errors:
                return render_to_response('addassignFees.html',locals(),context_instance=RequestContext(req))
        #return HttpResponse(overall)
            else:    
                months=[1,2,3,4,5,6,7,8,9,10,11,12]
                for data in overall1:
                    dicttemp={}
                    try:
                        gettempFeesobj=tbl_tempFees.objects.get(standard=data[0])
                        for fee in allfeetype:
                            dicttemp[fee.name]=req.POST.get(str(data[0].id)+fee.name,'').strip()
                        gettempFeesobj.parameter=str(dicttemp)
                        gettempFeesobj.save()
                    except:
                        gettempFeesobj=tbl_tempFees()
                        gettempFeesobj.standard=data[0]
                        for fee in allfeetype:
                            dicttemp[fee.name]=req.POST.get(str(data[0].id)+fee.name,'').strip()
                        gettempFeesobj.parameter=str(dicttemp)
                        gettempFeesobj.save()
                    
                    for month in months:
                        ftype=[]
                        for pp in allfeetype:
                            
                            monthlist=pp.month.split(',')[:-1]
                            monthlist=[int(p) for p in monthlist]
                            if month in monthlist:
                                
                                ftype.append(pp)
                        
                        rows=tbl_fees.objects.filter(standard=data[0],month=month,session1=schoolobj[0].getSession())
                        if rows:
                            rows[0].feesparameter.all().delete()
                            rows[0].save()
                            xsum=0
                            
                            for p in ftype:
                                
                                getObj=tbl_feeParameter()
                                getObj.name=p.name
                                
                                amt=req.POST.get(str(data[0].id)+p.name,'').strip()
                                
                                getObj.amt=amt
                                getObj.save()
                                xsum=xsum+int(amt)
                                rows[0].feesparameter.add(getObj)
                            rows[0].amount=xsum
                            rows[0].save()
                                
                        else:
                            
                            p1=tbl_fees()
                            p1.standard=data[0]
                            p1.month=month
                            
                            p1.session1=schoolobj[0].getSession()
                            p1.save()
                            xsum=0
                            for ftp in ftype:
                                newrow=tbl_feeParameter()
                                newrow.name=ftp.name
                                newrow.amt=int(req.POST.get(str(data[0].id)+ftp.name,'').strip())
                                xsum=xsum+newrow.amt
                                newrow.save()        
                                p1.feesparameter.add(newrow)
                            p1.amount=xsum
                            p1.save()
                return HttpResponseRedirect('/assignFees/')
        return render_to_response('addassignFees.html',locals(),context_instance=RequestContext(req))

def v_feePayment(req):
    '''
    help to access rows from database to show list of students who have paid the fees
    '''
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'fees','v'):
        schoolobj=tbl_school.objects.filter()
        errors=[]
        if not schoolobj:
            errors.append("Please specify the school details in setting of configuration!")
            return render_to_response('feePayment.html',locals(),context_instance=RequestContext(req))
        
        pagination_parameter=manavPageParameter
        allrows=tbl_feePayment.objects.filter(session1=schoolobj[0].getSession())
        NEXT=False
        errors=[]
        if len(allrows)>pagination_parameter:
            NEXT=True
        allrows=allrows[:pagination_parameter]
        if req.POST.get('getStudent',''):
            studid=req.POST.get('studentid','')
            data=getvalidstudent(studid)
            if data==None:
                errors.append("Please enter valid student id")
                
            
                return render_to_response('feePayment.html',locals(),context_instance=RequestContext(req))
            return render_to_response('searchstudent.html',locals(),context_instance=RequestContext(req))    
        return render_to_response('feePayment.html',locals(),context_instance=RequestContext(req))

def v_nextfeePayment(req,para):
    '''
    helps to access next rows present in database table(which contains list of student who paid fees) 
    '''
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'fees','v'):
        
        para=int(para)
        pagination_parameter=manavPageParameter
        pagination_parameter=pagination_parameter+para
        schoolobj=tbl_school.objects.filter()
        allrows=tbl_feePayment.objects.filter(session1=schoolobj[0].getSession())
        NEXT=False
        if len(allrows)>pagination_parameter:
            NEXT=True
        allrows=allrows[para:pagination_parameter]
        PREV="True"
        back=para
        return render_to_response('feePayment.html',locals(),context_instance=RequestContext(req))
def v_prevfeePayment(req,para):
    '''
    helps to access previous rows present in database table(which contains list of student who paid fees)
    '''
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'fees','v'):
        para=int(para)
        pagination_parameter=manavPageParameter
        back=para-pagination_parameter
        schoolobj=tbl_school.objects.filter()
        allrows=tbl_feePayment.objects.filter(session1=schoolobj[0].getSession())
        NEXT=False
        if len(allrows)>back:
            NEXT=True
        allrows=allrows[back:para]
        if back==0:
            PREV=False
        else:
            PREV=True
        
        return render_to_response('feePayment.html',locals(),context_instance=RequestContext(req))

def v_feePaymentAdd(req,id):
    ''' 
    this will help to add new payment row in database
    '''
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'fees','a'):
        schoolobj=tbl_school.objects.filter()
        errors=[]
        if not schoolobj:
            errors.append("Please specify the school details in setting of configuration!")
            return render_to_response('feePaymentAdd.html',locals(),context_instance=RequestContext(req))
        para=int(id)
        getstud=tbl_student.objects.get(id=para)
        studFacilities=getstud.facilities.all()
        studFacilities=[dd.facility for dd in studFacilities]
        facilities=tbl_feetype.objects.filter(facility=True)
        feesvalues=tbl_fees.objects.filter(standard=getstud.standard,session1=schoolobj[0].getSession())
        temp=[]
        overall=[]
        i=1
        totalamt=0
        
        months=['jan','feb','mar','apr','may','june','july','aug','sept','oct','nov','dec']
        while i<=12:
            temp=[]
            try:
                fv=feesvalues.get(month=i)
                temp.append(months[i-1])
                x=fv.amount
                
                for fac in facilities:
                    if fac in studFacilities:
                        pass
                    else:
                        paramtype=tbl_feetype.objects.filter(name=fac.name)[0]
                        monthlist=paramtype.month.split(',')[:-1]
                        monthlist=[int(m) for m in monthlist]
                        if i in monthlist:
                        
                            
                            z=fv.feesparameter.get(name=fac.name).amt
                            x=x-z
                #return HttpResponse(str(x))        
                temp.append(x)    
                        
                
            except:
                temp=[]
                temp.append(months[i-1])
                temp.append(0)
            temp.append(False)
            temp.append(i)
            i=i+1
            overall.append(temp)
        
        if req.POST.get('SaveFees',''):
            recipt=req.POST.get('recipt','').strip()
            date=req.POST.get('date','').strip()
            amtreceived=req.POST.get('amtreceived','').strip()
            paymode=req.POST.get('paymode','')
            totalamt=int(req.POST.get('totalamt','').strip())
            remaining=req.POST.get('remaining','').strip()
            bank=req.POST.get('bank','').strip()
            chequeno=req.POST.get('chequeno','').strip()
            chequedate=req.POST.get('chequedate','').strip()
            depositedate=req.POST.get('depositedate','').strip()
            cleardate=req.POST.get('cleardate','').strip()
            
            for val in overall:
                xx=req.POST.get(val[0],'')
                if xx:
                    val[2]=True
                else:
                    val[2]=False
            if not recipt:
                errors.append('Please enter the recipt no!')
                return render_to_response('feePaymentAdd.html',locals(),context_instance=RequestContext(req))
            
            if totalamt==0:
                errors.append("Please select atleast one month!")
                return render_to_response('feePaymentAdd.html',locals(),context_instance=RequestContext(req))
            if not amtreceived:
                errors.append("Please enter the valid amount received")
                return render_to_response('feePaymentAdd.html',locals(),context_instance=RequestContext(req))
            try:
                date1=dateformatConvertor(date)
            except:
                errors.append("Please enter the valid date!")
                return render_to_response('feePaymentAdd.html',locals(),context_instance=RequestContext(req))
            amtreceived=int(amtreceived)
            if amtreceived<totalamt:
                errors.append("Amount Received must be greater or equal to Amount")
                return render_to_response('feePaymentAdd.html',locals(),context_instance=RequestContext(req))
            if paymode=="-1":
                errors.append("Please select atleast one payment mode!")
                return render_to_response('feePaymentAdd.html',locals(),context_instance=RequestContext(req))
            if chequedate:
                try:
                    chequedate1=dateformatConvertor(chequedate)
                except:
                    errors.append("Please enter the valid date in payment sections")
                    return render_to_response('feePaymentAdd.html',locals(),context_instance=RequestContext(req))
            if depositedate:
                try:
                    depositedate1=dateformatConvertor(depositedate)
                except:
                    errors.append("Please enter the valid date in payment sections")
                    return render_to_response('feePaymentAdd.html',locals(),context_instance=RequestContext(req))
            if cleardate:
                try:
                    cleardate1=dateformatConvertor(cleardate)
                except:
                    errors.append("Please enter the valid date in payment sections")
                    return render_to_response('feePaymentAdd.html',locals(),context_instance=RequestContext(req))
            for val in overall:
                
                if val[2]==True:
                    feePay=tbl_feePayment.objects.filter(studid=getstud,month=val[3],session1=schoolobj[0].getSession())
                    if feePay:
                        errors.append("You have already paid the fees for selected month")
            errors=set(errors)    
            if errors:
                return render_to_response('feePaymentAdd.html',locals(),context_instance=RequestContext(req))        
            else:
                for dd in overall:
                    
                    if dd[2]==True:
                        newRow=tbl_feePayment()
                        newRow.studid=getstud
                        newRow.session1=schoolobj[0].getSession()
                        
                        #p3.year=year
                        newRow.month=dd[3]
                        newRow.date=date1
                        newRow.paymode=paymode
                        newRow.bankname=bank
                        newRow.chequeno=chequeno
                        #newRow.year=year
                        newRow.reciptno=recipt
                        if cleardate:
                            newRow.chequeClearDate=cleardate1
                        if depositedate:
                            newRow.chequeDepoDate=depositedate1
                        if chequedate:
                            newRow.chequedate=chequedate1
                        newRow.save()
                return HttpResponseRedirect('/feePayment/')
        if req.POST.get('GenerateRecipt',''):
            recipt=req.POST.get('recipt','').strip()
            date=req.POST.get('date','').strip()
            amtreceived=req.POST.get('amtreceived','').strip()
            paymode=req.POST.get('paymode','')
            totalamt=int(req.POST.get('totalamt','').strip())
            remaining=req.POST.get('remaining','').strip()
            bank=req.POST.get('bank','').strip()
            chequeno=req.POST.get('chequeno','').strip()
            chequedate=req.POST.get('chequedate','').strip()
            depositedate=req.POST.get('depositedate','').strip()
            cleardate=req.POST.get('cleardate','').strip()
            
            for val in overall:
                xx=req.POST.get(val[0],'')
                if xx:
                    val[2]=True
                else:
                    val[2]=False
            if not recipt:
                errors.append('Please enter the recipt no!')
                return render_to_response('feePaymentAdd.html',locals(),context_instance=RequestContext(req))
            if totalamt==0:
                errors.append("Please select atleast one month!")
                return render_to_response('feePaymentAdd.html',locals(),context_instance=RequestContext(req))
            try:
                date1=dateformatConvertor(date)
            except:
                errors.append("Please enter the valid date!")
                return render_to_response('feePaymentAdd.html',locals(),context_instance=RequestContext(req))
            if amtreceived<totalamt:
                errors.append("Amount received must be greater or equal to Amount")
                return render_to_response('feePaymentAdd.html',locals(),context_instance=RequestContext(req))
            if paymode=="-1":
                errors.append("Please select atleast one payment mode!")
                return render_to_response('feePaymentAdd.html',locals(),context_instance=RequestContext(req))
            if chequedate:
                try:
                    chequedate1=dateformatConvertor(chequedate)
                except:
                    errors.append("Please enter the valid date in payment sections")
                    return render_to_response('feePaymentAdd.html',locals(),context_instance=RequestContext(req))
            if depositedate:
                try:
                    depositedate1=dateformatConvertor(depositedate)
                except:
                    errors.append("Please enter the valid date in payment sections")
                    return render_to_response('feePaymentAdd.html',locals(),context_instance=RequestContext(req))
            if cleardate:
                try:
                    cleardate1=dateformatConvertor(cleardate)
                except:
                    errors.append("Please enter the valid date in payment sections")
                    return render_to_response('feePaymentAdd.html',locals(),context_instance=RequestContext(req))
            for val in overall:
                
                if val[2]==True:
                    feePay=tbl_feePayment.objects.filter(studid=getstud,month=val[3],session1=schoolobj[0].getSession())
                    if feePay:
                        errors.append("You have already paid the fees for selected month")
            errors=set(errors)    
            if errors:
                return render_to_response('feePaymentAdd.html',locals(),context_instance=RequestContext(req))
                    
            else:
                
                getmonths=[]
                schoolrow=tbl_school.objects.filter()
                if not schoolrow:
                    errors.append("Plese specify school details first in configuration settings")
                    return render_to_response('feePaymentAdd.html',locals(),context_instance=RequestContext(req))
                
                for dd in overall:
                    
                    if dd[2]==True:
                        newRow=tbl_feePayment()
                        newRow.studid=getstud
                        
                        newRow.session1=schoolobj[0].getSession()
                        #p3.year=year
                        newRow.month=dd[3]
                        newRow.date=date1
                        newRow.paymode=paymode
                        newRow.bankname=bank
                        newRow.chequeno=chequeno
                        getmonths.append(dd[0])
                        #newRow.year=year
                        newRow.reciptno=recipt
                        if cleardate:
                            newRow.chequeClearDate=cleardate1
                        if depositedate:
                            newRow.chequeDepoDate=depositedate1
                        if chequedate:
                            newRow.chequedate=chequedate1
                        newRow.save()
                        
                return render_to_response('feeRecipt.html',locals(),context_instance=RequestContext(req))            
                
        #return HttpResponse(dictfees)
        return render_to_response('feePaymentAdd.html',locals(),context_instance=RequestContext(req))
def v_feePaymentedit(req,para):#this will help to access and edit fee payment details
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'fees','u'):
        para=int(para)
        obj=tbl_feePayment.objects.get(id=para)
        name=obj.studid.getName()
        standard=obj.studid.standard.name
        medium=obj.studid.standard.medium.name
        month=obj.month
        session1=obj.session1
        session11=session1[:4]
        session12=session1[5:]
        uniquefee=tbl_fees.objects.get(month=month,session1=session1,standard=obj.studid.standard)
        amount=uniquefee.amount
        date1=obj.rdate()
        paymode=obj.paymode
        bank=obj.bankname
        chequeno=obj.chequeno
        chequedate=obj.rchequedate()
        depositedate=obj.rdepositedate()
        cleardate=obj.rcleardate()
        reciptno=obj.reciptno
        studid=STUDENTPREFIX+str(obj.studid.id)
        errors=[]
        if req.POST.get('editFeePayment',''):#accessing form elements and validating them
            studid=req.POST.get('studid','').strip()
            name=req.POST.get('name','').strip()
            standard=req.POST.get('standard','').strip()
            medium=req.POST.get('medium','').strip()
            month=int(req.POST.get('month',''))
            amount=req.POST.get('amount','').strip()
            date1=req.POST.get('date1','').strip()
            paymode=req.POST.get('paymode','')
            bank=req.POST.get('bank','').strip()
            chequeno=req.POST.get('chequeno','').strip()
            chequedate=req.POST.get('chequedate','').strip()
            depositedate=req.POST.get('depositedate','').strip()
            cleardate=req.POST.get('cleardate','').strip()
            reciptno=req.POST.get('reciptno','').strip()
            #year=int(req.POST.get('year',''))
            
            try:
                uniqueob=tbl_student.objects.get(id=int(studid[len(STUDENTPREFIX):]))
                name=uniqueob.perDetail.fName
                standard=uniqueob.standard.name
                medium=uniqueob.standard.medium.name
            except:
                errors.append('Please enter the valid student id!')
                return render_to_response('editfeePayment.html',locals(),context_instance=RequestContext(req))
            try:
                uniqueFee=tbl_fees.objects.get(month=month,session1=session1)
                amount=uniqueFee.amount
            except:
                errors.append("Fees for this month is not defined!")
                return render_to_response('editfeePayment.html',locals(),context_instance=RequestContext(req))
            try:
                date=dateformatConvertor(date1)
            except:
                errors.append("Please enter the valid date!")
                return render_to_response('editfeePayment.html',locals(),context_instance=RequestContext(req))
            if paymode=="-1":
                errors.append("Please select the payment mode!")
                return render_to_response('editfeePayment.html',locals(),context_instance=RequestContext(req))
            if chequedate:
                try:
                    chequedate1=dateformatConvertor(chequedate)
                except:
                    errors.append("Please enter the valid date in payment sections")
                    return render_to_response('editfeePayment.html',locals(),context_instance=RequestContext(req))
            if depositedate:
                try:
                    depositedate1=dateformatConvertor(depositedate)
                except:
                    errors.append("Please enter the valid date in payment sections")
                    return render_to_response('editfeePayment.html',locals(),context_instance=RequestContext(req))
            if cleardate:
                try:
                    cleardate1=dateformatConvertor(cleardate)
                except:
                    errors.append("Please enter the valid date in payment sections")
                    return render_to_response('editfeePayment.html',locals(),context_instance=RequestContext(req))
            
            #updating database row with new values
            obj.date=date
            obj.paymode=paymode
            obj.bankname=bank
            obj.chequeno=chequeno
            obj.reciptno=reciptno
            if cleardate:
                obj.chequeClearDate=cleardate1
            if depositedate:
                obj.chequeDepoDate=depositedate1
            if chequedate:
                obj.chequedate=chequedate1
            obj.save()
            return HttpResponseRedirect('/feePayment/')
        return render_to_response('editfeePayment.html',locals(),context_instance=RequestContext(req))

def v_generateslip(req):#this will help to generate new fee slip in PDF format
    schoolobj=tbl_school.objects.filter()
    if not schoolobj:
        template="<script>alert('Please specify school details first in configuration module!');window.close()</script>"
        return HttpResponse(template) 
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'filename=feeslip.pdf'

    temp = StringIO()

    
    p = canvas.Canvas(temp)

    
    p.setFont('Times-Bold',18)
    school=tbl_school.objects.filter()
    x=820
    p.drawString(10,x, schoolobj[0].name)
    x=x-20
    p.drawString(10,x,"Address:"+schoolobj[0].address)
    x=x-20
    p.drawString(10,x,"City:"+schoolobj[0].getcityname())
    x=x-20
    p.drawString(10,x,"State:"+schoolobj[0].getstatename())
    x=x-20
    p.drawString(10,x,"Contact No:05712410789")
    p.setFont('Times-Roman',15)
    x=x-30
    p.drawString(10,x,"DateofDeposit:")
    x=x-20
    p.drawString(10,x,"StudentName:")
    x=x-20
    p.drawString(10,x,"StudentId:")
    x=x-20
    p.drawString(10,x,"Standard:")
    x=x-20
    p.drawString(10,x,"Medium:")
    x=x-20
    p.drawString(10,x,"Section:")
    x=x-20
    p.drawString(10,x,"ContactNo:")
    x=x-20
    p.drawString(10,x,"Amount:")
    x=x-20
    p.drawString(10,x,"Amount(In Words):")
    x=x-20
    p.drawString(10,x,"Payment Mode:")
    x=x-20
    p.drawString(10,x,"Payment Details:")
    x=x-50
    p.drawString(490,x,"Signature:")
    
    
    
    
    p.showPage()
    p.save()

    
    response.write(temp.getvalue())
    return response
    return render_to_response('')
def v_feePending(req):
    '''
    this function helps to see and generate excel file of fee defaulters student in tabular format
    '''
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'fees','v'):
        errors=[]
        months=['Jan','Feb','Mar','Apr','May','June','July','Aug','Sept','Oct','Nov','Dec']
        schoolobj=tbl_school.objects.filter()
        if not schoolobj:
            
            errors.append("Please specify the school details in setting of configuration!")
            return render_to_response('latefeePayment.html',locals(),context_instance=RequestContext(req))
        mondict={1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'June',7:'July',8:'Aug',9:'Sept',10:'Oct',11:'Nov',12:'Dec'}
        allMSS=tbl_MSS.objects.filter(isActive=True)
        
        if req.POST.get('exportLateFee',''):# this is used to generate report
            year=req.POST.get('year','')
            month=int(req.POST.get('month',''))
            listing=[]
            if not year:
                errors.append("Please enter the valid year!")
                return render_to_response('latefeePayment.html',locals(),context_instance=RequestContext(req))
            
            
            listing=getFeeDefaulterList(month, year)
            
            if not listing:
                return HttpResponse('<script>alert("No fee Defaulter at present");location.href="/pendingfee/"</script>')
            else:
                #creating excel file
                w = Workbook()
        
                ws = w.add_sheet('AttendenceReport')
                ws.col(1).width=30*256
                styletoprow=easyxf('align: vertical center, horizontal center;'
                               'font: name Arial;'
                               'border:bottom thin,right thin,top thin;'
                               )
                styletoprow1=easyxf('align: vertical center, horizontal center;'
                                'font: name Arial,bold true;'
                         
                                'border:bottom thin,right thin,top thin;'
                                )
                ws.write_merge(0,0,0,4,"Fee Defaulters Report for "+mondict[month]+" "+str(year),styletoprow1)
                ws.write(1,0,'S.No',styletoprow1)
                ws.write(1,1,'Student Name',styletoprow1)
                ws.write(1,2,'Medium',styletoprow1)
                ws.write(1,3,'Standard',styletoprow1)
                ws.write(1,4,'Section',styletoprow1)
                row=2
                
                for data in listing:
                    ws.write(row,0,row-1,styletoprow)
                    ws.write(row,1,data.getName(),styletoprow)
                    ws.write(row,2,data.standard.medium.name,styletoprow)
                    ws.write(row,3,data.standard.name,styletoprow)
                    ws.write(row,4,data.section.name,styletoprow)
                    row=row+1
     
                
                w.save(MEDIA_ROOT+'feedefaulterreport.xls')
                myfile=open(MEDIA_ROOT+'feedefaulterreport.xls',"r")
                response = HttpResponse(FileWrapper(myfile), content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename=feedefaulterReport.xls'
                return response
        if req.POST.get('viewLateFee',''):
            '''
            this is to view the fee defaulter listing
            '''
            listing=[]
            month=int(req.POST.get('month',''))
            getst=int(req.POST.get('getmss',''))
            showtables=True
            if month!=-1:
                if getst!=-1:
                    mssobj=tbl_MSS.objects.get(id=getst)
                    getstudent=tbl_student.objects.filter(standard=mssobj.standard,section=mssobj.section)
                    for data in getstudent:
                        rows=tbl_feePayment.objects.filter(month=month,studid=data,session1=schoolobj[0].getSession())
                        if not rows:
                            listing.append(data)
                    listing=set(listing)        
                    return render_to_response('latefeePayment.html',locals(),context_instance=RequestContext(req))    
                else:
                    getclass=tbl_MSS.objects.filter(isActive=True)
                    for gc in getclass:
                        getstudent=tbl_student.objects.filter(standard=gc.standard,section=gc.section)
                        for data in getstudent:
                            rows=tbl_feePayment.objects.filter(month=month,studid=data,session1=schoolobj[0].getSession())
                            if not rows:
                                listing.append(data)
                    listing=set(listing)
                    return render_to_response('latefeePayment.html',locals(),context_instance=RequestContext(req))
            else:
                if getst==-1:
                    getclass=tbl_MSS.objects.filter(isActive=True)
                    
                    for gc in getclass:
                        getstudent=tbl_student.objects.filter(standard=gc.standard,section=gc.section)
                        i=1
                        for mon in months:
                            for data in getstudent:
                                rows=tbl_feePayment.objects.filter(month=i,studid=data,session1=schoolobj[0].getSession())
                                if not rows:
                                    listing.append(data)
                                i=i+1
                    listing=set(listing)
                    return render_to_response('latefeePayment.html',locals(),context_instance=RequestContext(req))    
                else:
                    gc=tbl_MSS.objects.get(id=getst)
                    
                    
                    getstudent=tbl_student.objects.filter(standard=gc.standard,section=gc.section)
                    i=1
                    for mon in months:
                        for data in getstudent:
                            rows=tbl_feePayment.objects.filter(month=i,studid=data,session1=schoolobj[0].getSession())
                            if not rows:
                                listing.append(data)
                            i=i+1
                    listing=set(listing)
                    return render_to_response('latefeePayment.html',locals(),context_instance=RequestContext(req))
            '''listing=[]
            if not year:
                errors.append("Please enter the valid year!")
                return render_to_response('latefeePayment.html',locals(),context_instance=RequestContext(req))
            
            showtables=True
            listing=getFeeDefaulterList(month,year)'''
            
            return render_to_response('latefeePayment.html',locals(),context_instance=RequestContext(req))
                  
                   
                
        return render_to_response('latefeePayment.html',locals(),context_instance=RequestContext(req))
def getFeeDefaulterList(month,year):
    '''
    function which returns the  list of fee defaulters
    '''
    listing=[]
    for data in tbl_student.objects.filter():
        temp=1
        for fpl in tbl_feePayment.objects.filter(month=month,year=int(year)):
            if fpl.studid==data:
                temp=0
                break
            else:
                temp=1
        if temp==1:
            listing.append(data)
    return listing
def getvalidstudent(studid):
    '''
    Helps to access valid student by its ID
    '''
    prefix=studid[:len(STUDENTPREFIX)]
    if prefix.upper()==STUDENTPREFIX:
        try:
            getid=int(studid[len(STUDENTPREFIX):])
            uniqueobj=tbl_student.objects.get(id=getid)
            return uniqueobj 
        except:
            return None
def v_assignSessionFees(req,para1):
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'fees','v'):
        schoolobj=tbl_school.objects.filter()
        
        
        
        
        temp=tbl_fees.objects.values('session1').distinct()
        sessionlist=[]
        selectsession=para1
        sessionlist.append(schoolobj[0].getSession())
        for data in temp:
            sessionlist.append(data['session1'])
        sessionlist=set(sessionlist)
        months=['Jan','Feb','Mar','Apr','May','June','July','Aug','Sept','Oct','Nov','Dec']
        temp=[]
        temp.append('Standards')
        for data in months:
            temp.append(data)
        temp.append('Total')
        allstandards=tbl_standard.objects.filter().order_by('name')
        overall=[]
        temp1=[]
        if tbl_fees.objects.filter(session1=para1):
            for st in allstandards:
            
                temp1=[]
                temp1.append(st)
                i=1
                sum1=0
                for m in months:
                    getFees=tbl_fees.objects.filter(standard=st,month=i,session1=para1)
                    if getFees:
                        sum1=sum1+getFees[0].amount 
                        temp1.append(getFees[0].amount)
                        i=i+1
                    else:
                        sum1=sum1
                        temp1.append('-----')
                        i=i+1
                temp1.append(sum1)
                overall.append(temp1)
        return render_to_response('assignFees.html',locals(),context_instance=RequestContext(req))