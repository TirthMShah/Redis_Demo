from rest_framework.generics import CreateAPIView
from django.contrib.auth.models import User
from demo.serializers.UserSerializer import UserRegisterSerializer
from rest_framework.permissions import AllowAny



class RegisterAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]