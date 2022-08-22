from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm
from account.models import userprofile,reimbursement,event,auditorium,lecturehalls,labs

class UserProfileForm(ModelForm):
    class Meta:
        model=userprofile
        fields=['full_name','sid','branch','year','gender','DOB','email','mobile_number','profile_pic']

class reimbursement_Form(ModelForm):
    class Meta:
        model=reimbursement
        exclude = ['Secretary_approval','OI_approval','CA_approval','DA_approval','DSA_approval','reason_for_disapproval']

class reimbursement_personal_Form(ModelForm):
    class Meta:
        model=reimbursement
        fields= ['full_name','sid','branch','year','mobile_number','email']

class reimbursement_event_Form(ModelForm):
    class Meta:
        model=reimbursement
        fields= ['name_of_club_or_technical_society','type','event_name','institute','dates_for_which_team_will_be_away_from','dates_for_which_team_will_be_away_to','date_of_event_from','date_of_event_to','brief_event_description']

class reimbursement_expenditure_Form(ModelForm):
    class Meta:
        model=reimbursement
        fields= ['mode_of_travel','attach_bills','accomodation_or_food','attach_proofs','total_expenditure']

class reimbursement_bank_Form(ModelForm):
    class Meta:
        model=reimbursement
        fields= ['account_holder_name','account_number','IFSC_code','PAN_card_number']

class reimbursementFormforAll(ModelForm):
    class Meta:
        model=reimbursement
        fields= ['Secretary_approval','OI_approval','CA_approval','DA_approval','DSA_approval','reason_for_disapproval']

class reimbursementFormforSecretary(ModelForm):
    class Meta:
        model=reimbursement
        fields= ['Secretary_approval','reason_for_disapproval']
    def clean(self):
        approval=self.cleaned_data.get('Secretary_approval')
        reason_for_disapproval=self.cleaned_data.get('reason_for_disapproval')
        if approval=='not approved' and not reason_for_disapproval:
            msg=forms.ValidationError("This field is required!")
            self.add_error('reason_for_disapproval',msg)
        return self.cleaned_data

class reimbursementFormforCCS_CTS(ModelForm):
    class Meta:
        model=reimbursement
        fields= ['Secretary_approval','CCS_CTS_approval','reason_for_disapproval']
    def clean(self):
        approval=self.cleaned_data.get('CCS_CTS_approval')
        reason_for_disapproval=self.cleaned_data.get('reason_for_disapproval')
        if approval=='not approved' and not reason_for_disapproval:
            msg=forms.ValidationError("This field is required!")
            self.add_error('reason_for_disapproval',msg)
        return self.cleaned_data

class reimbursementFormforOI(ModelForm):
    class Meta:
        model=reimbursement
        fields= ['Secretary_approval','CCS_CTS_approval','OI_approval','reason_for_disapproval']
    def clean(self):
        approval=self.cleaned_data.get('OI_approval')
        reason_for_disapproval=self.cleaned_data.get('reason_for_disapproval')
        if approval=='not approved' and not reason_for_disapproval:
            msg=forms.ValidationError("This field is required!")
            self.add_error('reason_for_disapproval',msg)
        return self.cleaned_data

class reimbursementFormforCA(ModelForm):
    class Meta:
        model=reimbursement
        fields= ['Secretary_approval','CCS_CTS_approval','OI_approval','CA_approval','reason_for_disapproval']
    def clean(self):
        approval=self.cleaned_data.get('CA_approval')
        reason_for_disapproval=self.cleaned_data.get('reason_for_disapproval')
        if approval=='not approved' and not reason_for_disapproval:
            msg=forms.ValidationError("This field is required!")
            self.add_error('reason_for_disapproval',msg)
        return self.cleaned_data

class reimbursementFormforDA(ModelForm):
    class Meta:
        model=reimbursement
        fields= ['Secretary_approval','CCS_CTS_approval','OI_approval','CA_approval','DA_approval','reason_for_disapproval']
    def clean(self):
        approval=self.cleaned_data.get('DA_approval')
        reason_for_disapproval=self.cleaned_data.get('reason_for_disapproval')
        if approval=='not approved' and not reason_for_disapproval:
            msg=forms.ValidationError("This field is required!")
            self.add_error('reason_for_disapproval',msg)
        return self.cleaned_data

