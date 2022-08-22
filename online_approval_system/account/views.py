from django.shortcuts import get_object_or_404
from datetime import datetime
from django import forms
from account.forms import ( UserProfileForm,SecretaryProfileForm,CAProfileForm,CTSProfileForm,CDGCProfileForm,OIProfileForm,OISecurityProfileForm,DAProfileForm,DSAProfileForm,CCSProfileForm,HODProfileForm,
                            reimbursement_Form,reimbursement_event_Form,reimbursement_expenditure_Form,reimbursement_bank_Form,reimbursement_personal_Form,reimbursementFormforSecretary,reimbursementFormforOI,reimbursementFormforCCS_CTS,reimbursementFormforCA,reimbursementFormforDA,reimbursementFormforDSA,reimbursementFormforAll,
                            event_detail_Form,event_expenditure_Form,event_bank_Form,eventFormforCCS_CTS,eventFormforOI,eventFormforCA,eventFormforDA,eventFormforDSA,eventFormforAll,
                            auditoriumForm,auditoriumFormforOI,auditoriumFormforCDGC,auditoriumFormforDA,auditoriumFormforDSA,auditoriumFormforAll,
                            lectureHallForm,lectureHallFormForAll,lectureHallFormForOI,lectureHallFormForOISecurity, lectureHallFormForAll,
                            lab_Form, lab_details_Form,lab_personal_Form,labFormforHOD,labFormforDA,labFormforDSA,labFormforAll
                            )
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from . import models
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from .models import userprofile,reimbursement,event,auditorium,lecturehalls,labs
from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.db.models import F
from django.core.mail import EmailMessage,send_mail

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return render(request,'accounts/login.html',{})
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password_form.html', {
        'form': form
    })

