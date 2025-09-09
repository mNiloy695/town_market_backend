from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import CustomUserRegistrationViewSet,LoginView,LogoutView,activate

router=DefaultRouter()
router.register('register',CustomUserRegistrationViewSet)

urlpatterns = [
    path('',include(router.urls)),
    path('login/',LoginView.as_view()),
    path('logout/',LogoutView.as_view()),
    path('activate/<uid64>/<token>/',activate),
]