class reimbursementFormforDSA(ModelForm):
    class Meta:
        model=reimbursement
        fields= ['Secretary_approval','CCS_CTS_approval','OI_approval','CA_approval','DA_approval','DSA_approval','reason_for_disapproval']
    def clean(self):
        approval=self.cleaned_data.get('DSA_approval')
        reason_for_disapproval=self.cleaned_data.get('reason_for_disapproval')
        if approval=='not approved' and not reason_for_disapproval:
            msg=forms.ValidationError("This field is required!")
            self.add_error('reason_for_disapproval',msg)
        return self.cleaned_data

class lab_Form(ModelForm):
    class Meta:
        model=labs
        exclude=['filed_by','reason_for_disapproval']
    def clean(self):
        place=self.cleaned_data.get('place')
        date_from=self.cleaned_data.get('date_from')
        date_to=self.cleaned_data.get('date_to')
        time_from=self.cleaned_data.get('time_from')
        time_to=self.cleaned_data.get('time_to')
        if place!=None and date_from!=None and date_to!=None and time_to!=None and time_from!=None:
            if (labs.objects.filter(date_from__lte=date_from,date_to__lte=date_to,date_to__gte=date_from,time_to__lte=time_to,time_from__gte=time_from,place__exact=place,progress__exact='in-progress')
            or labs.objects.filter(date_to__gte=date_to,date_from__gte=date_from,date_from__lte=date_to,time_to__lte=time_to,time_from__gte=time_from,place__exact=place,progress__exact='in-progress')
            or labs.objects.filter(date_to__gte=date_to,date_from__lte=date_from,time_to__lte=time_to,time_from__gte=time_from,place__exact=place,progress__exact='in-progress')
            or labs.objects.filter(date_to__lte=date_to,date_from__gte=date_from,time_to__lte=time_to,time_from__gte=time_from,place__exact=place,progress__exact='in-progress')
            or labs.objects.filter(date_to__lte=date_to,date_from__gte=date_from,time_from__lte=time_from,time_to__lte=time_to,time_to__gte=time_from,place__exact=place,progress__exact='in-progress')
            or labs.objects.filter(date_to__lte=date_to,date_from__gte=date_from,time_to__gte=time_to,time_from__gte=time_from,time_from__lte=time_to,place__exact=place,progress__exact='in-progress')
            or labs.objects.filter(date_to__lte=date_to,date_from__gte=date_from,time_to__gte=time_to,time_from__lte=time_from,place__exact=place,progress__exact='in-progress')
            or labs.objects.filter(date_to__lte=date_to,date_from__gte=date_from,time_from__lte=time_from,time_to__lte=time_to,time_to__gte=time_from,place__exact=place,progress__exact='approved')
            or labs.objects.filter(date_to__lte=date_to,date_from__gte=date_from,time_to__gte=time_to,time_from__gte=time_from,time_from__lte=time_to,place__exact=place,progress__exact='approved')
            or labs.objects.filter(date_to__lte=date_to,date_from__gte=date_from,time_to__gte=time_to,time_from__lte=time_from,place__exact=place,progress__exact='approved')
            or labs.objects.filter(date_from__lte=date_from,date_to__lte=date_to,date_to__gte=date_from,time_from__lte=time_from,time_to__lte=time_to,time_to__gte=time_from,place__exact=place,progress__exact='in-progress')
            or labs.objects.filter(date_from__lte=date_from,date_to__lte=date_to,date_to__gte=date_from,time_to__gte=time_to,time_from__gte=time_from,time_from__lte=time_to,place__exact=place,progress__exact='in-progress')
            or labs.objects.filter(date_from__lte=date_from,date_to__lte=date_to,date_to__gte=date_from,time_to__gte=time_to,time_from__lte=time_from,place__exact=place,progress__exact='in-progress')
            or labs.objects.filter(date_to__gte=date_to,date_from__gte=date_from,date_from__lte=date_to,time_from__lte=time_from,time_to__lte=time_to,time_to__gte=time_from,place__exact=place,progress__exact='in-progress')
            or labs.objects.filter(date_to__gte=date_to,date_from__gte=date_from,date_from__lte=date_to,time_to__gte=time_to,time_from__gte=time_from,time_from__lte=time_to,place__exact=place,progress__exact='in-progress')
            or labs.objects.filter(date_to__gte=date_to,date_from__gte=date_from,date_from__lte=date_to,time_to__gte=time_to,time_from__lte=time_from,place__exact=place,progress__exact='in-progress')
            or labs.objects.filter(date_to__gte=date_to,date_from__lte=date_from,time_from__lte=time_from,time_to__lte=time_to,time_to__gte=time_from,place__exact=place,progress__exact='in-progress')
            or labs.objects.filter(date_to__gte=date_to,date_from__lte=date_from,time_to__gte=time_to,time_from__gte=time_from,time_from__lte=time_to,place__exact=place,progress__exact='in-progress')
            or labs.objects.filter(date_to__gte=date_to,date_from__lte=date_from,time_to__gte=time_to,time_from__lte=time_from,place__exact=place,progress__exact='in-progress')
            or labs.objects.filter(date_from__lte=date_from,date_to__lte=date_to,date_to__gte=date_from,time_to__lte=time_to,time_from__gte=time_from,place__exact=place,progress__exact='approved')
            or labs.objects.filter(date_to__gte=date_to,date_from__gte=date_from,date_from__lte=date_to,time_to__lte=time_to,time_from__gte=time_from,place__exact=place,progress__exact='approved')
            or labs.objects.filter(date_to__gte=date_to,date_from__lte=date_from,time_to__lte=time_to,time_from__gte=time_from,place__exact=place,progress__exact='approved')
            or labs.objects.filter(date_to__lte=date_to,date_from__gte=date_from,time_to__lte=time_to,time_from__gte=time_from,place__exact=place,progress__exact='approved')
            or labs.objects.filter(date_from__lte=date_from,date_to__lte=date_to,date_to__gte=date_from,time_from__lte=time_from,time_to__lte=time_to,time_to__gte=time_from,place__exact=place,progress__exact='approved')
            or labs.objects.filter(date_from__lte=date_from,date_to__lte=date_to,date_to__gte=date_from,time_to__gte=time_to,time_from__gte=time_from,time_from__lte=time_to,place__exact=place,progress__exact='approved')
            or labs.objects.filter(date_from__lte=date_from,date_to__lte=date_to,date_to__gte=date_from,time_to__gte=time_to,time_from__lte=time_from,place__exact=place,progress__exact='approved')
            or labs.objects.filter(date_to__gte=date_to,date_from__gte=date_from,date_from__lte=date_to,time_from__lte=time_from,time_to__lte=time_to,time_to__gte=time_from,place__exact=place,progress__exact='approved')
            or labs.objects.filter(date_to__gte=date_to,date_from__gte=date_from,date_from__lte=date_to,time_to__gte=time_to,time_from__gte=time_from,time_from__lte=time_to,place__exact=place,progress__exact='approved')
            or labs.objects.filter(date_to__gte=date_to,date_from__gte=date_from,date_from__lte=date_to,time_to__gte=time_to,time_from__lte=time_from,place__exact=place,progress__exact='approved')
            or labs.objects.filter(date_to__gte=date_to,date_from__lte=date_from,time_from__lte=time_from,time_to__lte=time_to,time_to__gte=time_from,place__exact=place,progress__exact='approved')
            or labs.objects.filter(date_to__gte=date_to,date_from__lte=date_from,time_to__gte=time_to,time_from__gte=time_from,time_from__lte=time_to,place__exact=place,progress__exact='approved')
            or labs.objects.filter(date_to__gte=date_to,date_from__lte=date_from,time_to__gte=time_to,time_from__lte=time_from,place__exact=place,progress__exact='approved')):
                msg=forms.ValidationError('This venue is already booked or in progress!')
                self.add_error('place',msg)
        return self.cleaned_data

