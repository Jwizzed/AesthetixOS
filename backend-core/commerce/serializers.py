from rest_framework import serializers
from .models import Product, Course, Transaction, CommissionLog

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class CommissionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommissionLog
        fields = '__all__'

