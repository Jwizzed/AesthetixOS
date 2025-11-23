import uuid
from django.db import models
from django.contrib.auth.models import User
from clinic.models import Patient

class Product(models.Model):
    """
    Inventory Item or Service.
    """
    TYPE_CHOICES = [
        ('SERVICE', 'Service (Laser, Facial)'),
        ('DRUG', 'Drug (Botox, Filler)'),
        ('RETAIL', 'Retail Product'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sku = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    product_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Inventory check
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.sku} - {self.name}"

class Course(models.Model):
    """
    A prepaid package definition.
    e.g., "Acne Clear 10 Sessions"
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    product_included = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='courses_defined')
    total_sessions = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.total_sessions} sessions)"

class UserCourseBalance(models.Model):
    """
    Tracks what a patient actually owns.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, related_name='course_balances')
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    
    remaining_sessions = models.PositiveIntegerField()
    purchased_date = models.DateTimeField(auto_now_add=True)
    last_used_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('patient', 'course')

class Transaction(models.Model):
    """
    A sales record. Triggers commission calculation.
    """
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('VOID', 'Voided'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, related_name='transactions')
    staff_1 = models.ForeignKey(User, on_delete=models.PROTECT, related_name='primary_sales', null=True)
    staff_2 = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='secondary_sales', null=True, blank=True)
    
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

class CommissionLog(models.Model):
    """
    Output of the Async Calculation Task.
    """
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, related_name='commission_log')
    staff = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    calculation_details = models.JSONField(help_text="Snapshots the formula used")
    calculated_at = models.DateTimeField(auto_now_add=True)
