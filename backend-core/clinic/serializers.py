from rest_framework import serializers
from core.serializers import PDPAMaskingField
from .models import Patient, TreatmentSession, ClinicalImage

class PatientSerializer(serializers.ModelSerializer):
    # Apply the custom masking field to the phone number
    phone_number = PDPAMaskingField()

    class Meta:
        model = Patient
        fields = [
            'id', 
            'hn', 
            'first_name', 
            'last_name', 
            'date_of_birth', 
            'phone_number',  # This is now masked
            'created_at'
        ]

class ClinicalImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicalImage
        fields = '__all__'

class TreatmentSessionSerializer(serializers.ModelSerializer):
    images = ClinicalImageSerializer(many=True, read_only=True)

    class Meta:
        model = TreatmentSession
        fields = '__all__'
        read_only_fields = ('doctor',)

