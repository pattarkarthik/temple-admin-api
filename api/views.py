from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import UserSerializer, MemberSerializer,YelamProductSerializer, YelamSerializer, TokenSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Member, YelamProduct, Yelam, Token
# Create your views here.

class CreateUserView(generics.CreateAPIView):
    queryset= User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class MemberListCreateView(generics.ListCreateAPIView):
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Member.objects.all()

class MemberDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Member.objects.all()

# YelamProduct Views
class YelamProductListCreateView(generics.ListCreateAPIView):
    queryset = YelamProduct.objects.all()
    serializer_class = YelamProductSerializer
    permission_classes = [IsAuthenticated]

class YelamProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = YelamProduct.objects.all()
    serializer_class = YelamProductSerializer
    permission_classes = [IsAuthenticated]


# Yelam Views
class YelamListCreateView(generics.ListCreateAPIView):
    queryset = Yelam.objects.all()
    serializer_class = YelamSerializer
    permission_classes = [IsAuthenticated]

class YelamDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Yelam.objects.all()
    serializer_class = YelamSerializer
    permission_classes = [IsAuthenticated]


# Token Views
class TokenListCreateView(generics.ListCreateAPIView):
    queryset = Token.objects.all()
    serializer_class = TokenSerializer
    permission_classes = [IsAuthenticated]

class TokenDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Token.objects.all()
    serializer_class = TokenSerializer
    permission_classes = [IsAuthenticated]
