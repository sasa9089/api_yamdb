
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import UserViewSet, create_user, create_token
from .views import ReviewViewSet, CommentViewSet


v1_router = DefaultRouter
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
v1_router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', create_user, name='signup'),
    # path('v1/auth/token/', create_user, name='token'),
    ]

