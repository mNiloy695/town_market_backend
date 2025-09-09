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
from .email import send_email
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from rest_framework.decorators import api_view
class CustomPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
                
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

    def perform_create(self, serializer):
        user=serializer.save(is_active=False)
        token=default_token_generator.make_token(user)
        uid=urlsafe_base64_encode(force_bytes(user.pk))
        subject="Activate You Account On Town Market Feni"
        activation_link=f'http://127.0.0.1:8000/account/activate/{uid}/{token}/'
        message=f"{user.username} Active your account !Please visite the link for activate you account {activation_link}"
        receiver_email=user.email
        send_email(subject,message,receiver_email)
    def get_queryset(self):
        user=self.request.user
        if user.is_staff:
            return User.objects.all()
        return User.objects.filter(pk=user.pk)

#activate user id
@api_view(['GET'])
def activate(request,uid64,token):
    try:
        uid=urlsafe_base64_decode(uid64).decode()
        user=User.objects.get(pk=uid)
    except (User.DoesNotExist,ValueError,TypeError):
        return Response({"error": "Invalid activation link"}, status=status.HTTP_400_BAD_REQUEST)
    
    if default_token_generator.check_token(user,token):
        if not user.is_active:
            user.is_active=True
            user.save()
            return Response({"success": "Account activated successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"info": "Account already active"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Activation link is invalid or expired"}, status=status.HTTP_400_BAD_REQUEST)

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

            
        

        
