from django.contrib import admin
from .models import User, Community, UserJoinedCommunity, Post, Comment, Upvote, Save

# Register your models here.

admin.site.register(User)
admin.site.register(Community)
admin.site.register(UserJoinedCommunity)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Upvote)
admin.site.register(Save)