class lab_personal_Form(ModelForm):
    class Meta:
        model=labs
        fields= ['full_name','sid','branch','year','mobile_number','email']

class lab_details_Form(ModelForm):
    class Meta:
        model=labs
        fields= ['place','department_related_to_project','date_from','date_to','time_from','time_to','brief_project_description','project_report']

class labFormforAll(ModelForm):
    class Meta:
        model=labs
        fields= ['HOD_approval','DA_approval','DSA_approval','reason_for_disapproval']

class labFormforHOD(ModelForm):
    class Meta:
        model=labs
        fields= ['HOD_approval','reason_for_disapproval']
    def clean(self):
        approval=self.cleaned_data.get('HOD_approval')
        reason_for_disapproval=self.cleaned_data.get('reason_for_disapproval')
        if approval=='not approved' and not reason_for_disapproval:
            msg=forms.ValidationError("This field is required!")
            self.add_error('reason_for_disapproval',msg)
        else:
            self.cleaned_data['reason_for_disapproval']=''
        return self.cleaned_data

class labFormforDA(ModelForm):
    class Meta:
        model=labs
        fields= ['HOD_approval','DA_approval','reason_for_disapproval']
    def clean(self):
        approval=self.cleaned_data.get('DA_approval')
        reason_for_disapproval=self.cleaned_data.get('reason_for_disapproval')
        if approval=='not approved' and not reason_for_disapproval:
            msg=forms.ValidationError("This field is required!")
            self.add_error('reason_for_disapproval',msg)
        return self.cleaned_data

