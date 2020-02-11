from django.contrib import admin
from .models import User, Community, UserJoinedCommunity, Post, Comment, Upvote, Save

admin.site.register(User)
admin.site.register(Community)
admin.site.register(UserJoinedCommunity)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Upvote)
admin.site.register(Save)