from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register('users', views.UserViewSet)
router.register('communities', views.CommunityViewSet)
router.register('userjoinedcommunities', views.UserJoinedCommunityViewSet)
router.register('posts', views.PostViewSet)
router.register('comments', views.CommentViewSet)
router.register('upvote', views.UpvoteViewSet)
router.register('save', views.SaveViewSet)

urlpatterns = [
   path('', include(router.urls)),
   path('login/', views.UserLoginApiView.as_view()), 
   path('getcurrentuserid/', views.CurrentUserApiView.as_view()),
   path('userrelevantposts/', views.UserRelevantPosts.as_view())   
]