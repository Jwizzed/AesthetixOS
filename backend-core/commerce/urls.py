from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CourseViewSet, TransactionViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'transactions', TransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

