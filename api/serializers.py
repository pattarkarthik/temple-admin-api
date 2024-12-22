from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Member

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password":{"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'

from rest_framework import serializers
from .models import YelamProduct, Yelam, Token, Member

class YelamProductSerializer(serializers.ModelSerializer):
    member = serializers.StringRelatedField(read_only=True)  # Display member's string representation

    class Meta:
        model = YelamProduct
        fields = ["id", "name", "member"]


class YelamSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField(read_only=True)  # Display product's string representation
    member = serializers.StringRelatedField(read_only=True)  # Display member's string representation

    class Meta:
        model = Yelam
        fields = [
            "id",
            "product",
            "member",
            "bidder_type",
            "bidder_name",
            "bid_amount",
            "pending_amount",
        ]

    def validate(self, data):
        # Custom validation logic for Yelam model
        bidder_type = data.get("bidder_type")
        member = data.get("member")
        bidder_name = data.get("bidder_name")

        if bidder_type == Yelam.INHOUSE and not member:
            raise serializers.ValidationError({"member": "Member must be provided for inhouse bids."})

        if bidder_type == Yelam.EXTERNAL and not bidder_name:
            raise serializers.ValidationError({"bidder_name": "Bidder name must be provided for external bids."})

        if bidder_type == Yelam.EXTERNAL and not member:
            raise serializers.ValidationError({"member": "Reference member must be provided for external bids."})

        return data


class TokenSerializer(serializers.ModelSerializer):
    member = serializers.StringRelatedField(read_only=True)  # Display member's string representation

    class Meta:
        model = Token
        fields = ["id", "number", "year", "member"]