class labFormforDSA(ModelForm):
    class Meta:
        model=labs
        fields= ['HOD_approval','DA_approval','DSA_approval','reason_for_disapproval']
    def clean(self):
        approval=self.cleaned_data.get('DSA_approval')
        reason_for_disapproval=self.cleaned_data.get('reason_for_disapproval')
        if approval=='not approved' and not reason_for_disapproval:
            msg=forms.ValidationError("This field is required!")
            self.add_error('reason_for_disapproval',msg)
        return self.cleaned_data

class event_detail_Form(ModelForm):
    class Meta:
        model=event
        fields=['name_of_club_or_technical_society','type','secretary_name','secretary_SID','event_name','date_of_event_from','date_of_event_to','time_of_event_from','time_of_event_to','venues','brief_event_description']

class event_expenditure_Form(ModelForm):
    class Meta:
        model=event
        fields=['expected_expenditure_description','total_expected_expenditure','advance_required','advance_required_justification','advance_amount']
    def clean(self):
        approval=self.cleaned_data.get('advance_required')
        if approval:
            msg=forms.ValidationError("This field is required!")
            self.add_error('advance_required_justification',msg)
            self.add_error('advance_amount',msg)
        else:
            self.cleaned_data['advance_required_justification']=''
            self.cleaned_data['advance_amount']=0
        return self.cleaned_data

class event_bank_Form(ModelForm):
    class Meta:
        model=event
        fields=['account_holder_name','account_number','IFSC_code','PAN_card_number']

class eventFormforCCS_CTS(ModelForm):
    class Meta:
        model=event
        fields=['CCS_CTS_approval','reason_for_disapproval']
    def clean(self):
        approval=self.cleaned_data.get('CCS_CTS_approval')
        reason_for_disapproval=self.cleaned_data.get('reason_for_disapproval')
        if approval=='not approved' and not reason_for_disapproval:
            msg=forms.ValidationError("This field is required!")
            self.add_error('reason_for_disapproval',msg)
        return self.cleaned_data

class eventFormforAll(ModelForm):
    class Meta:
        model=event
        fields=['OI_approval','CCS_CTS_approval','CA_approval','DA_approval','DSA_approval','reason_for_disapproval']

class eventFormforOI(ModelForm):
    class Meta:
        model=event
        fields=['CCS_CTS_approval','OI_approval','reason_for_disapproval']
    def clean(self):
        approval=self.cleaned_data.get('OI_approval')
        reason_for_disapproval=self.cleaned_data.get('reason_for_disapproval')
        if approval=='not approved' and not reason_for_disapproval:
            msg=forms.ValidationError("This field is required!")
            self.add_error('reason_for_disapproval',msg)
        return self.cleaned_data

