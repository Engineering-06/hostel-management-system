from django.contrib import admin

# Register your models here.

from .models import Student, Room,RoomAllocation,Fee,Complaint

admin.site.register(Student)
admin.site.register(Room)
admin.site.register(RoomAllocation)
admin.site.register(Fee)
admin.site.register(Complaint)