def my_view(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        USER = authenticate(username=username, password=password)

        if USER:
            id=models.userprofile.objects.get(user__username=request.POST.get('username'))
            login(request, USER)
            if id.role=='Student':
                return HttpResponseRedirect('/Student/homepage/')
            elif id.role=='Secretary(Club/Tech Society/NSS/NCC/Others)':
                return HttpResponseRedirect('/Secretary/homepage/')
            elif id.role=='Head of Department':
                return HttpResponseRedirect('/HOD/homepage/')
            elif id.role=='CDGC':
                return HttpResponseRedirect('/CDGC/homepage/')
            elif id.role=='Dean Student Affairs':
                return HttpResponseRedirect('/DSA/homepage/')
            elif id.role=='Dealing Assistant of DSA':
                return HttpResponseRedirect('/DA/homepage/')
            elif id.role=='Chief Technical Society':
                return HttpResponseRedirect('/CTS/homepage/')
            elif id.role=='Chief Cultural Clubs':
                return HttpResponseRedirect('/CCS/homepage/')
            elif id.role=='Chief Advisor':
                return HttpResponseRedirect('/CA/homepage/')
            elif id.role=='O/I(Club/Tech Society/NSS/NCC/Others)':
                return HttpResponseRedirect('/OI/homepage/')
            elif id.role=='O/I Securities' :
                return HttpResponseRedirect('/OISecurity/homepage/')
            else:
                return HttpResponseRedirect('/admin/')
        else:
            messages.error(request, 'You entered wrong password or username!')
            return render(request,"accounts/login.html",{})

    else:
        return render(request,"accounts/login.html",{})

def reimbursement_request(request):
    form1 = reimbursement_personal_Form()
    form2= reimbursement_event_Form()
    form3= reimbursement_expenditure_Form()
    form4= reimbursement_bank_Form()
    if request.method == "POST":
        instance=reimbursement.objects.create()
        form1 = reimbursement_personal_Form(request.POST, request.FILES,instance=instance)
        form2= reimbursement_event_Form(request.POST, request.FILES,instance=instance)
        form3= reimbursement_expenditure_Form(request.POST, request.FILES,instance=instance)
        form4= reimbursement_bank_Form(request.POST, request.FILES,instance=instance)
        if form1.is_valid() and form2.is_valid() and form3.is_valid() and form4.is_valid():
            form1.save()
            form2.save()
            form3.save()
            instance=form4.save(commit=False)
            instance.filed_by=request.user.id
            instance.save()
            sec=userprofile.objects.filter(society_or_club_name=instance.name_of_club_or_technical_society,role="Secretary(Club/Tech Society/NSS/NCC/Others)")
            for inst in sec:
                send_mail('Hello from Student Workshop/Event Management Application!','There is a Reimbursement request for you. This is an automated generated email. So, donot respond to it!',request.user.email,[inst.email], fail_silently=False)
            return homepage(request)
        else:
            instance.delete()
    return render(request,'Student/reimbursementrequest.html',{'form1':form1,'form2':form2,'form3':form3,'form4':form4})

def lab_request(request):
    form1 = lab_personal_Form()
    form2 = lab_details_Form()
    if request.method == "POST":
        instance=labs.objects.create()
        form1 = lab_personal_Form(request.POST, request.FILES,instance=instance)
        form2=lab_details_Form(request.POST, request.FILES,instance=instance)
        if form1.is_valid() and form2.is_valid():
            form1.save()
            instance=form2.save(commit=False)
            instance.filed_by=request.user.id
            instance.progress='in-progress'
            instance.save()
            hod=userprofile.objects.filter(department=instance.department_related_to_project,role="Head of Department")
            for inst in hod:
                send_mail('Hello from Student Workshop/Event Management Application!','There is a lab booking request for you. This is an automated generated email. So, donot respond to it!',request.user.email,[inst.email], fail_silently=False)
            return homepage(request)
        else:
            instance.delete()
    return render(request,'Student/labrequest.html',{'form1':form1,'form2':form2})

def event_request(request):
    form1 =event_detail_Form()
    form2= event_expenditure_Form()
    form3= event_bank_Form()
    if request.method == "POST":
        instance=reimbursement.objects.create()
        form1 =event_detail_Form(request.POST, request.FILES,instance=instance)
        form2= event_expenditure_Form(request.POST, request.FILES,instance=instance)
        form3= event_bank_Form(request.POST, request.FILES,instance=instance)
        if form1.is_valid() and form2.is_valid() and form3.is_valid():
            form1.save()
            form2.save()
            instance=form3.save(commit=False)
            instance.filed_by=request.user.id
            instance.save()
            if instance.type=='Technical':
                ccs=userprofile.objects.filter(role="Chief Technical Society")
                for inst in ccs:
                    send_mail('Hello from Student Workshop/Event Management Application!','There is a event permission request for you. This is an automated generated email. So, donot respond to it!',request.user.email,[inst.email], fail_silently=False)
            else:
                ccs=userprofile.objects.filter(role="Chief Cultural Clubs")
                for inst in ccs:
                    send_mail('Hello from Student Workshop/Event Management Application!','There is a event permission request for you. This is an automated generated email. So, donot respond to it!',request.user.email,[inst.email], fail_silently=False)
            return Secretary_homepage(request)
        else:
            instance.delete()
    return render(request,'Secretary/eventrequest.html',{'form1':form1,'form2':form2,'form3':form3})

def auditorium_request(request):
    form = auditoriumForm()
    if request.method == "POST":
        instance=auditorium.objects.create()
        form = auditoriumForm(request.POST, request.FILES,instance=instance)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.filed_by=request.user.id
            instance.progress='in-progress'
            instance.save()
            oi=userprofile.objects.filter(society_or_club_name=instance.name_of_club_or_technical_society,role="O/I(Club/Tech Society/NSS/NCC/Others)")
            for inst in oi:
                send_mail('Hello from Student Workshop/Event Management Application!',
                'There is a Auditorium booking request for you. This is an automated generated email. So, donot respond to it!',
                request.user.email,[inst.email], fail_silently=False)
            return Secretary_homepage(request)
        else:
            instance.delete()
    return render(request,'Secretary/auditoriumrequest.html',{'form':form})

def LH_request(request):
    form = lectureHallForm()
    if request.method == "POST":
        instance = lecturehalls.objects.create()
        form = lectureHallForm(request.POST, request.FILES,instance=instance)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.filed_by=request.user.id
            instance.progress='in-progress'
            instance.save()
            oi=userprofile.objects.filter(society_or_club_name=instance.name_of_club_or_technical_society,role="O/I(Club/Tech Society/NSS/NCC/Others)")
            for inst in oi:
                send_mail('Hello from Student Workshop/Event Management Application!',
                'There is a lecture hall booking request for you. This is an automated generated email. So, donot respond to it!',
                request.user.email,[inst.email], fail_silently=False)
            return Secretary_homepage(request)
        else:
            instance.delete()
    return render(request,'Secretary/LHrequest.html',{'form':form})

def homepage(request):
    return render(request,"Student/homepage.html",{})

def edit_profile(request):
    instance=request.user.userprofile
    form= UserProfileForm(instance=instance)
    if request.method == 'POST' :
        form = UserProfileForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            instance=request.user.userprofile
            instance=form.save(commit=False)
            instance.save()
            return HttpResponseRedirect('/Student/homepage/')
    context={'form':form}
    return render(request, "Student/editprofile.html", context)

def view_profile(request):
    return render(request, 'Student/showProfile.html', {})

def user_logout(request):
    logout(request)
    return render(request,'accounts/login.html',{})

def Secretary_homepage(request):
    return render(request,"Secretary/homepage.html",{})

def Secretary_edit_profile(request):
    instance=request.user.userprofile
    form= SecretaryProfileForm(instance=instance)
    if request.method == 'POST' :
        form = SecretaryProfileForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/Secretary/homepage/')
    context={'form':form}
    return render(request, "Secretary/editprofile.html", context)

def Secretary_view_profile(request):
    return render(request, "Secretary/showProfile.html", {})

def Secretary_user_logout(request):
    logout(request)
    return render(request,'accounts/login.html',{})

def CCS_homepage(request):
    return render(request,"CCS/homepage.html",{})

def CCS_edit_profile(request):
    instance=request.user.userprofile
    form= CCSProfileForm(instance=instance)
    if request.method == 'POST' :
        form = CCSProfileForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/CCS/homepage/')
    context={'form':form}
    return render(request, "CCS/editprofile.html", context)

def CCS_view_profile(request):
    return render(request, "CCS/showProfile.html", {})

def CCS_user_logout(request):
    logout(request)
    return render(request,'accounts/login.html',{})

def CTS_homepage(request):
    return render(request,"CTS/homepage.html",{})

def CTS_edit_profile(request):
    instance=request.user.userprofile
    form= CTSProfileForm(instance=instance)
    if request.method == 'POST' :
        form = CTSProfileForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/CTS/homepage/')
    context={'form':form}
    return render(request, "CTS/editprofile.html", context)

def CTS_view_profile(request):
    return render(request, "CTS/showProfile.html", {})

def CTS_user_logout(request):
    logout(request)
    return render(request,'accounts/login.html',{})

def CDGC_homepage(request):
    return render(request,"CDGC/homepage.html",{})

def CDGC_edit_profile(request):
    instance=request.user.userprofile
    form= CDGCProfileForm(instance=instance)
    if request.method == 'POST' :
        form = CDGCProfileForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/CDGC/homepage/')
    context={'form':form}
    return render(request, "CDGC/editprofile.html", context)

def CDGC_view_profile(request):
    return render(request, "CDGC/showProfile.html", {})

def CDGC_user_logout(request):
    logout(request)
    return render(request,'accounts/login.html',{})

def CA_homepage(request):
    return render(request,"CA/homepage.html",{})

def CA_edit_profile(request):
    instance=request.user.userprofile
    form= CAProfileForm(instance=instance)
    if request.method == 'POST' :
        form = CAProfileForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/CA/homepage/')
    context={'form':form}
    return render(request, "CA/editprofile.html", context)

def CA_view_profile(request):
    return render(request, "CA/showProfile.html", {})

def CA_user_logout(request):
    logout(request)
    return render(request,'accounts/login.html',{})

def DA_homepage(request):
    return render(request,"DA/homepage.html",{})

def DA_edit_profile(request):
    instance=request.user.userprofile
    form= DAProfileForm(instance=instance)
    if request.method == 'POST' :
        form = DAProfileForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/DA/homepage/')
    context={'form':form}
    return render(request, "DA/editprofile.html", context)

def DA_view_profile(request):
    return render(request, "DA/showProfile.html", {})

def DA_user_logout(request):
    logout(request)
    return render(request,'accounts/login.html',{})

def DSA_homepage(request):
    return render(request,"DSA/homepage.html",{})

def DSA_edit_profile(request):
    instance=request.user.userprofile
    form= DSAProfileForm(instance=instance)
    if request.method == 'POST' :
        form = DSAProfileForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/DSA/homepage/')
    context={'form':form}
    return render(request, "DSA/editprofile.html", context)

def DSA_view_profile(request):
    return render(request, "DSA/showProfile.html", {})

def DSA_user_logout(request):
    logout(request)
    return render(request,'accounts/login.html',{})

def OI_homepage(request):
    return render(request,"OI/homepage.html",{})

def OI_edit_profile(request):
    instance=request.user.userprofile
    form= OIProfileForm(instance=instance)
    if request.method == 'POST' :
        form = OIProfileForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/OI/homepage/')
    context={'form':form}
    return render(request, "OI/editprofile.html", context)

def OI_view_profile(request):
    return render(request, "OI/showProfile.html", {})

def OI_user_logout(request):
    logout(request)
    return render(request,'accounts/login.html',{})

def OISecurity_homepage(request):
    return render(request,"OISecurity/homepage.html",{})

def OISecurity_edit_profile(request):
    instance=request.user.userprofile
    form= OISecurityProfileForm(instance=instance)
    if request.method == 'POST' :
        form = OISecurityProfileForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/OISecurity/homepage/')
    context={'form':form}
    return render(request, "OISecurity/editprofile.html", context)

def OISecurity_view_profile(request):
    return render(request, "OISecurity/showProfile.html", {})

def OISecurity_user_logout(request):
    logout(request)
    return render(request,'accounts/login.html',{})

def HOD_homepage(request):
    return render(request,"HOD/homepage.html",{})

def HOD_edit_profile(request):
    instance=request.user.userprofile
    form= HODProfileForm(instance=instance)
    if request.method == 'POST' :
        form = HODProfileForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/HOD/homepage/')
    context={'form':form}
    return render(request, "HOD/editprofile.html", context)

def HOD_view_profile(request):
    return render(request, "HOD/showProfile.html", {})

def HOD_user_logout(request):
    logout(request)
    return render(request,'accounts/login.html',{})

#reimbursement
def Secretary_Reimbursement_List(request):
    title= 'list of Reimbursement requests'
    queryset=reimbursement.objects.all()
    context={
        "title":title,
        "queryset": queryset,
    }
    return render(request,"Secretary/Reimbursement_List.html",context)

def Secretary_Reimbursement_approve(request, id=None):
    instance = get_object_or_404(reimbursement, id=id)
    form1= reimbursement_personal_Form(request.POST or None, instance=instance)
    form2= reimbursement_event_Form(request.POST or None, instance=instance)
    form3= reimbursement_expenditure_Form(request.POST or None, instance=instance)
    form4= reimbursement_bank_Form(request.POST or None, instance=instance)
    form = reimbursementFormforSecretary(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        if instance.Secretary_approval=='approved':
            if instance.type=='Technical':
                cts=userprofile.objects.filter(role="Chief Technical Society")
                for inst in cts:
                    send_mail('Hello from Student Workshop/Event Management Application!','There is a Reimbursement request for you. This is an automated generated email. So, donot respond to it!',request.user.email,[inst.email], fail_silently=False)
            else:
                ccs=userprofile.objects.filter(role="Chief Cultural Clubs")
                for inst in ccs:
                    send_mail('Hello from Student Workshop/Event Management Application!','There is a Reimbursement request for you. This is an automated generated email. So, donot respond to it!',request.user.email,[inst.email], fail_silently=False)
        elif instance.Secretary_approval=='not approved':
                ca=userprofile.objects.filter(role='Student',user_id=instance.filed_by)
                for inst in ca:
                    send_mail('Hello from Student Workshop/Event Management Application!',
                    'Your Reimbursement request is not approved. This is an automated generated email. So, donot respond to it!',
                    request.user.email,[inst.email], fail_silently=False)
        return HttpResponseRedirect('/Secretary/Reimbursement_List')
    context = {
        "title": 'Approve or Disapprove request for Reimbursement',
        "instance": instance,
        "form1": form1,
        "form2": form2,
        "form3": form3,
        "form4": form4,
        "form": form,}
    return render(request, "Secretary/reimbursement_approve.html", context)

def CCS_Reimbursement_List(request):
    title= 'list of Reimbursement requests'
    queryset=reimbursement.objects.all()
    context={
        "title":title,
        "queryset": queryset,
    }
    return render(request,"CCS/Reimbursement_List.html",context)

def CCS_Reimbursement_approve(request, id=None):
    instance = get_object_or_404(reimbursement, id=id)
    form1 = reimbursement_personal_Form(request.POST or None, instance=instance)
    form2= reimbursement_event_Form(request.POST or None, instance=instance)
    form3= reimbursement_expenditure_Form(request.POST or None, instance=instance)
    form4= reimbursement_bank_Form(request.POST or None, instance=instance)
    form=reimbursementFormforCCS_CTS(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        if instance.CCS_CTS_approval=='approved':
            oi=userprofile.objects.filter(society_or_club_name=instance.name_of_club_or_technical_society,role="O/I(Club/Tech Society/NSS/NCC/Others)")
            for inst in oi:
                send_mail('Hello from Student Workshop/Event Management Application!',
                'There is a Reimbursement request for you. This is an automated generated email. So, donot respond to it!',
                request.user.email,[inst.email], fail_silently=False)
        elif instance.CCS_CTS_approval=='not approved':
                ca=userprofile.objects.filter(role='Student',user_id=instance.filed_by)
                for inst in ca:
                    send_mail('Hello from Student Workshop/Event Management Application!',
                    'Your Reimbursement request is not approved. This is an automated generated email. So, donot respond to it!',
                    request.user.email,[inst.email], fail_silently=False)
        return HttpResponseRedirect('/CCS/Reimbursement_List')
    context = {
        "title": 'Approve or Disapprove request for Reimbursement',
        "instance": instance,
        "form1": form1,
        "form2": form2,
        "form3": form3,
        "form4": form4,
        "form": form,}
    return render(request, "CCS/Reimbursement_approve.html", context)

def CTS_Reimbursement_List(request):
    title= 'list of Reimbursement requests'
    queryset=reimbursement.objects.all()
    context={
        "title":title,
        "queryset": queryset,
    }
    return render(request,"CTS/Reimbursement_List.html",context)

def CTS_Reimbursement_approve(request, id=None):
    instance = get_object_or_404(reimbursement, id=id)
    form1= reimbursement_personal_Form(request.POST or None, instance=instance)
    form2= reimbursement_event_Form(request.POST or None, instance=instance)
    form3= reimbursement_expenditure_Form(request.POST or None, instance=instance)
    form4= reimbursement_bank_Form(request.POST or None, instance=instance)
    form = reimbursementFormforCCS_CTS(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        if instance.CCS_CTS_approval== 'approved':
            oi=userprofile.objects.filter(society_or_club_name=instance.name_of_club_or_technical_society,role="O/I(Club/Tech Society/NSS/NCC/Others)")
            for inst in oi:
                send_mail('Hello from Student Workshop/Event Management Application!',
                'There is a Reimbursement request for you. This is an automated generated email. So, donot respond to it!',
                request.user.email,[inst.email], fail_silently=False)
        elif instance.CCS_CTS_approval=='not approved':
            ca=userprofile.objects.filter(role='Student',user_id=instance.filed_by)
            for inst in ca:
                send_mail('Hello from Student Workshop/Event Management Application!',
                'Your Reimbursement request is not approved. This is an automated generated email. So, donot respond to it!',
                request.user.email,[inst.email], fail_silently=False)
        return HttpResponseRedirect('/CTS/Reimbursement_List')
    context = {
        "title": 'Approve or Disapprove request for Reimbursement',
        "instance": instance,
        "form1": form1,
        "form2": form2,
        "form3": form3,
        "form4": form4,
        "form": form,}
    return render(request, "CTS/Reimbursement_approve.html", context)

def OI_Reimbursement_List(request):
    title= 'list of Reimbursement requests'
    queryset=reimbursement.objects.all()
    context={
        "title":title,
        "queryset": queryset,
    }
    return render(request,"OI/Reimbursement_List.html",context)

def OI_Reimbursement_approve(request, id=None):
    instance = get_object_or_404(reimbursement, id=id)
    form1= reimbursement_personal_Form(request.POST or None, instance=instance)
    form2= reimbursement_event_Form(request.POST or None, instance=instance)
    form3= reimbursement_expenditure_Form(request.POST or None, instance=instance)
    form4= reimbursement_bank_Form(request.POST or None, instance=instance)
    form = reimbursementFormforOI(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        if instance.OI_approval=='approved':
            ca=userprofile.objects.filter(role='Chief Advisor')
            for inst in ca:
                send_mail('Hello from Student Workshop/Event Management Application!',
                'There is a Reimbursement request for you. This is an automated generated email. So, donot respond to it!',
                request.user.email,[inst.email], fail_silently=False)
        elif instance.OI_approval=='not approved':
            ca=userprofile.objects.filter(role='Student',user_id=instance.filed_by)
            for inst in ca:
                send_mail('Hello from Student Workshop/Event Management Application!',
                'Your Reimbursement request is not approved. This is an automated generated email. So, donot respond to it!',
                request.user.email,[inst.email], fail_silently=False)
        return HttpResponseRedirect('/OI/Reimbursement_List')
    context = {
        "title": 'Approve or Disapprove request for Reimbursement',
        "instance": instance,
        "form1": form1,
        "form2": form2,
        "form3": form3,
        "form4": form4,
        "form": form,}
    return render(request, "OI/Reimbursement_approve.html", context)

def CA_Reimbursement_List(request):
    title= 'list of Reimbursement requests'
    queryset=reimbursement.objects.all()
    context={
        "title":title,
        "queryset": queryset,
    }
    return render(request,"CA/Reimbursement_List.html",context)

def CA_Reimbursement_approve(request, id=None):
    instance = get_object_or_404(reimbursement, id=id)
    form1= reimbursement_personal_Form(request.POST or None, instance=instance)
    form2= reimbursement_event_Form(request.POST or None, instance=instance)
    form3= reimbursement_expenditure_Form(request.POST or None, instance=instance)
    form4= reimbursement_bank_Form(request.POST or None, instance=instance)
    form = reimbursementFormforCA(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        if instance.CA_approval=='approved':
            ca=userprofile.objects.filter(role='Dealing Assistant of DSA')
            for inst in ca:
                send_mail('Hello from Student Workshop/Event Management Application!',
                'There is a Reimbursement request for you. This is an automated generated email. So, donot respond to it!',
                request.user.email,[inst.email], fail_silently=False)
        elif instance.CA_approval=='not approved':
            ca=userprofile.objects.filter(role='Student',user_id=instance.filed_by)
            for inst in ca:
                send_mail('Hello from Student Workshop/Event Management Application!',
                'Your Reimbursement request is not approved. This is an automated generated email. So, donot respond to it!',
                request.user.email,[inst.email], fail_silently=False)
        return HttpResponseRedirect('/CA/Reimbursement_List')
    context = {
        "title": 'Approve or Disapprove request for Reimbursement',
        "instance": instance,
        "form1": form1,
        "form2": form2,
        "form3": form3,
        "form4": form4,
        "form": form,}
    return render(request, "CA/Reimbursement_approve.html", context)

def DA_Reimbursement_List(request):
    title= 'list of Reimbursement requests'
    queryset=reimbursement.objects.all()
    context={
        "title":title,
        "queryset": queryset,
    }
    return render(request,"DA/Reimbursement_List.html",context)

def DA_Reimbursement_approve(request, id=None):
    instance = get_object_or_404(reimbursement, id=id)
    form1= reimbursement_personal_Form(request.POST or None, instance=instance)
    form2= reimbursement_event_Form(request.POST or None, instance=instance)
    form3= reimbursement_expenditure_Form(request.POST or None, instance=instance)
    form4= reimbursement_bank_Form(request.POST or None, instance=instance)
    form = reimbursementFormforDA(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        if instance.DA_approval=='approved':
            ca=userprofile.objects.filter(role='Dean Student Affairs')
            for inst in ca:
                send_mail('Hello from Student Workshop/Event Management Application!',
                'There is a Reimbursement request for you. This is an automated generated email. So, donot respond to it!',
                request.user.email,[inst.email], fail_silently=False)
        elif instance.DA_approval=='not approved':
            ca=userprofile.objects.filter(role='Student',user_id=instance.filed_by)
            for inst in ca:
                send_mail('Hello from Student Workshop/Event Management Application!',
                'Your Reimbursement request is not approved. This is an automated generated email. So, donot respond to it!',
                request.user.email,[inst.email], fail_silently=False)
        return HttpResponseRedirect('/DA/Reimbursement_List')
    context = {
        "title": 'Approve or Disapprove request for Reimbursement',
        "instance": instance,
        "form1": form1,
        "form2": form2,
        "form3": form3,
        "form4": form4,
        "form": form,}
    return render(request, "DA/Reimbursement_approve.html", context)

def DSA_Reimbursement_List(request):
    title= 'list of Reimbursement requests'
    queryset=reimbursement.objects.all()
    context={
        "title":title,
        "queryset": queryset,
    }
    return render(request,"DSA/Reimbursement_List.html",context)

def DSA_Reimbursement_approve(request, id=None):
    instance = get_object_or_404(reimbursement, id=id)
    form1= reimbursement_personal_Form(request.POST or None, instance=instance)
    form2= reimbursement_event_Form(request.POST or None, instance=instance)
    form3= reimbursement_expenditure_Form(request.POST or None, instance=instance)
    form4= reimbursement_bank_Form(request.POST or None, instance=instance)
    form = reimbursementFormforDSA(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        if instance.DSA_approval=='approved':
            ca=userprofile.objects.filter(role='Student',user_id=instance.filed_by)
            for inst in ca:
                send_mail('Hello from Student Workshop/Event Management Application!',
                'Your Reimbursement request is approved. This is an automated generated email. So, donot respond to it!',
                request.user.email,[inst.email], fail_silently=False)
        elif instance.DSA_approval=='not approved':
            ca=userprofile.objects.filter(role='Student',user_id=instance.filed_by)
            for inst in ca:
                send_mail('Hello from Student Workshop/Event Management Application!',
                'Your Reimbursement request is not approved. This is an automated generated email. So, donot respond to it!',
                request.user.email,[inst.email], fail_silently=False)
        return HttpResponseRedirect('/DSA/Reimbursement_List')
    context = {
        "title": 'Approve or Disapprove request for Reimbursement',
        "instance": instance,
        "form1": form1,
        "form2": form2,
        "form3": form3,
        "form4": form4,
        "form": form,}
    return render(request, "DSA/Reimbursement_approve.html", context)

def reimbursement_history(request):
    title= 'list of Reimbursement requests'
    queryset=reimbursement.objects.all()
    context={
        "title":title,
        "queryset": queryset,
    }
    return render(request,"Student/reimbursementhistory.html",context)

def Student_reimbursement_approved(request):
    instance = get_object_or_404(reimbursement, id=id)
    form1= reimbursement_personal_Form(request.POST or None, instance=instance)
    form2= reimbursement_event_Form(request.POST or None, instance=instance)
    form3= reimbursement_expenditure_Form(request.POST or None, instance=instance)
    form4= reimbursement_bank_Form(request.POST or None, instance=instance)
    form = reimbursementFormforall(request.POST or None, instance=instance)
    if form.is_valid():
        return HttpResponseRedirect('/Student/reimbursementhistory')
    context = {
        "title": 'Request for Reimbursement got APPROVED!!!!',
        "instance": instance,
        "form": form,}
    return render(request, "Student/Reimbursement_approved.html", context)

#event
def CCS_Event_List(request):
    title= 'list of Event requests'
    queryset=event.objects.all()
    context={
        "title":title,
        "queryset": queryset,
    }
    return render(request,"CCS/Event_List.html",context)

def CCS_Event_approve(request, id=None):
    instance = get_object_or_404(event, id=id)
    form1 = event_detail_Form(request.POST or None, instance=instance)
    form2 = event_expenditure_Form(request.POST or None, instance=instance)
    form3 = event_bank_Form(request.POST or None, instance=instance)
    form  = eventFormforCCS_CTS(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        if instance.CCS_CTS_approval=='approved':
            oi=userprofile.objects.filter(society_or_club_name=instance.name_of_club_or_technical_society,role="O/I(Club/Tech Society/NSS/NCC/Others)")
            for inst in oi:
                send_mail('Hello from Student Workshop/Event Management Application!',
                'There is a event permission request for you. This is an automated generated email. So, donot respond to it!',
                request.user.email,[inst.email], fail_silently=False)
        elif instance.CCS_CTS_approval=='not approved':
                ca=userprofile.objects.filter(user_id=instance.filed_by)
                for inst in ca:
                    send_mail('Hello from Student Workshop/Event Management Application!',
                    'Your event permission request is not approved. This is an automated generated email. So, donot respond to it!',
                    request.user.email,[inst.email], fail_silently=False)
        return HttpResponseRedirect('/CCS/Event_List')
    context = {
        "title": 'Approve or Disapprove request for Event',
        "instance": instance,
        "form1": form1,
        "form2": form2,
        "form3": form3,
        "form": form,}
    return render(request, "CCS/Event_approve.html", context)

def CTS_Event_List(request):
    title= 'list of Event requests'
    queryset=event.objects.all()
    context={
        "title":title,
        "queryset": queryset,
    }
    return render(request,"CTS/Event_List.html",context)

def CTS_Event_approve(request, id=None):
    instance = get_object_or_404(event, id=id)
    form1 = event_detail_Form(request.POST or None, instance=instance)
    form2 = event_expenditure_Form(request.POST or None, instance=instance)
    form3 = event_bank_Form(request.POST or None, instance=instance)
    form  =eventFormforCCS_CTS(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        if instance.CCS_CTS_approval=='approved':
            oi=userprofile.objects.filter(society_or_club_name=instance.name_of_club_or_technical_society,role="O/I(Club/Tech Society/NSS/NCC/Others)")
            for inst in oi:
                send_mail('Hello from Student Workshop/Event Management Application!',
                'There is a event permission request for you. This is an automated generated email. So, donot respond to it!',
                request.user.email,[inst.email], fail_silently=False)
        elif instance.CCS_CTS_approval=='not approved':
                ca=userprofile.objects.filter(user_id=instance.filed_by)
                for inst in ca:
                    send_mail('Hello from Student Workshop/Event Management Application!',
                    'Your event permission request is not approved. This is an automated generated email. So, donot respond to it!',
                    request.user.email,[inst.email], fail_silently=False)
        return HttpResponseRedirect('/CTS/Event_List')
    context = {
        "title": 'Approve or Disapprove request for Event',
        "instance": instance,
        "form1": form1,
        "form2": form2,
        "form3": form3,
        "form": form,}
    return render(request, "CTS/Event_approve.html", context)

def OI_Event_List(request):
    title= 'list of Event requests'
    queryset=event.objects.all()
    context={
        "title":title,
        "queryset": queryset,
    }
    return render(request,"OI/Event_List.html",context)

def OI_Event_approve(request, id=None):
    instance = get_object_or_404(event, id=id)
    form1 = event_detail_Form(request.POST or None, instance=instance)
    form2 = event_expenditure_Form(request.POST or None, instance=instance)
    form3 = event_bank_Form(request.POST or None, instance=instance)
    form  = eventFormforOI(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        if instance.OI_approval=='approved':
            ca=userprofile.objects.filter(role='Chief Advisor')
            for inst in ca:
                send_mail('Hello from Student Workshop/Event Management Application!',
                'There is a event permission request for you. This is an automated generated email. So, donot respond to it!',
                request.user.email,[inst.email], fail_silently=False)
        elif instance.OI_approval=='not approved':
                ca=userprofile.objects.filter(user_id=instance.filed_by)
                for inst in ca:
                    send_mail('Hello from Student Workshop/Event Management Application!',
                    'Your event permission request is not approved. This is an automated generated email. So, donot respond to it!',
                    request.user.email,[inst.email], fail_silently=False)
        return HttpResponseRedirect('/OI/Event_List')
    context = {
        "title": 'Approve or Disapprove request for Event',
        "instance": instance,
        "form1": form1,
        "form2": form2,
        "form3": form3,
        "form": form,}
    return render(request, "OI/Event_approve.html", context)

def CA_Event_List(request):
    title= 'list of Event requests'
    queryset=event.objects.all()
    context={
        "title":title,
        "queryset": queryset,
    }
    return render(request,"CA/Event_List.html",context)

def CA_Event_approve(request, id=None):
    instance = get_object_or_404(event, id=id)
    form1 = event_detail_Form(request.POST or None, instance=instance)
    form2 = event_expenditure_Form(request.POST or None, instance=instance)
    form3 = event_bank_Form(request.POST or None, instance=instance)
    form  = eventFormforCA(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        if instance.CA_approval=='approved':
            ca=userprofile.objects.filter(role='Dealing Assistant of DSA')
            for inst in ca:
                send_mail('Hello from Student Workshop/Event Management Application!',
                'There is a event permission request for you. This is an automated generated email. So, donot respond to it!',
                request.user.email,[inst.email], fail_silently=False)
        elif instance.CA_approval=='not approved':
                ca=userprofile.objects.filter(user_id=instance.filed_by)
                for inst in ca:
                    send_mail('Hello from Student Workshop/Event Management Application!',
                    'Your event permission request is not approved. This is an automated generated email. So, donot respond to it!',
                    request.user.email,[inst.email], fail_silently=False)
        return HttpResponseRedirect('/CA/Event_List')
    context = {
        "title": 'Approve or Disapprove request for Event',
        "instance": instance,
        "form1": form1,
        "form2": form2,
        "form3": form3,
        "form": form,}
    return render(request, "CA/Event_approve.html", context)

def DA_Event_List(request):
    title= 'list of Event requests'
    queryset=event.objects.all()
    context={
        "title":title,
        "queryset": queryset,
    }
    return render(request,"DA/Event_List.html",context)

def DA_Event_approve(request, id=None):
    instance = get_object_or_404(event, id=id)
    form1 = event_detail_Form(request.POST or None, instance=instance)
    form2 = event_expenditure_Form(request.POST or None, instance=instance)
    form3 = event_bank_Form(request.POST or None, instance=instance)
    form  =eventFormforDA(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        if instance.DA_approval=='approved':
            ca=userprofile.objects.filter(role='Dean Student Affairs')
            for inst in ca:
                send_mail('Hello from Student Workshop/Event Management Application!',
                'There is a event permission request for you. This is an automated generated email. So, donot respond to it!',
                request.user.email,[inst.email], fail_silently=False)
        elif instance.DA_approval=='not approved':
                ca=userprofile.objects.filter(user_id=instance.filed_by)
                for inst in ca:
                    send_mail('Hello from Student Workshop/Event Management Application!',
                    'Your event permission request is not approved. This is an automated generated email. So, donot respond to it!',
                    request.user.email,[inst.email], fail_silently=False)
        return HttpResponseRedirect('/DA/Event_List')
    context = {
        "title": 'Approve or Disapprove request for Event',
        "instance": instance,
        "form1": form1,
        "form2": form2,
        "form3": form3,
        "form": form,}
    return render(request, "DA/Event_approve.html", context)

def DSA_Event_List(request):
    title= 'list of Event requests'
    queryset=event.objects.all()
    context={
        "title":title,
        "queryset": queryset,
    }
    return render(request,"DSA/Event_List.html",context)

def DSA_Event_approve(request, id=None):
    instance = get_object_or_404(event, id=id)
    form1 = event_detail_Form(request.POST or None, instance=instance)
    form2 = event_expenditure_Form(request.POST or None, instance=instance)
    form3 = event_bank_Form(request.POST or None, instance=instance)
    form  = eventFormforDSA(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        if instance.DSA_approval=='approved':
            ca=userprofile.objects.filter(user_id=instance.filed_by)
            for inst in ca:
                send_mail('Hello from Student Workshop/Event Management Application!',
                'Your event permission request is approved. This is an automated generated email. So, donot respond to it!',
                request.user.email,[inst.email], fail_silently=False)
        elif instance.DSA_approval=='not approved':
            ca=userprofile.objects.filter(user_id=instance.filed_by)
            for inst in ca:
                send_mail('Hello from Student Workshop/Event Management Application!',
                'Your event permission request is not approved. This is an automated generated email. So, donot respond to it!',
                request.user.email,[inst.email], fail_silently=False)
        return HttpResponseRedirect('/DSA/Event_List')
    context = {
        "title": 'Approve or Disapprove request for Event',
        "instance": instance,
        "form1": form1,
        "form2": form2,
        "form3": form3,
        "form": form,}
    return render(request, "DSA/Event_approve.html", context)

def event_history(request):
    title= 'list of Event requests'
    queryset=event.objects.all()
    context={
        "title":title,
        "queryset": queryset,
    }
    return render(request,"Secretary/eventhistory.html",context)

def event_approved(request, id=None):
    instance = get_object_or_404(event, id=id)
    form1 = event_detail_Form(request.POST or None, instance=instance)
    form2 = event_expenditure_Form(request.POST or None, instance=instance)
    form3 = event_bank_Form(request.POST or None, instance=instance)
    form  =eventFormforAll(request.POST or None, instance=instance)
    if form.is_valid():
        return HttpResponseRedirect('/Secretary/event_history')
    context = {
        "title": 'Request for Event got APPROVED!!!!',
        "instance": instance,
        "form1": form1,
        "form2": form2,
        "form3": form3,
        "form": form,}
    return render(request, "Secretary/Event_approved.html", context)

#auditorium
def OI_Auditorium_List(request):
    title= 'list of Auditorium requests'
    queryset=auditorium.objects.all()
    context={
        "title":title,
        "queryset": queryset,
    }
    return render(request,"OI/Auditorium_List.html",context)

def OI_Auditorium_approve(request, id=None):
    instance = get_object_or_404(auditorium, id=id)
    form1 = auditoriumForm(request.POST or None, instance=instance)
    form = auditoriumFormforOI(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        if instance.OI_approval == 'not approved' :
            instance.progress='dismissed'
        instance.save()
        if instance.OI_approval=='approved':
            ca=userprofile.objects.filter(role='CDGC')
            for inst in ca:
                send_mail('Hello from Student Workshop/Event Management Application!',
                'There is auditorium booking request for you. This is an automated generated email. So, donot respond to it!',
                request.user.email,[inst.email], fail_silently=False)
        elif instance.OI_approval=='not approved':
                ca=userprofile.objects.filter(user_id=instance.filed_by)
                for inst in ca:
                    send_mail('Hello from Student Workshop/Event Management Application!',
                    'Your auditorium booking request is not approved. This is an automated generated email. So, donot respond to it!',
                    request.user.email,[inst.email], fail_silently=False)
        return HttpResponseRedirect('/OI/Auditorium_List')
    context = {
        "title": 'Approve or Disapprove request for Auditorium',
        "instance": instance,
        "form1": form1,
        "form": form,}
    return render(request, "OI/auditorium_approve.html", context)

def CDGC_Auditorium_List(request):
    title= 'list of Auditorium requests'
    queryset=auditorium.objects.all()
    context={
        "title":title,
        "queryset": queryset,
    }
    return render(request,"CDGC/Auditorium_List.html",context)

def CDGC_Auditorium_approve(request, id=None):
    instance = get_object_or_404(auditorium, id=id)
    form1 = auditoriumForm(request.POST or None, instance=instance)
    form = auditoriumFormforCDGC(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        if instance.CDGC_approval == 'not approved' :
            instance.progress='dismissed'
        instance.save()
        if instance.CDGC_approval=='approved':
            ca=userprofile.objects.filter(role='Dealing Assistant of DSA')
            for inst in ca:
                send_mail('Hello from Student Workshop/Event Management Application!',
                'There is auditorium booking request for you. This is an automated generated email. So, donot respond to it!',
                request.user.email,[inst.email], fail_silently=False)
        elif instance.CDGC_approval=='not approved':
                ca=userprofile.objects.filter(user_id=instance.filed_by)
                for inst in ca:
                    send_mail('Hello from Student Workshop/Event Management Application!',
                    'Your auditorium booking request is not approved. This is an automated generated email. So, donot respond to it!',
                    request.user.email,[inst.email], fail_silently=False)
        return HttpResponseRedirect('/CDGC/Auditorium_List')
    context = {
        "title": 'Approve or Disapprove request for Auditorium',
        "instance": instance,
        "form1": form1,
        "form": form,}
    return render(request, "CDGC/auditorium_approve.html", context)

def DA_Auditorium_List(request):
    title= 'list of Auditorium requests'
    queryset=auditorium.objects.all()
    context={
        "title":title,
        "queryset": queryset,
    }
    return render(request,"DA/Auditorium_List.html",context)

def DA_Auditorium_approve(request, id=None):
    instance = get_object_or_404(auditorium, id=id)
    form1 = auditoriumForm(request.POST or None, instance=instance)
    form = auditoriumFormforDA(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        if instance.DA_approval == 'not approved' :
            instance.progress='dismissed'
        instance.save()
        if instance.DA_approval=='approved':
            ca=userprofile.objects.filter(role='Dean Student Affairs')
            for inst in ca:
                send_mail('Hello from Student Workshop/Event Management Application!',
                'There is auditorium booking request for you. This is an automated generated email. So, donot respond to it!',
                request.user.email,[inst.email], fail_silently=False)
        elif instance.DA_approval=='not approved':
                ca=userprofile.objects.filter(user_id=instance.filed_by)
                for inst in ca:
                    send_mail('Hello from Student Workshop/Event Management Application!',
                    'Your auditorium booking request is not approved. This is an automated generated email. So, donot respond to it!',
                    request.user.email,[inst.email], fail_silently=False)
        return HttpResponseRedirect('/DA/Auditorium_List')
    context = {
        "title": 'Approve or Disapprove request for Auditorium',
        "instance": instance,
        "form1": form1,
        "form": form,}
    return render(request, "DA/auditorium_approve.html", context)

def DSA_Auditorium_List(request):
    title= 'list of Auditorium requests'
    queryset=auditorium.objects.all()
    context={
        "title":title,
        "queryset": queryset,
    }
    return render(request,"DSA/Auditorium_List.html",context)

def DSA_Auditorium_approve(request, id=None):
    instance = get_object_or_404(auditorium, id=id)
    form1 = auditoriumForm(request.POST or None, instance=instance)
    form = auditoriumFormforDSA(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        if instance.DSA_approval == 'not approved' :
            instance.progress='dismissed'
        if instance.DSA_approval == 'approved' :
            instance.progress='approved'
        instance.save()
        if instance.DSA_approval=='approved':
            ca=userprofile.objects.filter(user_id=instance.filed_by)
            for inst in ca:
                send_mail('Hello from Student Workshop/Event Management Application!',
                'Your auditorium booking request is approved. This is an automated generated email. So, donot respond to it!',
                request.user.email,[inst.email], fail_silently=False)
        elif instance.DSA_approval=='not approved':
            ca=userprofile.objects.filter(user_id=instance.filed_by)
            for inst in ca:
                send_mail('Hello from Student Workshop/Event Management Application!',
                'Your auditorium booking request is not approved. This is an automated generated email. So, donot respond to it!',
                request.user.email,[inst.email], fail_silently=False)
        return HttpResponseRedirect('/DSA/Auditorium_List')
    context = {
        "title": 'Approve or Disapprove request for Auditorium',
        "instance": instance,
        "form1": form1,
        "form": form,}
    return render(request, "DSA/auditorium_approve.html", context)

def auditorium_history(request):
    title= 'list of Auditorium requests'
    queryset=auditorium.objects.all()
    context={
        "title":title,
        "queryset": queryset,
    }
    return render(request,"Secretary/auditoriumhistory.html",context)

def auditorium_approved(request, id=None):
    instance = get_object_or_404(auditorium, id=id)
    form = auditoriumForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect('/Secretary/Auditorium_approved')
    context = {
        "title": 'Request for Auditorium got APPROVED!!!!',
        "instance": instance,
        "form": form,}
    return render(request, "Secretary/Auditorium_approved.html", context)

#lab
def HOD_Lab_List(request):
    title= 'list of Lab requests'
    queryset=labs.objects.all()
    context={
        "title":title,
        "queryset": queryset,
    }
    return render(request,"HOD/LAB_List.html",context)

def HOD_Lab_approve(request, id=None):
    instance = get_object_or_404(labs, id=id)
    form1 = lab_personal_Form(request.POST or None, instance=instance)
    form2 = lab_details_Form(request.POST or None, instance=instance)
    form = labFormforHOD(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        if instance.HOD_approval == 'not approved' :
            instance.progress='dismissed'
        instance.save()
        if instance.HOD_approval=='approved':
            ca=userprofile.objects.filter(role='Dealing Assistant of DSA')
            for inst in ca:
                send_mail('Hello from Student Workshop/Event Management Application!',
                'There is a lab booking request for you. This is an automated generated email. So, donot respond to it!',
                request.user.email,[inst.email], fail_silently=False)
        elif instance.HOD_approval=='not approved':
            ca=userprofile.objects.filter(role='Student',user_id=instance.filed_by)
            for inst in ca:
                send_mail('Hello from Student Workshop/Event Management Application!',
                'Your lab booking request is not approved. This is an automated generated email. So, donot respond to it!',
                request.user.email,[inst.email], fail_silently=False)
        return HttpResponseRedirect('/HOD/Lab_List')
    context = {
        "title": 'Approve or Disapprove request for Lab',
        "instance": instance,
        "form1": form1,
        "form2": form2,
        "form": form,}
    return render(request, "HOD/Lab_approve.html", context)

def DA_Lab_List(request):
    title= 'list of Lab requests'
    queryset=labs.objects.all()
    context={
        "title":title,
        "queryset": queryset,
    }
    return render(request,"DA/LAB_List.html",context)

def DA_Lab_approve(request, id=None):
    instance = get_object_or_404(labs, id=id)
    form1 = lab_personal_Form(request.POST or None, instance=instance)
    form2 = lab_details_Form(request.POST or None, instance=instance)
    form = labFormforDA(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        if instance.DA_approval == 'not approved' :
            instance.progress='dismissed'
        instance.save()
        if instance.DA_approval=='approved':
            ca=userprofile.objects.filter(role='Dean Student Affairs')
            for inst in ca:
                send_mail('Hello from Student Workshop/Event Management Application!',
                'There is lab booking request for you. This is an automated generated email. So, donot respond to it!',
                request.user.email,[inst.email], fail_silently=False)
        elif instance.DA_approval=='not approved':
            ca=userprofile.objects.filter(role='Student',user_id=instance.filed_by)
            for inst in ca:
                send_mail('Hello from Student Workshop/Event Management Application!',
                'Your lab booking request is not approved. This is an automated generated email. So, donot respond to it!',
                request.user.email,[inst.email], fail_silently=False)
        return HttpResponseRedirect('/DA/Lab_List')
    context = {
        "title": 'Approve or Disapprove request for Lab',
        "instance": instance,
            "form1": form1,
            "form2": form2,
            "form": form,}
    return render(request, "DA/Lab_approve.html", context)

def DSA_Lab_List(request):
    title= 'list of Lab requests'
    queryset=labs.objects.all()
    context={
        "title":title,
        "queryset": queryset,
    }
    return render(request,"DSA/LAB_List.html",context)

def DSA_Lab_approve(request, id=None):
    instance = get_object_or_404(labs, id=id)
    form1 = lab_personal_Form(request.POST or None, instance=instance)
    form2 = lab_details_Form(request.POST or None, instance=instance)
    form = labFormforDSA(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        if instance.DSA_approval == 'not approved' :
            instance.progress='dismissed'
        if instance.DSA_approval == 'approved' :
            instance.progress='approved'
        instance.save()
        if instance.DSA_approval=='approved':
            ca=userprofile.objects.filter(role='Student',user_id=instance.filed_by)
            for inst in ca:
                send_mail('Hello from Student Workshop/Event Management Application!',
                'Your lab booking request is approved. This is an automated generated email. So, donot respond to it!',
                request.user.email,[inst.email], fail_silently=False)
        elif instance.DSA_approval=='not approved':
            ca=userprofile.objects.filter(role='Student',user_id=instance.filed_by)
            for inst in ca:
                send_mail('Hello from Student Workshop/Event Management Application!',
                'Your lab booking request is not approved. This is an automated generated email. So, donot respond to it!',
                request.user.email,[inst.email], fail_silently=False)
        return HttpResponseRedirect('/DSA/Lab_List')
    context = {
        "title": 'Approve or Disapprove request for Lab',
        "instance": instance,
        "form1": form1,
        "form2": form2,
        "form": form,}
    return render(request, "DSA/Lab_approve.html", context)

def lab_history(request):
    title= 'list of LAB requests'
    queryset=labs.objects.all()
    context={
        "title":title,
        "queryset": queryset,
    }
    return render(request,"Student/labhistory.html",context)

def lab_approved(request, id=None):
    instance = get_object_or_404(labs, id=id)
    form1 = lab_personal_Form(request.POST or None, instance=instance)
    form2 = lab_details_Form(request.POST or None, instance=instance)
    form = labFormforAll(request.POST or None, instance=instance)
    if form.is_valid():
        return HttpResponseRedirect('/OISecurity/Lab_history')
    context = {
        "title": 'Request for LAB got APPROVED!!!!',
        "instance": instance,
        "form1": form1,
        "form2": form2,
        "form": form,}
    return render(request, "Student/Lab_approved.html", context)

#lectureHall
def OI_LH_List(request):
    title= 'list for booking of Lecture Halls requests'
    queryset=lecturehalls.objects.all()
    context={
        "title":title,
        "queryset": queryset,
    }
    return render(request,"OI/LH_List.html",context)

def OI_LH_approve(request, id=None):
    instance = get_object_or_404(lecturehalls, id=id)
    form1 = lectureHallForm(request.POST or None, instance=instance)
    form =lectureHallFormForOI(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        if instance.OI_approval == 'not approved' :
            instance.progress='dismissed'
        instance.save()
        if instance.OI_approval=='approved':
            ca=userprofile.objects.filter(role='O/I Securities')
            for inst in ca:
                send_mail('Hello from Student Workshop/Event Management Application!',
                'There is lecture hall booking request for you. This is an automated generated email. So, donot respond to it!',
                request.user.email,[inst.email], fail_silently=False)
        elif instance.OI_approval=='not approved':
                ca=userprofile.objects.filter(user_id=instance.filed_by)
                for inst in ca:
                    send_mail('Hello from Student Workshop/Event Management Application!',
                    'Your lecture hall booking request is not approved. This is an automated generated email. So, donot respond to it!',
                    request.user.email,[inst.email], fail_silently=False)
        return HttpResponseRedirect('/OI/LH_List')
    context = {
        "title": 'Approve or Disapprove request for Lab',
        "instance": instance,
            "form1": form1,
            "form": form,}
    return render(request, "OI/LH_approve.html", context)

def OISecurity_LH_List(request):
    title= 'list for booking of Lecture Halls requests'
    queryset=lecturehalls.objects.all()
    context={
        "title":title,
        "queryset": queryset,
    }
    return render(request,"OISecurity/LH_List.html",context)

def OISecurity_LH_approve(request, id=None):
    instance = get_object_or_404(lecturehalls, id=id)
    form1 = lectureHallForm(request.POST or None, instance=instance)
    form = lectureHallFormForOISecurity(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        if instance.OISecurity_approval == 'not approved' :
            instance.progress='dismissed'
        if instance.OISecurity_approval == 'approved' :
            instance.progress='approved'
        instance.save()
        if instance.OISecurity_approval=='approved':
            ca=userprofile.objects.filter(user_id=instance.filed_by)
            for inst in ca:
                send_mail('Hello from Student Workshop/Event Management Application!',
                'Your lecture hall booking request is approved. This is an automated generated email. So, donot respond to it!',
                request.user.email,[inst.email], fail_silently=False)
        elif instance.OISecurity_approval=='not approved':
            ca=userprofile.objects.filter(user_id=instance.filed_by)
            for inst in ca:
                send_mail('Hello from Student Workshop/Event Management Application!',
                'Your lecture hall booking request is not approved. This is an automated generated email. So, donot respond to it!',
                request.user.email,[inst.email], fail_silently=False)
        return HttpResponseRedirect('/OISecurity/LH_List')
    context = {
        "title": 'Approve or Disapprove request for Lab',
        "instance": instance,
        "form1": form1,
        "form": form,}
    return render(request, "OISecurity/LH_approve.html", context)

def LH_history(request):
    title= 'list of booked lecture hall requests.'
    queryset=lecturehalls.objects.all()
    context={
        "title":title,
        "queryset": queryset,
    }
    return render(request,"Secretary/LHhistory.html",context)

def Secretary_LH_approved(request, id=None):
    instance = get_object_or_404(lecturehalls, id=id)
    form1 = lectureHallForm(request.POST or None, instance=instance)
    form = lectureHallFormForAll(request.POST or None, instance=instance)
    if form.is_valid():
        return HttpResponseRedirect('/Secretary/LH_history')
    context = {
        "title": 'Request for LAB got APPROVED!!!!',
        "instance": instance,
        "form1": form1,
        "form": form,}
    return render(request, "Secretary/LH_approved.html", context)
