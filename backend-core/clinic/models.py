import uuid
from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):
    """
    Core patient identity.
    PDPA Sensitivity: High.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hn = models.CharField(max_length=20, unique=True, verbose_name="Hospital Number")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, db_index=True)
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['first_name', 'last_name']),
        ]

    def __str__(self):
        return f"{self.hn}: {self.first_name} {self.last_name}"

class TreatmentSession(models.Model):
    """
    Represents a single clinical visit.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, related_name='sessions')
    doctor = models.ForeignKey(User, on_delete=models.PROTECT, related_name='doctor_sessions')
    date = models.DateTimeField(auto_now_add=True)
    diagnosis_notes = models.TextField(blank=True)
    
    # Drawing JSON data from the Canvas Frontend (EMR Module)
    # Stores coordinates of injection points
    face_chart_data = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"Session {self.date.date()} - {self.patient.hn}"

class ClinicalImage(models.Model):
    """
    Links a high-res photo in MinIO to a treatment session.
    """
    IMAGE_TYPES = [
        ('BEFORE', 'Before Treatment'),
        ('AFTER', 'After Treatment'),
        ('LAB', 'Lab Result'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(TreatmentSession, on_delete=models.CASCADE, related_name='images')
    
    # This is the S3 Key (Path in MinIO bucket), not the file itself.
    # e.g., "patients/uuid/2023-10-27/img_001.jpg"
    s3_key = models.CharField(max_length=500)
    
    image_type = models.CharField(max_length=20, choices=IMAGE_TYPES, default='BEFORE')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.image_type} - {self.session}"
