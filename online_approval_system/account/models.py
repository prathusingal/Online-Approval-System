from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from PIL import Image

class userprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50,blank=False)
    profile_pic=models.ImageField(upload_to='profile_pic/',default="profile_pic/statue.jpg",blank=True, null=True)
    department_CHOICES=(
    ('None','------'),
    ('Computer Science and Engineering','Computer Science and Engineering'),
    ('Electronics and Communication Engineering','Electronics and Communication Engineering'),
    ('Electrical Engineering','Electrical Engineering'),
    ('Mechanical Engineering','Mechanical Engineering'),
    ('Civil Engineering','Civil Engineering'),
    ('Production and Industrial Engineering','Production and Industrial Engineering'),
    ('Aerospace Engineering','Aerospace Engineering'),
    ('Metallurgical Engineering','Metallurgical Engineering'),
    )
    department=models.CharField(max_length=100,choices=department_CHOICES,default=None,blank=False, null=True)
    society_choices=(
    ('None','------'),
    ('AMS','AMS'),
    ('ASCE', 'ASCE'),
    ('ASME', 'ASME'),
    ('ACM', 'ACM'),
    ('IIM', 'IIM'),
    ('ISTE', 'ISTE'),
    ('IEEE', 'IEEE'),
    ('IETE', 'IETE'),
    ('SAE', 'SAE'),
    ('SME', 'SME'),
    ('SESI', 'SESI'),
    ('ROBOTICS', 'ROBOTICS'),
    ('NSS', 'NSS'),
    ('NCC', 'NCC'),
    ('Art and Photography Club', 'Art and Photography Club'),
    ('Music Club', 'Music Club'),
    ('Dramatics Club', 'Dramatics Club'),
    ('Speakers Association & Study Circle', 'Speakers Association & Study Circle'),
    ('Projection Design Club', 'Projection Design Club'),
    ('Rotaract Club', 'Rotaract Club'),
    ('Communication Club', 'Communication Club'),
    ('Student Counselling Cell','Student Counselling Cell'),
    ('Women Empowerment Cell','Women Empowerment Cell'),
    ('EIC','EIC'),
    )
    society_or_club_name=models.CharField(max_length=50,choices=society_choices,default=None,blank=False, null=True)
    full_name = models.CharField(max_length=50,default=None,blank=True, null=True)
    sid = models.CharField(max_length=50,default=None,blank=True, null=True)
    branch=models.CharField(max_length=100,choices=department_CHOICES,default=None,blank=False, null=True)
    year_choice=(
    ('N','------'),
    ('1','1'),
    ('2','2'),
    ('3','3'),
    ('4','4'),
    )
    year=models.CharField(max_length=1,default=None,choices=year_choice,blank=False, null=True)
    GENDER_CHOICES = (
        ('N','------'),
        ('M', 'Male'),
        ('F', 'Female'),
        ('O','Other'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,default=None,blank=False, null=True)
    DOB=models.DateField(default=None,blank=True, null=True,help_text="Use %YYYY-%MM-%DD format.")
    mobile_number=models.CharField(max_length=10,default=None,blank=True, null=True)
    email=models.EmailField(default=None,blank=False, null=True)

    def __str__(self):
        return self.user.username

def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = userprofile(user=user)
        user_profile.save()
post_save.connect(create_profile, sender=User)


class reimbursement(models.Model):
    type_CHOICES=(
    ('None','------'),
    ('Technical','Technical'),
    ('Cultural','Cultural'),
    )
    department_CHOICES=(
    ('None','------'),
    ('Computer Science and Engineering','Computer Science and Engineering'),
    ('Electronics and Communication Engineering','Electronics and Communication Engineering'),
    ('Electrical Engineering','Electrical Engineering'),
    ('Mechanical Engineering','Mechanical Engineering'),
    ('Civil Engineering','Civil Engineering'),
    ('Production and Industrial Engineering','Production and Industrial Engineering'),
    ('Aerospace Engineering','Aerospace Engineering'),
    ('Metallurgical Engineering','Metallurgical Engineering'),
    )
    society_choices=(
    ('None','------'),
    ('AMS','AMS'),
    ('ASCE', 'ASCE'),
    ('ASME', 'ASME'),
    ('ACM', 'ACM'),
    ('IIM', 'IIM'),
    ('ISTE', 'ISTE'),
    ('IEEE', 'IEEE'),
    ('IETE', 'IETE'),
    ('SAE', 'SAE'),
    ('SME', 'SME'),
    ('SESI', 'SESI'),
    ('ROBOTICS', 'ROBOTICS'),
    ('NSS', 'NSS'),
    ('NCC', 'NCC'),
    ('Art and Photography Club', 'Art and Photography Club'),
    ('Music Club', 'Music Club'),
    ('Dramatics Club', 'Dramatics Club'),
    ('Speakers Association & Study Circle', 'Speakers Association & Study Circle'),
    ('Projection Design Club', 'Projection Design Club'),
    ('Rotaract Club', 'Rotaract Club'),
    ('Communication Club', 'Communication Club'),
    ('Student Counselling Cell','Student Counselling Cell'),
    ('Women Empowerment Cell','Women Empowerment Cell'),
    ('EIC','EIC'),
    )
    year_choice=(
    ('N','------'),
    ('1','1'),
    ('2','2'),
    ('3','3'),
    ('4','4'),
    )
    approval_choices=(
    ('None','------'),
    ('approved','approved'),
    ('not approved','not approved'),
    )
    filed_by = models.IntegerField(default=None,blank=False, null=True)
    full_name = models.CharField(max_length=50,default=None,blank=False, null=True)
    sid = models.CharField(max_length=50,default=None,blank=False, null=True)
    branch=models.CharField(max_length=100,choices=department_CHOICES,default=None,blank=False, null=True)
    year=models.CharField(max_length=1,default=None,choices=year_choice,blank=False, null=True)
    mobile_number=models.CharField(max_length=10,default=None,blank=False, null=True)
    email=models.EmailField(default=None,blank=False, null=True)
    name_of_club_or_technical_society=models.CharField(max_length=50,choices=society_choices,default=None,blank=False, null=True)
    type=models.CharField(max_length=50,choices=type_CHOICES,default=None,blank=False, null=True)
    event_name=models.CharField(max_length=10,default=None,blank=False, null=True)
    institute=models.CharField(max_length=10,default=None,blank=False, null=True)
    dates_for_which_team_will_be_away_from=models.DateField(max_length=10,default=None,blank=False, null=True,help_text="Use %YYYY-%MM-%DD format.")
    dates_for_which_team_will_be_away_to=models.DateField(max_length=10,default=None,blank=False, null=True,help_text="Use %YYYY-%MM-%DD format.")
    date_of_event_from=models.DateField(max_length=10,default=None,blank=False, null=True,help_text="Use %YYYY-%MM-%DD format.")
    date_of_event_to=models.DateField(max_length=10,default=None,blank=False, null=True,help_text="Use %YYYY-%MM-%DD format.")
    brief_event_description=models.TextField(default=None,blank=False, null=True)
    mode_of_travel=models.CharField(max_length=50,default=None,blank=False, null=True)
    attach_bills=models.FileField(upload_to='files/',default=None,blank=False, null=True)
    accomodation_or_food=models.BooleanField(default=None,blank=False, null=True)
    attach_proofs=models.FileField(upload_to='files/',default=None,blank=False, null=True)
    total_expenditure=models.IntegerField(default=None,blank=False, null=True)
    account_holder_name=models.CharField(max_length=50,default=None,blank=False, null=True)
    account_number=models.CharField(max_length=16,default=None,blank=False, null=True)
    IFSC_code=models.CharField(max_length=20,default=None,blank=False, null=True)
    PAN_card_number=models.CharField(max_length=20,default=None,blank=False, null=True)
    Secretary_approval=models.CharField(max_length=20,choices=approval_choices,default=None,blank=False, null=True)
    CCS_CTS_approval=models.CharField(max_length=20,choices=approval_choices,default=None,blank=False, null=True)
    OI_approval=models.CharField(max_length=20,default=None,choices=approval_choices,blank=False, null=True)
    CA_approval=models.CharField(max_length=20,default=None,choices=approval_choices,blank=False, null=True)
    DA_approval=models.CharField(max_length=20,default=None,choices=approval_choices,blank=False, null=True)
    DSA_approval=models.CharField(max_length=20,default=None,choices=approval_choices,blank=False, null=True)
    reason_for_disapproval=models.TextField(default=None,blank=True, null=True,help_text="Only required, if you are going to disapprove the application")

class event(models.Model):
    type_CHOICES=(
    ('None','------'),
    ('Technical','Technical'),
    ('Cultural','Cultural'),
    )
    approval_choices=(
    ('None','------'),
    ('approved','approved'),
    ('not approved','not approved'),
    )
    society_choices=(
    ('None','------'),
    ('AMS','AMS'),
    ('ASCE', 'ASCE'),
    ('ASME', 'ASME'),
    ('ACM', 'ACM'),
    ('IIM', 'IIM'),
    ('ISTE', 'ISTE'),
    ('IEEE', 'IEEE'),
    ('IETE', 'IETE'),
    ('SAE', 'SAE'),
    ('SME', 'SME'),
    ('SESI', 'SESI'),
    ('ROBOTICS', 'ROBOTICS'),
    ('NSS', 'NSS'),
    ('NCC', 'NCC'),
    ('Art and Photography Club', 'Art and Photography Club'),
    ('Music Club', 'Music Club'),
    ('Dramatics Club', 'Dramatics Club'),
    ('Speakers Association & Study Circle', 'Speakers Association & Study Circle'),
    ('Projection Design Club', 'Projection Design Club'),
    ('Rotaract Club', 'Rotaract Club'),
    ('Communication Club', 'Communication Club'),
    ('Student Counselling Cell','Student Counselling Cell'),
    ('Women Empowerment Cell','Women Empowerment Cell'),
    ('EIC','EIC'),
    )
    filed_by = models.IntegerField(default=None,blank=False, null=True)
    name_of_club_or_technical_society=models.CharField(max_length=50,choices=society_choices,default=None,blank=False, null=True)
    type=models.CharField(max_length=50,choices=type_CHOICES,default=None,blank=False, null=True)
    secretary_name=models.CharField(max_length=50,default=None,blank=False, null=True)
    secretary_SID=models.CharField(max_length=50,default=None,blank=False, null=True)
    event_name=models.CharField(max_length=10,default=None,blank=False, null=True)
    date_of_event_from=models.DateField(max_length=10,default=None,blank=False, null=True,help_text="Use %YYYY-%MM-%DD format.")
    date_of_event_to=models.DateField(max_length=10,default=None,blank=False, null=True,help_text="Use %YYYY-%MM-%DD format.")
    time_of_event_from=models.TimeField(default=None,blank=False, null=True,help_text="In 24 hour notation.")
    time_of_event_to=models.TimeField(default=None,blank=False, null=True,help_text="In 24 hour notation.")
    venues=models.CharField(max_length=25,default=None,blank=False, null=True)
    brief_event_description=models.TextField(default=None,blank=False, null=True)
    expected_expenditure_description=models.TextField(default=None,blank=False, null=True)
    total_expected_expenditure=models.IntegerField(default=None,blank=False, null=True)
    advance_required=models.BooleanField(default=None,blank=False, null=True)
    advance_required_justification=models.TextField(default=None,blank=True, null=True)
    advance_amount=models.IntegerField(default=None,blank=True, null=True)
    account_holder_name=models.CharField(max_length=50,default=None,blank=False, null=True)
    account_number=models.CharField(max_length=16,default=None,blank=False, null=True)
    IFSC_code=models.CharField(max_length=20,default=None,blank=False, null=True)
    PAN_card_number=models.CharField(max_length=20,default=None,blank=False, null=True)
    CCS_CTS_approval=models.CharField(max_length=20,default=None,choices=approval_choices,blank=False, null=True)
    OI_approval=models.CharField(max_length=20,default=None,blank=False,choices=approval_choices, null=True)
    CA_approval=models.CharField(max_length=20,default=None,blank=False,choices=approval_choices, null=True)
    DA_approval=models.CharField(max_length=20,default=None,blank=False,choices=approval_choices, null=True)
    DSA_approval=models.CharField(max_length=20,default=None,blank=False,choices=approval_choices, null=True)
    reason_for_disapproval=models.TextField(default=None,blank=True, null=True,help_text="Only required, if you are going to disapprove the application")


class auditorium(models.Model):
    type_CHOICES=(
    ('None','------'),
    ('Technical','Technical'),
    ('Cultural','Cultural'),
    )
    approval_choices=(
    ('None','------'),
    ('approved','approved'),
    ('not approved','not approved'),
    )
    society_choices=(
    ('None','------'),
    ('AMS','AMS'),
    ('ASCE', 'ASCE'),
    ('ASME', 'ASME'),
    ('ACM', 'ACM'),
    ('IIM', 'IIM'),
    ('ISTE', 'ISTE'),
    ('IEEE', 'IEEE'),
    ('IETE', 'IETE'),
    ('SAE', 'SAE'),
    ('SME', 'SME'),
    ('SESI', 'SESI'),
    ('ROBOTICS', 'ROBOTICS'),
    ('NSS', 'NSS'),
    ('NCC', 'NCC'),
    ('Art and Photography Club', 'Art and Photography Club'),
    ('Music Club', 'Music Club'),
    ('Dramatics Club', 'Dramatics Club'),
    ('Speakers Association & Study Circle', 'Speakers Association & Study Circle'),
    ('Projection Design Club', 'Projection Design Club'),
    ('Rotaract Club', 'Rotaract Club'),
    ('Communication Club', 'Communication Club'),
    ('Student Counselling Cell','Student Counselling Cell'),
    ('Women Empowerment Cell','Women Empowerment Cell'),
    ('EIC','EIC'),
    )
    progress_CHOICES=(
    ('None','------'),
    ('in-progress','in-progress'),
    ('approved','approved'),
    ('dismissed','dismissed'),
    )
    filed_by = models.IntegerField(default=None,blank=False, null=True)
    name_of_club_or_technical_society=models.CharField(max_length=50,choices=society_choices,default=None,blank=False, null=True)
    type=models.CharField(max_length=20,choices=type_CHOICES,default=None,blank=False, null=True)
    event_name=models.CharField(max_length=100,default=None,blank=False, null=True)
    date=models.DateField(default=None,blank=False, null=True,help_text="Use %YYYY-%MM-%DD format.")
    time_from=models.TimeField(default=None,blank=False, null=True,help_text="In 24 hour notation.")
    time_to=models.TimeField(default=None,blank=False, null=True,help_text="In 24 hour notation.")
    brief_event_description=models.TextField(default=None,blank=False, null=True)
    secretary_name=models.CharField(max_length=50,default=None,blank=False, null=True)
    secretary_SID=models.CharField(max_length=50,default=None,blank=False, null=True)
    OI_approval=models.CharField(max_length=20,default=None,blank=False,choices=approval_choices, null=True)
    CDGC_approval=models.CharField(max_length=20,default=None,blank=False,choices=approval_choices, null=True)
    DA_approval=models.CharField(max_length=20,default=None,blank=False,choices=approval_choices, null=True)
    DSA_approval=models.CharField(max_length=20,default=None,blank=False,choices=approval_choices, null=True)
    reason_for_disapproval=models.TextField(default=None,blank=True, null=True,help_text="Required, if you are going to disapprove the application")
    progress=models.CharField(max_length=20,default=None,blank=False,choices=progress_CHOICES, null=True)

# if id.role=='Student':
#     return render(request,"Student/homepage.html",{})
# elif id.role=='Secretary(Club/Tech Society/NSS/NCC/Others)':
#     return render(request,"Secretary/homepage.html",{})
# elif id.role=='Head of Department':
#     return render(request,"HOD/homepage.html",{})
# elif id.role=='CDGC':
#     return render(request,"CDGC/homepage.html",{})
# elif id.role=='Dean Student Affairs':
#     return render(request,"DSA/homepage.html",{})
# elif id.role=='Dealing Assistant of DSA':
#     return render(request,"DA/homepage.html",{})
# elif id.role=='Chief Technical Society':
#     return render(request,"CTS/homepage.html",{})
# elif id.role=='Chief Cultural Clubs':
#     return render(request,"CCS/homepage.html",{})
# elif id.role=='Chief Advisor':
#     return render(request,"CA/homepage.html",{})
# elif id.role=='O/I(Club/Tech Society/NSS/NCC/Others)':
#     return render(request,"OI/homepage.html",{})
# else:
#     return render(request,"OISecurity/homepage.html",{})


class lecturehalls(models.Model):
    progress_CHOICES=(
    ('None','------'),
    ('in-progress','in-progress'),
    ('approved','approved'),
    ('dismissed','dismissed'),
    )
    venue_choice=(
    ('None','------'),
    ('L-1','L-1'),
    ('L-2','L-2'),
    ('L-3','L-3'),
    ('L-4','L-4'),
    ('L-5','L-5'),
    ('L-6','L-6'),
    ('L-7','L-7'),
    ('L-8','L-8'),
    ('L-9','L-9'),
    ('L-10','L-10'),
    ('L-11','L-11'),
    ('L-12','L-12'),
    ('L-13','L-13'),
    ('L-14','L-14'),
    ('L-15','L-15'),
    ('L-16','L-16'),
    ('L-17','L-17'),
    ('L-18','L-18'),
    ('L-19','L-19'),
    ('L-20','L-20'),
    ('L-21','L-21'),
    ('L-22','L-22'),
    ('L-23','L-23'),
    ('L-24','L-24'),
    ('L-25','L-25'),
    ('L-26','L-26'),
    ('L-27','L-27'),
    ('L-28','L-28'),
    ('L-29','L-29'),
    ('L-30','L-30'),
    ('L-31','L-31'),
    )

    type_CHOICES=(
    ('None','------'),
    ('Technical','Technical'),
    ('Cultural','Cultural'),
    )
    approval_choices=(
    ('None','------'),
    ('approved','approved'),
    ('not approved','not approved'),
    )
    society_choices=(
    ('None','------'),
    ('AMS','AMS'),
    ('ASCE', 'ASCE'),
    ('ASME', 'ASME'),
    ('ACM', 'ACM'),
    ('IIM', 'IIM'),
    ('ISTE', 'ISTE'),
    ('IEEE', 'IEEE'),
    ('IETE', 'IETE'),
    ('SAE', 'SAE'),
    ('SME', 'SME'),
    ('SESI', 'SESI'),
    ('ROBOTICS', 'ROBOTICS'),
    ('NSS', 'NSS'),
    ('NCC', 'NCC'),
    ('Art and Photography Club', 'Art and Photography Club'),
    ('Music Club', 'Music Club'),
    ('Dramatics Club', 'Dramatics Club'),
    ('Speakers Association & Study Circle', 'Speakers Association & Study Circle'),
    ('Projection Design Club', 'Projection Design Club'),
    ('Rotaract Club', 'Rotaract Club'),
    ('Communication Club', 'Communication Club'),
    ('Student Counselling Cell','Student Counselling Cell'),
    ('Women Empowerment Cell','Women Empowerment Cell'),
    ('EIC','EIC'),
    )
    filed_by = models.IntegerField(default=None,blank=False, null=True)
    name_of_club_or_technical_society=models.CharField(max_length=50,choices=society_choices,default=None,blank=False, null=True)
    type=models.CharField(max_length=50,choices=type_CHOICES,default=None,blank=False, null=True)
    date_from=models.DateField(default=None,blank=False, null=True,help_text="Use %YYYY-%MM-%DD format.")
    date_to=models.DateField(default=None,blank=False, null=True,help_text="Use %YYYY-%MM-%DD format.")
    time_from=models.TimeField(default=None,blank=False, null=True,help_text="In 24 hour notation.")
    time_to=models.TimeField(default=None,blank=False, null=True,help_text="In 24 hour notation.")
    place=models.CharField(max_length=100,default=None,choices=venue_choice,blank=False, null=True)
    reason=models.TextField(default=None,blank=False, null=True)
    secretary_name=models.CharField(max_length=50,default=None,blank=False, null=True)
    secretary_SID=models.CharField(max_length=50,default=None,blank=False, null=True)
    OI_approval=models.CharField(max_length=20,default=None,blank=False,choices=approval_choices, null=True)
    OISecurity_approval=models.CharField(max_length=20,default=None,blank=False,choices=approval_choices, null=True)
    reason_for_disapproval=models.TextField(default=None,blank=True, null=True,help_text="Only required, if you are going to disapprove the application")
    progress=models.CharField(max_length=20,default=None,blank=False,choices=progress_CHOICES, null=True)


class labs(models.Model):
    progress_CHOICES=(
    ('None','------'),
    ('in-progress','in-progress'),
    ('approved','approved'),
    ('dismissed','dismissed'),
    )
    venue_choice=(
    ('None','------'),
    ('LAB-1(place-A)','LAB-1(place-A)'),
    ('LAB-1(place-B)','LAB-1(place-B)'),
    ('LAB-1(place-C)','LAB-1(place-C)'),
    ('LAB-1(place-D)','LAB-1(place-D)'),
    ('LAB-1(place-E)','LAB-1(place-E)'),
    ('LAB-2(place-A)','LAB-2(place-A)'),
    ('LAB-2(place-B)','LAB-2(place-B)'),
    ('LAB-2(place-C)','LAB-2(place-C)'),
    ('LAB-2(place-D)','LAB-2(place-D)'),
    ('LAB-2(place-E)','LAB-2(place-E)'),
    ('LAB-3(place-A)','LAB-3(place-A)'),
    ('LAB-3(place-B)','LAB-3(place-B)'),
    ('LAB-3(place-C)','LAB-3(place-C)'),
    ('LAB-3(place-D)','LAB-3(place-D)'),
    ('LAB-3(place-E)','LAB-3(place-E)'),
    ('LAB-4(place-A)','LAB-4(place-A)'),
    ('LAB-4(place-B)','LAB-4(place-B)'),
    ('LAB-4(place-C)','LAB-4(place-C)'),
    ('LAB-4(place-D)','LAB-4(place-D)'),
    ('LAB-4(place-E)','LAB-4(place-E)'),
    ('LAB-5(place-A)','LAB-5(place-A)'),
    ('LAB-5(place-B)','LAB-5(place-B)'),
    ('LAB-5(place-C)','LAB-5(place-C)'),
    ('LAB-5(place-D)','LAB-5(place-D)'),
    ('LAB-5(place-E)','LAB-5(place-E)')
    )

    approval_choices=(
    ('None','------'),
    ('approved','approved'),
    ('not approved','not approved'),
    )
    department_CHOICES=(
    ('None','------'),
    ('Computer Science and Engineering','Computer Science and Engineering'),
    ('Electronics and Communication Engineering','Electronics and Communication Engineering'),
    ('Electrical Engineering','Electrical Engineering'),
    ('Mechanical Engineering','Mechanical Engineering'),
    ('Civil Engineering','Civil Engineering'),
    ('Production and Industrial Engineering','Production and Industrial Engineering'),
    ('Aerospace Engineering','Aerospace Engineering'),
    ('Metallurgical Engineering','Metallurgical Engineering'),
    )
    year_choice=(
    ('N','------'),
    ('1','1'),
    ('2','2'),
    ('3','3'),
    ('4','4'),
    )
    filed_by = models.IntegerField(default=None,blank=False, null=True)
    full_name = models.CharField(max_length=50,default=None,blank=False, null=True)
    sid = models.CharField(max_length=50,default=None,blank=False, null=True)
    branch=models.CharField(max_length=100,default=None,blank=False,choices=department_CHOICES ,null=True)
    year=models.CharField(max_length=1,default=None,choices=year_choice,blank=False, null=True)
    mobile_number=models.CharField(max_length=10,default=None,blank=False, null=True)
    email=models.EmailField(default=None,blank=False, null=True)
    place=models.CharField(max_length=100,default=None,choices=venue_choice,blank=False, null=True)
    date_from=models.DateField(default=None,blank=False, null=True,help_text="Use %YYYY-%MM-%DD format.")
    date_to=models.DateField(default=None,blank=False, null=True,help_text="Use %YYYY-%MM-%DD format.")
    time_from=models.TimeField(default=None,blank=False, null=True,help_text="In 24 hour notation.")
    time_to=models.TimeField(default=None,blank=False, null=True,help_text="In 24 hour notation.")
    brief_project_description=models.TextField(default=None,blank=False, null=True)
    department_related_to_project=models.CharField(max_length=100,default=None,blank=False,choices=department_CHOICES ,null=True)
    project_report=models.FileField(upload_to='files/',default=None,blank=False, null=True)
    HOD_approval=models.CharField(max_length=20,default=None,blank=False,choices=approval_choices, null=True)
    DA_approval=models.CharField(max_length=20,default=None,blank=False,choices=approval_choices, null=True)
    DSA_approval=models.CharField(max_length=20,default=None,blank=False,choices=approval_choices, null=True)
    reason_for_disapproval=models.TextField(default=None,blank=True, null=True,help_text="Only required, if you are going to disapprove the application")
    progress=models.CharField(max_length=20,default='in-progress',blank=False,choices=progress_CHOICES, null=True)