class eventFormforCA(ModelForm):
    class Meta:
        model=event
        fields=['CCS_CTS_approval','OI_approval','CA_approval','reason_for_disapproval']
    def clean(self):
        approval=self.cleaned_data.get('CA_approval')
        reason_for_disapproval=self.cleaned_data.get('reason_for_disapproval')
        if approval=='not approved' and not reason_for_disapproval:
            msg=forms.ValidationError("This field is required!")
            self.add_error('reason_for_disapproval',msg)
        return self.cleaned_data

class eventFormforDA(ModelForm):
    class Meta:
        model=event
        fields=['CCS_CTS_approval','OI_approval','CA_approval','DA_approval','reason_for_disapproval']
    def clean(self):
        approval=self.cleaned_data.get('DA_approval')
        reason_for_disapproval=self.cleaned_data.get('reason_for_disapproval')
        if approval=='not approved' and not reason_for_disapproval:
            msg=forms.ValidationError("This field is required!")
            self.add_error('reason_for_disapproval',msg)
        return self.cleaned_data

class eventFormforDSA(ModelForm):
    class Meta:
        model=event
        fields=['CCS_CTS_approval','OI_approval','CA_approval','DA_approval','DSA_approval','reason_for_disapproval']
    def clean(self):
        approval=self.cleaned_data.get('DSA_approval')
        reason_for_disapproval=self.cleaned_data.get('reason_for_disapproval')
        if approval=='not approved' and not reason_for_disapproval:
            msg=forms.ValidationError("This field is required!")
            self.add_error('reason_for_disapproval',msg)
        return self.cleaned_data


class auditoriumForm(ModelForm):
    class Meta:
        model=auditorium
        exclude=['filed_by','OI_approval','CDGC_approval','DA_approval','DSA_approval','reason_for_disapproval','progress']
    def clean(self):
        date=self.cleaned_data.get('date')
        time_from=self.cleaned_data.get('time_from')
        time_to=self.cleaned_data.get('time_to')
        if date!=None and time_to!=None and time_from!=None:
            if (auditorium.objects.filter(date__exact=date,time_from__lte=time_from,time_to__lte=time_to,time_to__gte=time_from,progress__exact='in-progress')
                or auditorium.objects.filter(date__exact=date,time_to__gte=time_to,time_from__gte=time_from,time_from__lte=time_to,progress__exact='in-progress')
                or auditorium.objects.filter(date__exact=date,time_to__lte=time_to,time_from__gte=time_from,progress__exact='in-progress')
                or auditorium.objects.filter(date__exact=date,time_to__gte=time_to,time_from__lte=time_from,progress__exact='in-progress')
                or auditorium.objects.filter(date__exact=date,time_from__lte=time_from,time_to__lte=time_to,time_to__gte=time_from,progress__exact='approved')
                or auditorium.objects.filter(date__exact=date,time_to__gte=time_to,time_from__gte=time_from,time_from__lte=time_to,progress__exact='approved')
                or auditorium.objects.filter(date__exact=date,time_to__gte=time_to,time_from__lte=time_from,progress__exact='approved')
                or auditorium.objects.filter(date__exact=date,time_to__lte=time_to,time_from__gte=time_from,progress__exact='approved')):
                msg=forms.ValidationError('This venue is already booked or in progress!')
                self.add_error('date',msg)
        return self.cleaned_data

class auditoriumFormforAll(ModelForm):
    class Meta:
        model=auditorium
        fields= ['OI_approval','CDGC_approval','DA_approval','DSA_approval','reason_for_disapproval']

class auditoriumFormforOI(ModelForm):
    class Meta:
        model=auditorium
        fields=['OI_approval','reason_for_disapproval']
    def clean(self):
        approval=self.cleaned_data.get('OI_approval')
        reason_for_disapproval=self.cleaned_data.get('reason_for_disapproval')
        if approval=='not approved' and not reason_for_disapproval:
            msg=forms.ValidationError("This field is required!")
            self.add_error('reason_for_disapproval',msg)
        return self.cleaned_data

