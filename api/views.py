from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserSerializer, MemberSerializer, ProductSerializer, YelamSerializer, TokenSerializer, CategoryWithProductsSerializer
from .models import Member, Category, Yelam, Token, Product

# Create your views here.

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
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
    lookup_field = 'pulli_id'  # Use pulli_id for member identification

    def get_queryset(self):
        return Member.objects.all()

    def patch(self, request, *args, **kwargs):
        """
        Handle PATCH request to update Member and create a new Token if required.
        """
        member = self.get_object()

        # Validate and update the Member data
        serializer = self.get_serializer(member, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_member = serializer.save()

        # Handle token creation/update logic (if token details are provided in the PATCH request)
        token_data = request.data.get("token", None)
        if token_data:
            token_year = token_data.get("year")
            token_number = token_data.get("number")

            # Create a new Token or update the existing one
            Token.objects.create(
                member=updated_member,
                year=token_year,
                number=token_number
            )

        # Return the updated member and token information
        return self.retrieve(request, *args, **kwargs)

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


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.prefetch_related('products').all()
    serializer_class = CategoryWithProductsSerializer
    permission_classes = [IsAuthenticated]

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.prefetch_related('products').all()
    serializer_class = CategoryWithProductsSerializer
    permission_classes = [IsAuthenticated]

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]