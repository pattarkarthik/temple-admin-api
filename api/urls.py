from django.urls import path
from .views import (
    MemberListCreateView,
    MemberDetailView,
    YelamProductListCreateView,
    YelamProductDetailView,
    YelamListCreateView,
    YelamDetailView,
    TokenListCreateView,
    TokenDetailView,
)

urlpatterns = [
    # Member URLs
    path('members/', MemberListCreateView.as_view(), name='member-list-create'),
    path('members/<int:pk>/', MemberDetailView.as_view(), name='member-detail'),
    path('members/<int:pk>/delete/', MemberDetailView.as_view(), name='member-delete'), 

    # YelamProduct URLs
    path('yelam-products/', YelamProductListCreateView.as_view(), name='yelamproduct-list-create'),
    path('yelam-products/<int:pk>/', YelamProductDetailView.as_view(), name='yelamproduct-detail'),
    path('yelam-products/<int:pk>/delete/', YelamProductDetailView.as_view(), name='yelamproduct-delete'),

    # Yelam URLs
    path('yelams/', YelamListCreateView.as_view(), name='yelam-list-create'),
    path('yelams/<int:pk>/', YelamDetailView.as_view(), name='yelam-detail'),
    path('yelams/<int:pk>/delete/', YelamDetailView.as_view(), name='yelam-delete'),

    # Token URLs
    path('tokens/', TokenListCreateView.as_view(), name='token-list-create'),
    path('tokens/<int:pk>/', TokenDetailView.as_view(), name='token-detail'),
    path('tokens/<int:pk>/delete/', TokenDetailView.as_view(), name='token-delete'),
]