class auditoriumFormforCDGC(ModelForm):
    class Meta:
        model=auditorium
        fields=['OI_approval','CDGC_approval','reason_for_disapproval']
    def clean(self):
        approval=self.cleaned_data.get('CDGC_approval')
        reason_for_disapproval=self.cleaned_data.get('reason_for_disapproval')
        if approval=='not approved' and not reason_for_disapproval:
            msg=forms.ValidationError("This field is required!")
            self.add_error('reason_for_disapproval',msg)
        return self.cleaned_data

class auditoriumFormforDA(ModelForm):
    class Meta:
        model=auditorium
        fields=['OI_approval','CDGC_approval','DA_approval','reason_for_disapproval']
    def clean(self):
        approval=self.cleaned_data.get('DA_approval')
        reason_for_disapproval=self.cleaned_data.get('reason_for_disapproval')
        if approval=='not approved' and not reason_for_disapproval:
            msg=forms.ValidationError("This field is required!")
            self.add_error('reason_for_disapproval',msg)
        return self.cleaned_data

class auditoriumFormforDSA(ModelForm):
    class Meta:
        model=auditorium
        fields=['OI_approval','CDGC_approval','DA_approval','DSA_approval','reason_for_disapproval']
    def clean(self):
        approval=self.cleaned_data.get('DSA_approval')
        reason_for_disapproval=self.cleaned_data.get('reason_for_disapproval')
        if approval=='not approved' and not reason_for_disapproval:
            msg=forms.ValidationError("This field is required!")
            self.add_error('reason_for_disapproval',msg)
        return self.cleaned_data

