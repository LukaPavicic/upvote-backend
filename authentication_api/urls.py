from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('users', views.UserViewSet)
router.register('communities', views.CommunityViewSet)
router.register('userjoinedcommunities', views.UserJoinedCommunityViewSet)
router.register('posts', views.PostViewSet)
router.register('comments', views.CommentViewSet)
router.register('upvote', views.UpvoteViewSet)

urlpatterns = [
   path('', include(router.urls)),
   path('login/', views.UserLoginApiView.as_view()), 
   path('getcurrentuserid/', views.CurrentUserApiView.as_view()),   
]
