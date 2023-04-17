












from django.contrib import admin
from .models import Profile, Location, User, Contact
# Register your models here.
admin.site.register(Profile)
admin.site.register(Location)
admin.site.register(User)
admin.site.register(Contact)