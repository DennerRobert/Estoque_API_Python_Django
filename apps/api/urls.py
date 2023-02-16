from django.urls import path, include
from apps.api.views import UserViewSet
from apps.api import views
from rest_framework import routers 




router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('auth/', include('rest_framework.urls'), name='rest_framework')
    path('auth/token/', views.CustomAuthToken.as_view())
]