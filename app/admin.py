from django.contrib import admin

from app.models import *

# Register your models here.
admin.site.register(Lessons)
admin.site.register(Group)
admin.site.register(GeneratedSchedule)
admin.site.register(Teachers)
admin.site.register(Cabinets)