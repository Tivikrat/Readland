from django.contrib import admin
from user_profile.models import UserProfile, UserList, UserListBook

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(UserList)
admin.site.register(UserListBook)
