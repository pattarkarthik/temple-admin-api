from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserSerializer, MemberSerializer, ProductSerializer, YelamSerializer, TokenSerializer, CategoryWithProductsSerializer,PaymentTransactionSerializer
from .models import Member, Category, Yelam, Token, Product, PaymentTransaction
from .communication import send_message
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json



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

class PaymentTransactionListCreateView(generics.ListCreateAPIView):
    queryset = PaymentTransaction.objects.select_related('yelam').all()
    serializer_class = PaymentTransactionSerializer
    permission_classes = [IsAuthenticated]

class PaymentTransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PaymentTransaction.objects.select_related('yelam').all()
    serializer_class = PaymentTransactionSerializer
    permission_classes = [IsAuthenticated]

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count, Avg
from .models import Member, Yelam, Product, Token, PaymentTransaction

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Total Members
        total_members = Member.objects.count()

        # Total Bid Amount
        total_bid_amount = Yelam.objects.aggregate(total_bid_amount=Sum('bid_amount'))['total_bid_amount'] or 0

        # Total Pending Amount
        total_pending_amount = Yelam.objects.aggregate(total_pending_amount=Sum('pending_amount'))['total_pending_amount'] or 0

        # Total Yelams
        total_yelams = Yelam.objects.count()

        # Total Products
        total_products = Product.objects.count()

        # Members by City
        members_by_city = Member.objects.values('city').annotate(count=Count('pulli_id')).order_by('-count')

        # Members by Karai
        members_by_karai = Member.objects.values('karai').annotate(count=Count('pulli_id')).order_by('-count')

        # Tokens Grouped by Year with Details
        tokens_grouped_by_year = {}
        tokens_data = Token.objects.values('year', 'member__name', 'member__family_name', 'number')

        for token in tokens_data:
            year = token['year']
            if year not in tokens_grouped_by_year:
                tokens_grouped_by_year[year] = []
            tokens_grouped_by_year[year].append({
                "member_name": token['member__name'],
                "family_name": token['member__family_name'],
                "number": token['number']
            })

        # Additional KPIs

        # Total Paid Amount
        total_paid_amount = PaymentTransaction.objects.aggregate(total_paid_amount=Sum('amount'))['total_paid_amount'] or 0

        # Yelams by Payment Status
        yelams_by_payment_status = Yelam.objects.values('payment_status').annotate(count=Count('id')).order_by('-count')

        # Top Products by Number of Yelams
        top_products_by_yelams = Product.objects.annotate(yelam_count=Count('yelam')).order_by('-yelam_count')[:5]

        # Yelams by Bidder Type (Filtered for Inhouse and Guest)
        yelams_by_bidder_type = Yelam.objects.filter(bidder_type__in=['inhouse', 'guest']).values('bidder_type').annotate(count=Count('id')).order_by('-count')

        # Top Members by Number of Yelams
        top_members_by_yelams = Member.objects.annotate(yelam_count=Count('yelam')).order_by('-yelam_count')[:5]

        # Yelams by Product Category
        yelams_by_product_category = Yelam.objects.values('product__category').annotate(count=Count('id')).order_by('-count')

        # Average Bid Amount
        average_bid_amount = Yelam.objects.aggregate(average_bid_amount=Avg('bid_amount'))['average_bid_amount'] or 0

        # Pending Payments by Member
        pending_payments_by_member = (Yelam.objects.values('member__name', 'member__family_name')
                                      .annotate(total_pending=Sum('pending_amount'))
                                      .order_by('-total_pending')[:5])

        # Response Data
        data = {
            "total_members": total_members,
            "total_bid_amount": total_bid_amount,
            "total_pending_amount": total_pending_amount,
            "total_yelams": total_yelams,
            "total_products": total_products,
            "members_by_city": list(members_by_city),
            "members_by_karai": list(members_by_karai),
            "tokens_details": tokens_grouped_by_year,
            "total_paid_amount": total_paid_amount,
            "yelams_by_payment_status": list(yelams_by_payment_status),
            "top_products_by_yelams": [
                {
                    "product_name": product.product_name,
                    "yelam_count": product.yelam_count
                }
                for product in top_products_by_yelams
            ],
            "yelams_by_bidder_type": list(yelams_by_bidder_type),
            "top_members_by_yelams": [
                {
                    "member_name": member.name,
                    "yelam_count": member.yelam_count
                }
                for member in top_members_by_yelams
            ],
            "yelams_by_product_category": list(yelams_by_product_category),
            "average_bid_amount": average_bid_amount,
            "pending_payments_by_member": list(pending_payments_by_member),
        }

        return Response(data)

@csrf_exempt  # Use this only for testing; implement proper CSRF protection in production
def send_whatsapp(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            phone_numbers = data.get("phone_numbers", [])
            message = data.get("message", "")
            send_message(phone_numbers, message)

            return JsonResponse({"status": "success", "message": "Request received"})
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)
    
    return JsonResponse({"status": "error", "message": "Only POST method allowed"}, status=405)
