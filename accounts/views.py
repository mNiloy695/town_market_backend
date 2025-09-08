from django.shortcuts import render
from django.contrib.auth import get_user_model
User=get_user_model()
# Create your views here.
from rest_framework import viewsets
from .serializers import CustomUserRegistrationSerializer,LoginSerializer
from rest_framework import permissions,status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate,login,logout
from rest_framework_simplejwt.tokens import RefreshToken,TokenError

class CustomPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.method in ['POST']:
            return not request.user.is_authenticated
        return request.user.is_authenticated
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj==request.user 

class CustomUserRegistrationViewSet(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=CustomUserRegistrationSerializer
    permission_classes=[CustomPermission]

class Anonymous(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ['POST']:
            return not request.user.is_authenticated
        return [permissions.IsAuthenticated]


class LoginView(APIView):
    permission_classes=[Anonymous]
    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            username=serializer.validated_data.get('username')
            password=serializer.validated_data.get('password')
            user=authenticate(username=username,password=password)
            if user:
                login(request,user)
                refresh=RefreshToken.for_user(user)
                return Response({
                    "message":"Login Successfully",
                    'access':str(refresh.access_token),
                    'refresh':str(refresh)
                })
            return Response({"error":"Invalid Username or Password"})
        return Response(serializer.errors)




class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        refresh = request.data.get("refresh")
         
        if not refresh:
            return Response(
                {"error": "Refresh token is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = RefreshToken(refresh)
            token.blacklist()
        except TokenError:
            return Response(
                {"error": "Invalid or expired refresh token"},
                status=status.HTTP_400_BAD_REQUEST
            )
        logout(request)

        return Response(
            {"message": "Logout successfully"},
            status=status.HTTP_205_RESET_CONTENT
        )

            
        

        
