from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientViewSet, TreatmentSessionViewSet, UploadTokenView, ConfirmUploadView

router = DefaultRouter()
router.register(r'patients', PatientViewSet)
router.register(r'sessions', TreatmentSessionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('upload-token/', UploadTokenView.as_view(), name='upload-token'),
    path('confirm-upload/', ConfirmUploadView.as_view(), name='confirm-upload'),
]

