from django.contrib import admin

from .models import CustomUser, Category, VoteItem, Profile

admin.site.register(CustomUser)
admin.site.register(Category)
admin.site.register(VoteItem)
admin.site.register(Profile)