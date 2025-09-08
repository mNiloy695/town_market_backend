from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import CustomUserRegistrationViewSet,LoginView,LogoutView

router=DefaultRouter()
router.register('register',CustomUserRegistrationViewSet)

urlpatterns = [
    path('',include(router.urls)),
    path('login/',LoginView.as_view()),
    path('logout/',LogoutView.as_view()),
]
