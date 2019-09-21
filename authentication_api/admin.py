from django.contrib import admin
from .models import User, Community, UserJoinedCommunity, Post

# Register your models here.

admin.site.register(User)
admin.site.register(Community)
admin.site.register(UserJoinedCommunity)
admin.site.register(Post)
