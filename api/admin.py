from django.contrib import admin
from .models import Member,  Yelam, Token, Category, Product

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('family_name', 'name', 'spouse_name', 'city', 'state', 'pin_code', 'pulli_id', 'native', 'karai')
    search_fields = ('family_name', 'name', 'spouse_name', 'pulli_id', 'native', 'karai')
    list_filter = ('city', 'state', 'native', 'karai')



@admin.register(Yelam)
class YelamAdmin(admin.ModelAdmin):
    list_display = ('manual_book_srno', 'product', 'member', 'bidder_type', 'guest_name', 'bid_amount',)
    list_filter = ('bidder_type',)
    search_fields = ('product__name', 'member__name', 'guest_name')

@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('number', 'year', 'member')
    search_fields = ('number', 'year', 'member__name')
    list_filter = ('year',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'category')
    search_fields = ('product_name', 'category__name')
    list_filter = ('category__name',)
