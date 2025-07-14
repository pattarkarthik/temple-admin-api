from django.urls import path
from .views import (
    MemberListCreateView,
    MemberDetailView,
    ProductListCreateView,
    ProductDetailView,
    YelamListCreateView,
    YelamDetailView,
    TokenListCreateView,
    TokenDetailView,
    CategoryListCreateView,
    CategoryDetailView,
    PaymentTransactionListCreateView,
    PaymentTransactionDetailView,
    DashboardView,
    send_whatsapp
)

urlpatterns = [
    # Member URLs
    path('members/', MemberListCreateView.as_view(), name='member-list-create'),
    path('members/<str:pulli_id>/', MemberDetailView.as_view(), name='member-detail'),
    path('members/<str:pulli_id>/delete/', MemberDetailView.as_view(), name='member-delete'),

    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('categories/<int:pk>/delete/', CategoryDetailView.as_view(), name='category-delete'),


    # Product URLs
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/<int:pk>/delete/', ProductDetailView.as_view(), name='product-delete'),


    # Yelam URLs
    path('yelams/', YelamListCreateView.as_view(), name='yelam-list-create'),
    path('yelams/<int:pk>/', YelamDetailView.as_view(), name='yelam-detail'),
    path('yelams/<int:pk>/delete/', YelamDetailView.as_view(), name='yelam-delete'),

    path("transactions/", PaymentTransactionListCreateView.as_view(), name="transaction-list-create"),
    path("transactions/<int:pk>/", PaymentTransactionDetailView.as_view(), name="transaction-detail"),

    # Token URLs
    path('tokens/', TokenListCreateView.as_view(), name='token-list-create'),
    path('tokens/<int:pk>/', TokenDetailView.as_view(), name='token-detail'),
    path('tokens/<int:pk>/delete/', TokenDetailView.as_view(), name='token-delete'),

     path("send-communication/", send_whatsapp, name="send_communication"),
     path('dashboard/', DashboardView.as_view(), name='dashboard'),
]
