from django.shortcuts import render_to_response
from django.template.context import RequestContext
from App.models import tbl_MSS, tbl_standard, tbl_teacher,\
    tbl_subject, tbl_subjectAndTeacher, tbl_systemUser
from SMS.settings import EMPLOYEE_PREFIX
from views.permission import i_hasPermission

def v_subjectAndTeacher(req):
    if i_hasPermission(tbl_systemUser.objects.get(username=req.session.get('username')),'assign','a'):
        
        standards=tbl_standard.objects.values_list('name').distinct()
        EP=EMPLOYEE_PREFIX
        
        
        if req.method=='POST':
            
            errors=[]
            teachers=tbl_teacher.objects.filter(isActive=True)
            
            standardName=req.POST.get('standardName')
            mediumName=req.POST.get('mediumName')
            
            try:
                mediums=[r[0] for r in tbl_standard.objects.filter(name=standardName).values_list('medium__name').distinct()]
                allSubject=tbl_subject.objects.filter(standards=tbl_standard.objects.get(name=standardName,medium__name=mediumName))
                mssesByStandard=tbl_MSS.objects.filter(standard__name=standardName,medium__name=mediumName)
            except:
                pass
            
            if standardName=='-1':
                errors.append('please select standard !')
            elif mediumName=='-1':
                errors.append('please select medium !')
            else:
                
                
                
                dataRows=[]
                '''
                dataRows has format 
                [subject id , subject name ,[[mssid,teacherid],...]]
                '''
                #return HttpResponse(mssesByStandard[0].section.name)
                #return HttpResponse(uniqueSections)
                uniqueSections=[]    
                for standard in tbl_standard.objects.filter(name=standardName,medium__name=mediumName):
                    for section in standard.sections.all():
                        uniqueSections.append(section.name)
                uniqueSections=sorted(uniqueSections)
                
                for s in allSubject:
                    temp1=[]
                    temp1.append(s.id)
                    temp1.append(s.name.title())
                    temp2=[]
                    for section in uniqueSections:
                        selectMssId=int(mssesByStandard.get(section__name=section).id)
                        selectName="tid_of_"+str(s.id)+":"+str(selectMssId)
                        temp2.append([selectMssId,int(req.POST.get(selectName,-1))])
                        if int(req.POST.get(selectName,-1))==-1:
                            errors.append("please select teacher for '"+s.name.title()+"' of '"+section+"' section !")
                    temp1.append(temp2)
                    dataRows.append(temp1)
                
                w_msg="no subject found for '"+standardName+"' standard '"+mediumName+"' medium ,please add first !"
                if not allSubject:
                    return render_to_response('subjectAndTeacher.html', context_instance=RequestContext(req,{'standards':standards,'cuWarnings':[w_msg]}))
            
            
            
            if not errors:
    #            '''
    #            checking is class teacher defined for any (standard,medium,section)
    #            '''
    #            for row in dataRows:
    #                _temp1=[]
    #                _temp1.append(row[0])
    #                _temp1.append(row[1])
    #                _temp2=[]
    #                for mssid,tid in row[2]:
    #                    try:
    #                        if mssesByStandard.get(id=mssid).subjectAndTeachers.get(mssId=mssid,tid=tid).ifCT:
    #                            _temp2.append([mssid,tid,True])
    #                        else:
    #                            _temp2.append([mssid,tid,False])
    #                    except:
    #                        _temp2.append([mssid,tid,False])
    #                _temp1.append(_temp2)
    #                newDataRows.append(_temp1)
    #            
                '''
                now deleting subjectAndTeachers from each mss belong to submit form
                '''
                for x in dataRows:
                    for mid,tid in x[2]:
                        try:
                            mssesByStandard.get(id=mid).subjectAndTeachers.all().delete()
    #                        obj=mssesByStandard.get(id=mid).subjectAndTeachers.all().delete()
    #                        obj.subjectAndTeachers.all().delete()
    #                        obj.save()
                        except:
                            pass
                
                '''
                finally storing data
                '''
                for row in dataRows:
                    for mssid,tid in row[2]:
                        tbl_MSS.objects.get(id=mssid).subjectAndTeachers.add(tbl_subjectAndTeacher.objects.create(mssId=mssid,tid=tid,subject=row[1]))
                    
                msg="subjects successfully assigned to '"+standardName+"' standard '"+mediumName+"' medium ,to see or edit please select same standard and medium in below dropdowns."
                return render_to_response('subjectAndTeacher.html', context_instance=RequestContext(req,{'standards':standards,'cuMessages':[msg]}))
                
                 
                
            return render_to_response('subjectAndTeacher.html',locals(),context_instance=RequestContext(req))
        return render_to_response('subjectAndTeacher.html',locals(),context_instance=RequestContext(req))
        
