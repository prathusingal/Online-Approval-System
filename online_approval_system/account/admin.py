from django.contrib import admin
from .models import userprofile,reimbursement,event,auditorium,lecturehalls,labs
# Register your models here.
admin.site.register(userprofile)
admin.site.register(reimbursement)
admin.site.register(event)
admin.site.register(auditorium)
admin.site.register(lecturehalls)
admin.site.register(labs)
