from rest_framework import serializers
from .models import  Member, Product, Yelam, Token, Category
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'


class YelamSerializer(serializers.ModelSerializer):
    member = serializers.SlugRelatedField(slug_field='pulli_id', queryset=Member.objects.all(), required=True)
    member_name = serializers.SerializerMethodField()
    family_name = serializers.SerializerMethodField()
    phone_1 = serializers.SerializerMethodField()
    product_name = serializers.SerializerMethodField()

    class Meta:
        model = Yelam
        fields = [
            "id",
            "manual_book_srno",
            "remarks",
            "product",
            "product_name",
            "member",
            "member_name",
            "family_name",
            "phone_1",
            "bidder_type",
            "guest_name",
            "bid_amount",
            "guest_whatsapp",
            "guest_native",
        ]

    def get_member_name(self, obj):
        return obj.member.name if obj.member else None

    def get_family_name(self, obj):
        return obj.member.family_name if obj.member else None

    def get_phone_1(self, obj):
        return obj.member.mobile_1 if obj.member else None
    
    def get_product_name(self, obj):
        return obj.product.product_name if obj.product else None 


    def validate(self, data):
        bidder_type = data.get("bidder_type")
        guest_name = data.get("guest_name")
        guest_whatsapp = data.get("guest_whatsapp")
        guest_native = data.get("guest_native")

        if bidder_type == Yelam.INHOUSE:
            # Ensure guest-related fields are not provided for inhouse
            if guest_name or guest_whatsapp or guest_native:
                raise serializers.ValidationError(
                    "Guest-related fields (guest_name, guest_whatsapp, guest_native) should not be provided for inhouse bidders."
                )

        elif bidder_type == Yelam.EXTERNAL:
            # Ensure guest-related fields are provided for guest
            if not guest_name or not guest_whatsapp or not guest_native:
                raise serializers.ValidationError(
                    "Guest-related fields (guest_name, guest_whatsapp, guest_native) are required for external (guest) bidders."
                )

        return data


class TokenSerializer(serializers.ModelSerializer):
    member = serializers.PrimaryKeyRelatedField(queryset=Member.objects.all(), required=True)  # Change to PrimaryKeyRelatedField

    class Meta:
        model = Token
        fields = ["id", "number", "year", "member"]

    def validate(self, data):
        # Optionally, validate if the combination of member, year, and number is unique
        if Token.objects.filter(member=data['member'], year=data['year'], number=data['number']).exists():
            raise serializers.ValidationError("This token already exists for the given member, year, and number.")
        return data

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'product_name', 'category']

class CategoryWithProductsSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'products']