class lectureHallForm(ModelForm):
    class Meta:
        model=lecturehalls
        exclude=['filed_by','OI_approval','OISecurity_approval','reason_for_disapproval','progress']
    def clean(self):
        place=self.cleaned_data.get('place')
        date_from=self.cleaned_data.get('date_from')
        date_to=self.cleaned_data.get('date_to')
        time_from=self.cleaned_data.get('time_from')
        time_to=self.cleaned_data.get('time_to')
        if place!=None and date_from!=None and date_to!=None and time_to!=None and time_from!=None:
            if (lecturehalls.objects.filter(date_from__lte=date_from,date_to__lte=date_to,date_to__gte=date_from,time_to__lte=time_to,time_from__gte=time_from,place__exact=place,progress__exact='in-progress')
            or lecturehalls.objects.filter(date_to__gte=date_to,date_from__gte=date_from,date_from__lte=date_to,time_to__lte=time_to,time_from__gte=time_from,place__exact=place,progress__exact='in-progress')
            or lecturehalls.objects.filter(date_to__gte=date_to,date_from__lte=date_from,time_to__lte=time_to,time_from__gte=time_from,place__exact=place,progress__exact='in-progress')
            or lecturehalls.objects.filter(date_to__lte=date_to,date_from__gte=date_from,time_to__lte=time_to,time_from__gte=time_from,place__exact=place,progress__exact='in-progress')
            or lecturehalls.objects.filter(date_to__lte=date_to,date_from__gte=date_from,time_from__lte=time_from,time_to__lte=time_to,time_to__gte=time_from,place__exact=place,progress__exact='in-progress')
            or lecturehalls.objects.filter(date_to__lte=date_to,date_from__gte=date_from,time_to__gte=time_to,time_from__gte=time_from,time_from__lte=time_to,place__exact=place,progress__exact='in-progress')
            or lecturehalls.objects.filter(date_to__lte=date_to,date_from__gte=date_from,time_to__gte=time_to,time_from__lte=time_from,place__exact=place,progress__exact='in-progress')
            or lecturehalls.objects.filter(date_to__lte=date_to,date_from__gte=date_from,time_from__lte=time_from,time_to__lte=time_to,time_to__gte=time_from,place__exact=place,progress__exact='approved')
            or lecturehalls.objects.filter(date_to__lte=date_to,date_from__gte=date_from,time_to__gte=time_to,time_from__gte=time_from,time_from__lte=time_to,place__exact=place,progress__exact='approved')
            or lecturehalls.objects.filter(date_to__lte=date_to,date_from__gte=date_from,time_to__gte=time_to,time_from__lte=time_from,place__exact=place,progress__exact='approved')
            or lecturehalls.objects.filter(date_from__lte=date_from,date_to__lte=date_to,date_to__gte=date_from,time_from__lte=time_from,time_to__lte=time_to,time_to__gte=time_from,place__exact=place,progress__exact='in-progress')
            or lecturehalls.objects.filter(date_from__lte=date_from,date_to__lte=date_to,date_to__gte=date_from,time_to__gte=time_to,time_from__gte=time_from,time_from__lte=time_to,place__exact=place,progress__exact='in-progress')
            or lecturehalls.objects.filter(date_from__lte=date_from,date_to__lte=date_to,date_to__gte=date_from,time_to__gte=time_to,time_from__lte=time_from,place__exact=place,progress__exact='in-progress')
            or lecturehalls.objects.filter(date_to__gte=date_to,date_from__gte=date_from,date_from__lte=date_to,time_from__lte=time_from,time_to__lte=time_to,time_to__gte=time_from,place__exact=place,progress__exact='in-progress')
            or lecturehalls.objects.filter(date_to__gte=date_to,date_from__gte=date_from,date_from__lte=date_to,time_to__gte=time_to,time_from__gte=time_from,time_from__lte=time_to,place__exact=place,progress__exact='in-progress')
            or lecturehalls.objects.filter(date_to__gte=date_to,date_from__gte=date_from,date_from__lte=date_to,time_to__gte=time_to,time_from__lte=time_from,place__exact=place,progress__exact='in-progress')
            or lecturehalls.objects.filter(date_to__gte=date_to,date_from__lte=date_from,time_from__lte=time_from,time_to__lte=time_to,time_to__gte=time_from,place__exact=place,progress__exact='in-progress')
            or lecturehalls.objects.filter(date_to__gte=date_to,date_from__lte=date_from,time_to__gte=time_to,time_from__gte=time_from,time_from__lte=time_to,place__exact=place,progress__exact='in-progress')
            or lecturehalls.objects.filter(date_to__gte=date_to,date_from__lte=date_from,time_to__gte=time_to,time_from__lte=time_from,place__exact=place,progress__exact='in-progress')
            or lecturehalls.objects.filter(date_from__lte=date_from,date_to__lte=date_to,date_to__gte=date_from,time_to__lte=time_to,time_from__gte=time_from,place__exact=place,progress__exact='approved')
            or lecturehalls.objects.filter(date_to__gte=date_to,date_from__gte=date_from,date_from__lte=date_to,time_to__lte=time_to,time_from__gte=time_from,place__exact=place,progress__exact='approved')
            or lecturehalls.objects.filter(date_to__gte=date_to,date_from__lte=date_from,time_to__lte=time_to,time_from__gte=time_from,place__exact=place,progress__exact='approved')
            or lecturehalls.objects.filter(date_to__lte=date_to,date_from__gte=date_from,time_to__lte=time_to,time_from__gte=time_from,place__exact=place,progress__exact='approved')
            or lecturehalls.objects.filter(date_from__lte=date_from,date_to__lte=date_to,date_to__gte=date_from,time_from__lte=time_from,time_to__lte=time_to,time_to__gte=time_from,place__exact=place,progress__exact='approved')
            or lecturehalls.objects.filter(date_from__lte=date_from,date_to__lte=date_to,date_to__gte=date_from,time_to__gte=time_to,time_from__gte=time_from,time_from__lte=time_to,place__exact=place,progress__exact='approved')
            or lecturehalls.objects.filter(date_from__lte=date_from,date_to__lte=date_to,date_to__gte=date_from,time_to__gte=time_to,time_from__lte=time_from,place__exact=place,progress__exact='approved')
            or lecturehalls.objects.filter(date_to__gte=date_to,date_from__gte=date_from,date_from__lte=date_to,time_from__lte=time_from,time_to__lte=time_to,time_to__gte=time_from,place__exact=place,progress__exact='approved')
            or lecturehalls.objects.filter(date_to__gte=date_to,date_from__gte=date_from,date_from__lte=date_to,time_to__gte=time_to,time_from__gte=time_from,time_from__lte=time_to,place__exact=place,progress__exact='approved')
            or lecturehalls.objects.filter(date_to__gte=date_to,date_from__gte=date_from,date_from__lte=date_to,time_to__gte=time_to,time_from__lte=time_from,place__exact=place,progress__exact='approved')
            or lecturehalls.objects.filter(date_to__gte=date_to,date_from__lte=date_from,time_from__lte=time_from,time_to__lte=time_to,time_to__gte=time_from,place__exact=place,progress__exact='approved')
            or lecturehalls.objects.filter(date_to__gte=date_to,date_from__lte=date_from,time_to__gte=time_to,time_from__gte=time_from,time_from__lte=time_to,place__exact=place,progress__exact='approved')
            or lecturehalls.objects.filter(date_to__gte=date_to,date_from__lte=date_from,time_to__gte=time_to,time_from__lte=time_from,place__exact=place,progress__exact='approved')):
                msg=forms.ValidationError('This venue is already booked or in progress!')
                self.add_error('place',msg)
        return self.cleaned_data


