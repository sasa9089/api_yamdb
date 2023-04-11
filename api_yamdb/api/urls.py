from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import UserViewSet, create_user, create_token

router = DefaultRouter()

router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', create_user, name='signup'),
    # path('v1/auth/token/', create_user, name='token'),
    ]
