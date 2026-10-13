from rest_framework import serializers
from django.contrib.auth.models import User
from core.models import Receipt


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Ta nazwa użytkownika jest już zajęta.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Ten adres email jest już zarejestrowany.")
        return value

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError({"password2": "Hasła muszą być identyczne."})
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user


class ReceiptSerializer(serializers.ModelSerializer):
    receipt_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Receipt
        fields = [
            "id",
            "shop_name",
            "transaction_date",
            "transaction_total_amount",
            "receipt_image_url",
            "created_at",
        ]
        read_only_fields = fields

    def get_receipt_image_url(self, obj):
        if obj.receipt_image:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.receipt_image.url)
            return obj.receipt_image.url
        return None


class ReceiptUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = ["receipt_image"]


class MonthlyStatSerializer(serializers.Serializer):
    month = serializers.DateField()
    total = serializers.DecimalField(max_digits=12, decimal_places=2)


class StatsSerializer(serializers.Serializer):
    total_expenses = serializers.DecimalField(max_digits=12, decimal_places=2)
    receipt_count = serializers.IntegerField()
    monthly_summary = MonthlyStatSerializer(many=True)