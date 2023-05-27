from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(packages)
admin.site.register(user_member)
admin.site.register(delivery_status)
admin.site.register(history)
admin.site.register(picker_schedule)