class lectureHallFormForAll(ModelForm):
    class Meta:
        model=lecturehalls
        fields=['OI_approval','OISecurity_approval','reason_for_disapproval']

class lectureHallFormForOI(ModelForm):
    class Meta:
        model=lecturehalls
        fields=['OI_approval','reason_for_disapproval']
    def clean(self):
        approval=self.cleaned_data.get('OI_approval')
        reason_for_disapproval=self.cleaned_data.get('reason_for_disapproval')
        if approval=='not approved' and not reason_for_disapproval:
            msg=forms.ValidationError("This field is required!")
            self.add_error('reason_for_disapproval',msg)
        return self.cleaned_data

class lectureHallFormForOISecurity(ModelForm):
    class Meta:
        model=lecturehalls
        fields=['OI_approval','OISecurity_approval','reason_for_disapproval']
    def clean(self):
        approval=self.cleaned_data.get('OISecurity_approval')
        reason_for_disapproval=self.cleaned_data.get('reason_for_disapproval')
        if approval=='not approved' and not reason_for_disapproval:
            msg=forms.ValidationError("This field is required!")
            self.add_error('reason_for_disapproval',msg)
        return self.cleaned_data



class SecretaryProfileForm(ModelForm):
    class Meta:
        model=userprofile
        fields=['full_name','society_or_club_name','sid','branch','gender','DOB','email','mobile_number','profile_pic']

class CAProfileForm(ModelForm):
    class Meta:
        model=userprofile
        fields=['full_name','department','gender','DOB','email','mobile_number','profile_pic']

class CTSProfileForm(ModelForm):
    class Meta:
        model=userprofile
        fields=['full_name','sid','branch','gender','DOB','email','mobile_number','profile_pic']

class CCSProfileForm(ModelForm):
    class Meta:
        model=userprofile
        fields=['full_name','sid','branch','gender','DOB','email','mobile_number','profile_pic']

class CDGCProfileForm(ModelForm):
    class Meta:
        model=userprofile
        fields=['full_name','gender','DOB','email','mobile_number','profile_pic']

class DAProfileForm(ModelForm):
    class Meta:
        model=userprofile
        fields=['full_name','gender','DOB','email','mobile_number','profile_pic']

class DSAProfileForm(ModelForm):
    class Meta:
        model=userprofile
        fields=['full_name','gender','DOB','email','mobile_number','profile_pic']

class HODProfileForm(ModelForm):
    class Meta:
        model=userprofile
        fields=['full_name','department','gender','DOB','email','mobile_number','profile_pic']

class OIProfileForm(ModelForm):
    class Meta:
        model=userprofile
        fields=['full_name','department','society_or_club_name','gender','DOB','email','mobile_number','profile_pic']

class OISecurityProfileForm(ModelForm):
    class Meta:
        model=userprofile
        fields=['full_name','department','gender','DOB','email','mobile_number','profile_pic']
